import sqlite3
import pandas as pd

# Connect to Chinook DB
conn = sqlite3.connect("data/Chinook_Sqlite.sqlite")

# Step 1: List all tables
print("=" * 50)
print("ALL TABLES IN CHINOOK DATABASE")
print("=" * 50)
tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table'",
    conn
)
print(tables)

# Step 2: Explore each table
print("\n" + "=" * 50)
print("TABLE DETAILS")
print("=" * 50)

for table in tables['name']:
    print(f"\n--- {table} ---")
    df = pd.read_sql(f"SELECT * FROM {table} LIMIT 3", conn)
    print(f"Columns: {list(df.columns)}")
    print(f"Sample rows:")
    print(df.to_string())

conn.close()
print("\nDone.")