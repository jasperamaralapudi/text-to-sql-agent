import os
from dotenv import load_dotenv #type:ignore
from langchain_google_genai import ChatGoogleGenerativeAI #type:ignore
from langchain_core.prompts import PromptTemplate #type:ignore
from src.schema_extractor import extract_schema

load_dotenv()

# --- PATHS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "Chinook_Sqlite.sqlite")

# --- AUTO SCHEMA ---
SCHEMA = extract_schema(DB_PATH)

# --- LLM ---
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

# --- CHAIN ---
chain = sql_prompt | llm