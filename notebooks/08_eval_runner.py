import json
import sqlite3
import pandas as pd  # type: ignore
import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import SCHEMA, DB_PATH, chain
from src.sql_validator import validate_sql, clean_sql

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

# --- LOAD EVAL QUESTIONS ---
with open("data/eval_questions.json") as f:
    questions = json.load(f)

results = []
correct = 0
total = len(questions)

print(f"Running eval — {total} questions")
print(f"{'='*55}")

for q in questions:
    print(f"\nQ{q['id']} [{q['difficulty']}]: {q['question']}")
    generated_sql = ""
    status = "error"
    note = ""

    try:
        # Step 1: Generate SQL
        result = chain.invoke({"schema": SCHEMA, "question": q["question"]})
        generated_sql = clean_sql(result.content.strip())
        print(f"  SQL: {generated_sql[:80]}...")

        # Step 2: Validate
        is_valid, val_error = validate_sql(generated_sql)
        if not is_valid:
            status = "error"
            note = f"Validation: {val_error}"
            print(f"  ❌ {note}")
        else:
            # Step 3: Execute
            df, exec_error = run_sql(generated_sql)

            if exec_error:
                status = "error"
                note = f"Exec error: {exec_error}"
                print(f"  ❌ {note}")
            elif len(df) == q["expected_rows"]:
                status = "correct"
                note = ""
                correct += 1
                print(f"  ✅ Correct ({len(df)} rows)")
            else:
                status = "wrong_rows"
                note = f"Expected {q['expected_rows']} rows, got {len(df)}"
                print(f"  ⚠️ {note}")

    except Exception as e:
        if "429" in str(e):
            print(f"  ⏳ Rate limit — waiting 60s...")
            time.sleep(60)
            status = "rate_limit"
            note = "Daily quota hit"
        else:
            status = "error"
            note = str(e)
            print(f"  ❌ Error: {e}")

    results.append({
        "id": q["id"],
        "difficulty": q["difficulty"],
        "question": q["question"],
        "expected_rows": q["expected_rows"],
        "generated_sql": generated_sql,
        "status": status,
        "note": note
    })

    time.sleep(20)  # safer delay — stays under per-minute rate cap

# --- SUMMARY ---
print(f"\n{'='*55}")
print(f"EVAL RESULTS")
print(f"{'='*55}")
print(f"Total: {total} | Correct: {correct} | Accuracy: {correct/total*100:.1f}%")
print()

by_difficulty = {}
for r in results:
    d = r["difficulty"]
    if d not in by_difficulty:
        by_difficulty[d] = {"correct": 0, "total": 0}
    by_difficulty[d]["total"] += 1
    if r["status"] == "correct":
        by_difficulty[d]["correct"] += 1

for d, stats in by_difficulty.items():
    acc = stats["correct"] / stats["total"] * 100
    print(f"  {d}: {stats['correct']}/{stats['total']} ({acc:.1f}%)")

# --- FAILURES ---
failures = [r for r in results if r["status"] != "correct"]
if failures:
    print(f"\nFailures ({len(failures)}):")
    for f in failures:
        print(f"  Q{f['id']} [{f['difficulty']}]: {f['question']}")
        print(f"    → {f['status']}: {f['note']}")

# --- SAVE ---
with open("data/eval_results_v1.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"\nSaved to data/eval_results_v1.json")