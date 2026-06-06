from langchain_core.prompts import PromptTemplate #type:ignore

fix_prompt = PromptTemplate(
    input_variables=["schema", "question", "bad_sql", "error"],
    template="""You are a SQLite SQL expert.
The following SQL query failed with an error.
Fix the SQL so it correctly answers the question.
Return ONLY the fixed SQL. No explanation. No markdown. No backticks.

Schema:
{schema}

Question: {question}

Failed SQL:
{bad_sql}

Error message:
{error}

Fixed SQL:"""
)


def fix_sql(llm, schema: str, question: str, bad_sql: str, error: str) -> str:
    """
    Asks the LLM to fix a failed SQL query.
    Returns fixed SQL string.
    """
    chain = fix_prompt | llm
    result = chain.invoke({
        "schema": schema,
        "question": question,
        "bad_sql": bad_sql,
        "error": error
    })
    return result.content.strip()


if __name__ == "__main__":
    import os
    import time
    from dotenv import load_dotenv #type:ignore
    from src.config import SCHEMA, llm
    from src.sql_validator import clean_sql

    load_dotenv()

    # Test cases — deliberately broken SQL
    tests = [
        {
            "question": "How many artists are there?",
            "bad_sql": "SELECT COUTN(*) FROM Artist",
            "error": "no such function: COUTN"
        },
        {
            "question": "List all customers from Germany",
            "bad_sql": "SELECT FirstName, LastName FROM Customers WHERE Country = 'Germany'",
            "error": "no such table: Customers"
        },
        {
            "question": "What is the total revenue?",
            "bad_sql": "SELECT SUM(Amount) FROM Invoice",
            "error": "no such column: Amount"
        },
    ]

    print("Testing sql_fixer.py — self-healing SQL\n")
    for i, test in enumerate(tests):
        print(f"Test {i+1}: {test['question']}")
        print(f"  Bad SQL:  {test['bad_sql']}")
        print(f"  Error:    {test['error']}")

        fixed = fix_sql(
            llm=llm,
            schema=SCHEMA,
            question=test["question"],
            bad_sql=test["bad_sql"],
            error=test["error"]
        )
        fixed = clean_sql(fixed)
        print(f"  Fixed SQL: {fixed}")
        print()
        time.sleep(15)

    print("Done!")