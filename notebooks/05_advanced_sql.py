import sqlite3
import pandas as pd # type: ignore

conn = sqlite3.connect("data/Chinook_Sqlite.sqlite")

def run(label, sql):
    print(f"\n{'='*55}")
    print(f"Q: {label}")
    print(f"{'='*55}")
    df = pd.read_sql(sql, conn)
    print(df.to_string())

# Q1
run("Customers from Brazil", """
    -- your SQL here
    select 
    FirstName, LastName, Email 
    from Customer
    where country='Brazil';
""")

# Q2
run("Tracks longer than 5 minutes", """
    -- your SQL here
    select name,(milliseconds)/30000 as Minutes 
    from Track 
    where minutes>=5 
    order by minutes desc;
""")

# Q3
run("Customer count by country", """
    -- your SQL here
    select country, count(country) as CustomerCount
    from Customer
    group by country
    order by CustomerCount desc;
""")

# Q4
run("Top 10 selling tracks", """
    -- your SQL here
    select t.trackid, t.name, sum(i.quantity) as TotalQuantitySold 
    from track t join invoiceline i
    on t.trackid=i.trackid
    group by t.trackid
    order by TotalQuantitySold desc
    limit 10;
""")

# Q5
run("Employees supporting most customers", """
    -- your SQL here
    select e.FirstName || ' ' || e.LastName as EmpName,
    count(c.CustomerId) as NumCustomers
    from Customer c
    join Employee e on e.EmployeeId=c.SupportRepId
    group by e.EmployeeId
    order by NumCustomers desc;
""")

# Q6
run("Total sales per country", """
    -- your SQL here
    select BillingCountry, round(sum(total),2) as TotalSales
    from Invoice
    group by BillingCountry
""")

# Q7
run("Albums with artist names", """
    -- your SQL here
    select al.title as Album, ar.name as Artist
    from album al
    join artist ar on al.artistid=ar.artistid;
""")

# Q8
run("Customers who spent more than average", """
    -- your SQL here
    select c.FirstName || ' ' || c.lastname as CustomerName,
    round(sum(i.total),2) as TotalSpent
    from customer c join invoice i
    on i.customerid=c.customerid 
    group by c.customerid
    having sum(i.total)>(select avg(CustomerTotal)
    from (select sum(total) as CustomerTotal
    from invoice
    group by customerid));
""")

# Q9
run("Most popular genre by tracks sold", """
    -- your SQL here
    select g.name , sum(il.quantity) as TotalQuantitySold
    from Genre g
    join track t on g.genreid=t.genreid
    join invoiceline il on t.trackid=il.trackid
    group by g.genreid
    order by TotalQuantitySold desc
    limit 1;
""")

# Q10a - without window functions
run("Top customer per country (subquery)", """
    -- your SQL here
    select c.country,
            c.firstname || ' ' || c.lastname as CustomerName,
            round(sum(i.total),2) as TotalSpent
    from customer c
    join invoice i on c.customerid=i.customerid
    group by c.customerid
    having sum(i.total)=(
        select max(sub.CustomerTotal)
        from (
            select c2.country,
                sum(i2.total) as CustomerTotal
            from customer c2
            join invoice i2 on c2.customerid=i2.customerid
            group by c2.customerid
        )sub
        where sub.country=c.country
    )
    order by c.country
""")

# Q10b - with ROW_NUMBER()
run("Top customer per country (ROW_NUMBER)", """
    -- your SQL here
    select Country, CustomerName, TotalSpent
    from(
        select c.Country,
            c.FirstName || ' ' || c.LastName as CustomerName,
            round(sum(i.Total), 2) as TotalSpent,
            ROW_NUMBER() over (
                PARTITION BY c.Country 
                ORDER BY SUM(i.Total) DESC
            ) as rn
        FROM Customer c
        JOIN Invoice i ON c.CustomerId = i.CustomerId
        GROUP BY c.CustomerId
    ) ranked
    WHERE rn = 1
    ORDER BY Country
""")

# Bonus Q11
run("Artist with highest revenue", """
    -- your SQL here
    SELECT ar.Name,
       ROUND(SUM(il.UnitPrice * il.Quantity), 2) as TotalRevenue
    FROM Artist ar
    JOIN Album al ON ar.ArtistId = al.ArtistId
    JOIN Track t ON al.AlbumId = t.AlbumId
    JOIN InvoiceLine il ON t.TrackId = il.TrackId
    GROUP BY ar.ArtistId
    ORDER BY TotalRevenue DESC
    LIMIT 1
""")

conn.close()