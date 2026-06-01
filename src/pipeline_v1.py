import sqlite3
import pandas as pd #type:ignore
import os
from dotenv import load_dotenv #type:ignore
from langchain_google_genai import ChatGoogleGenerativeAI #type:ignore
from langchain_core.prompts import PromptTemplate #type:ignore

load_dotenv()

# --- CONFIG ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "Chinook_Sqlite.sqlite")

SCHEMA = """
Tables:
- Artist(ArtistId, Name)
- Album(AlbumId, Title, ArtistId)
- Track(TrackId, Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice)
- Genre(GenreId, Name)
- MediaType(MediaTypeId, Name)
- Playlist(PlaylistId, Name)
- PlaylistTrack(PlaylistId, TrackId)
- Invoice(InvoiceId, CustomerId, InvoiceDate, BillingAddress, BillingCity, BillingState, BillingCountry, BillingPostalCode, Total)
- InvoiceLine(InvoiceLineId, InvoiceId, TrackId, UnitPrice, Quantity)
- Customer(CustomerId, FirstName, LastName, Company, Address, City, State, Country, PostalCode, Phone, Fax, Email, SupportRepId)
- Employee(EmployeeId, LastName, FirstName, Title, ReportsTo, BirthDate, HireDate, Address, City, State, Country, PostalCode, Phone, Fax, Email)

Relationships:
- Album.ArtistId → Artist.ArtistId
- Track.AlbumId → Album.AlbumId
- Track.GenreId → Genre.GenreId
- Track.MediaTypeId → MediaType.MediaTypeId
- InvoiceLine.TrackId → Track.TrackId
- InvoiceLine.InvoiceId → Invoice.InvoiceId
- Invoice.CustomerId → Customer.CustomerId
- Customer.SupportRepId → Employee.EmployeeId
- Employee.ReportsTo → Employee.EmployeeId
- PlaylistTrack.PlaylistId → Playlist.PlaylistId
- PlaylistTrack.TrackId → Track.TrackId
"""

# --- LLM SETUP ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# --- PROMPT ---
sql_prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template="""You are a SQLite SQL expert.
Given the schema below, write a SQL query to answer the question.
Return ONLY the raw SQL. No explanation. No markdown. No backticks.

Schema:
{schema}

Question: {question}

SQL:"""
)

chain = sql_prompt | llm

# --- EXECUTE SQL ---
def run_sql(sql):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql(sql, conn)
        conn.close()
        return df, None
    except Exception as e:
        return None, str(e)

# --- ASK FUNCTION — no error handling, no retry, no clean columns ---
def ask(question):
    print(f"\n{'='*55}")
    print(f"Question: {question}")
    print(f"{'='*55}")

    # Step 1: Generate SQL — no try/except, crashes on any error
    result = chain.invoke({"schema": SCHEMA, "question": question})
    sql = result.content.strip()
    tokens_used = (
        result.usage_metadata["input_tokens"] +
        result.usage_metadata["output_tokens"]
    )

    print(f"\nGenerated SQL:\n{sql}")
    print(f"Tokens used: {tokens_used}")

    # Step 2: Execute SQL
    df, error = run_sql(sql)

    if error:
        # No friendly message — just prints raw error
        print(f"SQL Error: {error}")
        return

    # Step 3: Print results — no column cleaning
    print(f"\nResult ({len(df)} rows):")
    print(df.to_string())

# --- TEST ---
if __name__ == "__main__":
    questions = [
        "Who are the top 5 artists by number of albums?",
        "What is the total revenue by country?",
        "Which customer has spent the most money?",
        "How many tracks are in each genre?",
        "Show me all employees and who they report to",
        "What percentage of total revenue comes from the USA?",
        "Which album has the most tracks?"
    ]

    for q in questions:
        ask(q)
        # No time.sleep — will crash on 429 after question 5

    print(f"\n{'='*55}")
    print("Pipeline v1 complete.")
    print(f"{'='*55}")