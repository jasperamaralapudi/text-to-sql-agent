import sqlparse #type:ignore

# Dangerous operations to block
BLOCKED_KEYWORDS = [
    "DROP", "DELETE", "UPDATE", "INSERT",
    "ALTER", "TRUNCATE", "CREATE", "REPLACE"
]

def clean_sql(sql: str) -> str:
    """
    Cleans LLM output — removes markdown code blocks,
    extra whitespace, and backticks.
    """
    sql = sql.replace("```sql", "").replace("```", "")
    sql = sql.strip()
    return sql


def validate_sql(sql: str) -> tuple[bool, str]:
    """
    Validates SQL before execution.
    Returns (is_valid, error_message).
    """
    if not sql or not sql.strip():
        return False, "Empty SQL returned by LLM"

    # Safety check — block destructive operations
    sql_upper = sql.upper()
    for keyword in BLOCKED_KEYWORDS:
        if keyword in sql_upper:
            return False, f"Blocked: SQL contains {keyword} — only SELECT is allowed"

    # Parse and check it's a SELECT
    parsed = sqlparse.parse(sql)
    if not parsed:
        return False, "Could not parse SQL"

    first_type = parsed[0].get_type()
    if first_type != "SELECT":
        return False, f"Only SELECT queries allowed, got: {first_type}"

    return True, ""


if __name__ == "__main__":
    tests = [
        ("SELECT * FROM Artist", True),
        ("DROP TABLE Artist", False),
        ("DELETE FROM Customer WHERE 1=1", False),
        ("ALTER TABLE Track ADD COLUMN test TEXT", False),
        ("```sql\nSELECT Name FROM Artist\n```", True),
        ("", False),
        ("SELECT Name FROM Artist; DROP TABLE Artist", False),
    ]

    print("Running validation tests...\n")
    all_passed = True
    for sql, expected in tests:
        cleaned = clean_sql(sql)
        valid, msg = validate_sql(cleaned)
        status = "✅" if valid == expected else "❌ FAIL"
        if valid != expected:
            all_passed = False
        label = sql[:45].replace("\n", " ")
        print(f"{status} | expected={expected} got={valid} | '{label}'")
        if msg:
            print(f"       → {msg}")

    print(f"\n{'All tests passed ✅' if all_passed else 'Some tests failed ❌'}")