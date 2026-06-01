import sqlite3

def extract_schema(db_path: str) -> str:
    """
    Automatically extracts schema from a SQLite database.
    Returns a formatted string describing all tables,
    columns, data types, and foreign keys.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    schema_parts = []

    for table in tables:
        # Get column info
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        # Each row: (cid, name, type, notnull, default, pk)

        col_descriptions = []
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            is_pk = " (PRIMARY KEY)" if col[5] else ""
            col_descriptions.append(f"  - {col_name}: {col_type}{is_pk}")

        # Get foreign keys
        cursor.execute(f"PRAGMA foreign_key_list({table})")
        fks = cursor.fetchall()
        fk_descriptions = []
        for fk in fks:
            fk_descriptions.append(f"  - {fk[3]} → {fk[2]}.{fk[4]}")

        table_desc = f"Table: {table}\nColumns:\n"
        table_desc += "\n".join(col_descriptions)
        if fk_descriptions:
            table_desc += "\nForeign Keys:\n"
            table_desc += "\n".join(fk_descriptions)

        schema_parts.append(table_desc)

    conn.close()
    return "\n\n".join(schema_parts)


if __name__ == "__main__":
    schema = extract_schema("data/Chinook_Sqlite.sqlite")
    print(schema)
    print(f"\n--- Schema length: {len(schema)} characters ---")