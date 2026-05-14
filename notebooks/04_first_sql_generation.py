import sqlite3
import pandas as pd
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

# --- LLM SETUP ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# --- SCHEMA (what we tell the LLM about our DB) ---
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

# --- PROMPT TEMPLATE ---
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

# --- CHAIN ---
chain = sql_prompt | llm

# --- EXECUTE SQL ---
def run_sql(sql):
    try:
        conn = sqlite3.connect("data/Chinook_Sqlite.sqlite")
        df = pd.read_sql(sql, conn)
        conn.close()
        return df
    except Exception as e:
        return f"ERROR: {e}"

# --- ASK FUNCTION ---
def ask(question):
    print(f"\n{'='*55}")
    print(f"Q: {question}")
    print(f"{'='*55}")

    # Step 1: Generate SQL
    result = chain.invoke({"schema": SCHEMA, "question": question})
    sql = result.content.strip()
    print(f"Generated SQL:\n{sql}")

    # Step 2: Execute
    print(f"\nResult:")
    output = run_sql(sql)
    print(output)

# --- TEST 5 QUESTIONS ---
ask("Who are the top 5 artists by number of albums?")
ask("What is the total revenue by country?")
ask("Which genre has the most tracks sold?")
ask("Who is the customer who spent the most money?")
ask("How many tracks are in each playlist?")