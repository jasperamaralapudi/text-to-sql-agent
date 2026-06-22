import sqlite3
import pandas as pd  # type: ignore
import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import DB_PATH, SCHEMA, chain, llm
from src.sql_validator import validate_sql, clean_sql
from src.sql_fixer import fix_sql

# --- HELPERS ---
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

# --- MAIN ASK FUNCTION ---
def ask(question, retry=True):
    print(f"\n{'='*55}")
    print(f"Question: {question}")
    print(f"{'='*55}")

    try:
        # Step 1: Generate SQL
        result = chain.invoke({"schema": SCHEMA, "question": question})
        sql = clean_sql(result.content.strip())
        tokens_used = (
            result.usage_metadata["input_tokens"] +
            result.usage_metadata["output_tokens"]
        )
        print(f"\nGenerated SQL:\n{sql}")
        print(f"Tokens used: {tokens_used}")

        # Step 2: Validate SQL — safety + syntax check
        is_valid, val_error = validate_sql(sql)
        if not is_valid:
            print(f" Validation failed: {val_error}")
            return

        # Step 3: Execute SQL
        df, exec_error = run_sql(sql)

        # Step 4: If execution fails — auto-fix and retry once
        if exec_error:
            print(f" Execution error: {exec_error}")
            print(" Attempting auto-fix...")
            time.sleep(12)

            fixed_sql = fix_sql(
                llm=llm,
                schema=SCHEMA,
                question=question,
                bad_sql=sql,
                error=exec_error
            )
            fixed_sql = clean_sql(fixed_sql)
            print(f"Fixed SQL:\n{fixed_sql}")

            df, exec_error2 = run_sql(fixed_sql)
            if exec_error2:
                print(f" Still failed after fix: {exec_error2}")
                return

        # Step 5: Show results
        print(f"\n Result ({len(df)} rows):")
        print(df.to_string())

    except Exception as e:
        if "429" in str(e) and retry:
            print(f" Rate limit — waiting 30s...")
            time.sleep(30)
            return ask(question, retry=False)
        else:
            print(f" Error: {e}")

# --- TEST ---
if __name__ == "__main__":
    questions = [
        "Who are the top 5 artists by number of albums?",
        "Which customer has spent the most money?",
        "What is the total revenue by country?",
        "Show me all employees and who they report to",
        "Which album has the most tracks?"
    ]

    for q in questions:
        ask(q)
        time.sleep(20)

    print(f"\n{'='*55}")
    print("Pipeline v3 complete.")
    print(f"{'='*55}")