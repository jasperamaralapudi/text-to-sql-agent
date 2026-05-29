import sqlite3
import pandas as pd # type: ignore

conn = sqlite3.connect("data/Chinook_Sqlite.sqlite")

def run(label, sql):
    print(f"\n{'='*55}")
    print(f"Q: {label}")
    print(f"{'='*55}")
    df = pd.read_sql(sql, conn)
    print(df.to_string())

# B1: Monthly revenue trend
run("Total revenue per month", """
    SELECT strftime('%m', InvoiceDate) as Month,
           ROUND(SUM(Total), 2) as Revenue
    FROM Invoice
    GROUP BY Month
    ORDER BY Month
""")

# B2: Best sales rep by customer spending
run("Best sales rep", """
    SELECT e.FirstName || ' ' || e.LastName as SalesRep,
           ROUND(SUM(i.Total), 2) as TotalCustomerSpend
    FROM Employee e
    JOIN Customer c ON c.SupportRepId = e.EmployeeId
    JOIN Invoice i ON i.CustomerId = c.CustomerId
    GROUP BY e.EmployeeId
    ORDER BY TotalCustomerSpend DESC
""")

# B3: Loyal customers (more than 5 purchases)
run("Customers with more than 5 invoices", """
    SELECT c.FirstName || ' ' || c.LastName as Customer,
           COUNT(i.InvoiceId) as Purchases
    FROM Customer c
    JOIN Invoice i ON c.CustomerId = i.CustomerId
    GROUP BY c.CustomerId
    HAVING Purchases > 5
    ORDER BY Purchases DESC
""")

# B4: Top 10 best-selling tracks by quantity
run("Top 10 best-selling tracks", """
    SELECT t.Name, SUM(il.Quantity) as TotalSold
    FROM Track t
    JOIN InvoiceLine il ON t.TrackId = il.TrackId
    GROUP BY t.TrackId
    ORDER BY TotalSold DESC
    LIMIT 10
""")

# B5: Revenue per genre
run("Revenue per genre", """
    SELECT g.Name, ROUND(SUM(il.UnitPrice * il.Quantity), 2) as Revenue
    FROM Genre g
    JOIN Track t ON g.GenreId = t.GenreId
    JOIN InvoiceLine il ON t.TrackId = il.TrackId
    GROUP BY g.GenreId
    ORDER BY Revenue DESC
""")

# B6: Average order value by country
run("Avg order value by country", """
    SELECT BillingCountry,
           ROUND(AVG(Total), 2) as AvgOrderValue
    FROM Invoice
    GROUP BY BillingCountry
    ORDER BY AvgOrderValue DESC
""")

# B7: Top 5 longest tracks in minutes
run("Top 5 longest tracks in minutes", """
    SELECT Name,
           ROUND(Milliseconds / 60000.0, 2) as Minutes
    FROM Track
    ORDER BY Milliseconds DESC
    LIMIT 5
""")

# B8: Artist revenue ranking
run("Artist revenue ranking", """
    SELECT ar.Name,
           ROUND(SUM(il.UnitPrice * il.Quantity), 2) as TotalRevenue
    FROM Artist ar
    JOIN Album al ON ar.ArtistId = al.ArtistId
    JOIN Track t ON al.AlbumId = t.AlbumId
    JOIN InvoiceLine il ON t.TrackId = il.TrackId
    GROUP BY ar.ArtistId
    ORDER BY TotalRevenue DESC
""")

# B9: Best single month ever
run("Best month by revenue", """
    SELECT strftime('%Y-%m', InvoiceDate) as YearMonth,
           ROUND(SUM(Total), 2) as Revenue
    FROM Invoice
    GROUP BY YearMonth
    ORDER BY Revenue DESC
    LIMIT 1
""")

# B10: Avg revenue per customer by country
run("Avg revenue per customer by country", """
    SELECT Country,
           ROUND(AVG(CustomerTotal), 2) as AvgRevenuePerCustomer
    FROM (
        SELECT c.Country,
               SUM(i.Total) as CustomerTotal
        FROM Customer c
        JOIN Invoice i ON c.CustomerId = i.CustomerId
        GROUP BY c.CustomerId
    )
    GROUP BY Country
    ORDER BY AvgRevenuePerCustomer DESC
""")

conn.close()