import sqlite3
import pandas as pd # type: ignore
import os

db_path="data/Chinook_Sqlite.sqlite"
output_folder="chinook_csv"
os.makedirs(output_folder,exist_ok=True)

conn=sqlite3.connect(db_path)
cursor=conn.cursor()

cursor.execute("select name from sqlite_master where type='table';")
tables=cursor.fetchall()

for table_name in tables:
    table=table_name[0]
    print(f"Exploring {table}...")
    df=pd.read_sql_query(f"select * from `{table}`",conn)
    df.to_csv(f"{output_folder}/{table}.csv",index=False)

conn.close()
print("Done")