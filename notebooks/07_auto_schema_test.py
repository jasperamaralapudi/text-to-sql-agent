import sqlite3
import pandas as pd #type:ignore
import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import SCHEMA, DB_PATH, chain

print(f"Schema length: {len(SCHEMA)} characters")
print("="*55)

def clean_columns(df):
    new_cols = []
    for col in df.columns:
        if len(col) > 30:
            new_cols.append("result")
        else:
            new_cols.append(col)
    df.columns = new_cols
    return df

def run_sql(sql):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql(sql, conn)
        conn.close()
        df = clean_columns(df)
        return df, None
    except Exception as e:
        return None, str(e)

def ask(question):
    print(f"\nQ: {question}")
    try:
        result = chain.invoke({"schema": SCHEMA, "question": question})
        sql = result.content.strip()
        tokens = (
            result.usage_metadata["input_tokens"] +
            result.usage_metadata["output_tokens"]
        )
        print(f"SQL: {sql}")
        print(f"Tokens: {tokens}")
        df, error = run_sql(sql)
        if error:
            print(f"Error: {error}")
        else:
            print(f"Result ({len(df)} rows):")
            print(df.to_string())
    except Exception as e:
        if "429" in str(e):
            print("Rate limit — waiting 30s...")
            time.sleep(30)
            ask(question)
        else:
            print(f"Error: {e}")

# Same 5 questions from pipeline_v2 for direct comparison
questions = [
    "Who are the top 5 artists by number of albums?",
    "Which customer has spent the most money?",
    "How many tracks are in each genre?",
    "What percentage of total revenue comes from the USA?",
    "Which album has the most tracks?"
]

for q in questions:
    ask(q)
    time.sleep(15)

print("\n" + "="*55)
print("Auto-schema test complete.")
print("="*55)