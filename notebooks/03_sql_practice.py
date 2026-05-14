import sqlite3
import pandas as pd

conn = sqlite3.connect("data/Chinook_Sqlite.sqlite")

def run(label, sql):
    print(f"\n{'='*50}")
    print(f"Q: {label}")
    print(f"{'='*50}")
    df = pd.read_sql(sql, conn)
    print(df.to_string())

# Query 1: Top 5 artists by number of albums
run("Top 5 artists by number of albums","""
    SELECT ar.Name, COUNT(al.AlbumId) as album_count
    FROM Artist ar
    JOIN Album al ON ar.ArtistId = al.ArtistId
    GROUP BY ar.ArtistId
    ORDER BY album_count DESC
    LIMIT 5
""")

# Query 2: Total revenue per country
run("Total revenue by country", """
    SELECT c.Country, ROUND(SUM(i.Total), 2) as revenue
    FROM Customer c
    JOIN Invoice i ON c.CustomerId = i.CustomerId
    GROUP BY c.Country
    ORDER BY revenue DESC
""")

# Query 3: Most popular genre by number of tracks sold
run("Most popular genre by tracks sold", """
    SELECT g.Name, COUNT(il.InvoiceLineId) as purchases
    FROM Genre g
    JOIN Track t ON g.GenreId = t.GenreId
    JOIN InvoiceLine il ON t.TrackId = il.TrackId
    GROUP BY g.GenreId
    ORDER BY purchases DESC
    LIMIT 5
""")

# Query 4: Employees and their managers
run("Employees and their managers", """
    SELECT e.FirstName || ' ' || e.LastName as Employee,
           e.Title,
           m.FirstName || ' ' || m.LastName as Manager
    FROM Employee e
    LEFT JOIN Employee m ON e.ReportsTo = m.EmployeeId
""")

# Query 5: Top 5 customers by total spending
run("Top 5 customers by spending", """
    SELECT c.FirstName || ' ' || c.LastName as Customer,
           c.Country,
           ROUND(SUM(i.Total), 2) as total_spent
    FROM Customer c
    JOIN Invoice i ON c.CustomerId = i.CustomerId
    GROUP BY c.CustomerId
    ORDER BY total_spent DESC
    LIMIT 5
""")

run("Names of customers","""
    select FirstName, LastName from customer
""")

conn.close()