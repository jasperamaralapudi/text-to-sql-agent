## DAY 1
 - Did: Installed conda and all libraries, created repo on github,  created folder structure in vs code
 - Broke: Nothing
 - Tomorrow: Run LLM

## Day 2
- Did: Tried to run OpenAI API but it was 5$, so switched to Gemini API, ran gemini-2.5-flash, called gemini succesfully, good response
- Broke: gemini-2.0-flash quota issue on free tier, switched to gemini-2.5-flash
- Tomorrow: Download Chinook DB, explore all 11 tables in Python, write 5 SQL queries by hand

## Day: 3
- Did: Downloaded Chinook DB, ran 5 SQL queries successfully
- Broke: Didn't understand how queries must run, tried to learn
- Key learning: 3-table joins (Genre→Track→InvoiceLine), self-join on Employee table
- Tomorrow: First LangChain call — PromptTemplate + make LLM generate SQL

## Day 4
- Did: Built PromptTemplate chain, Gemini generating SQL from plain English
- Works: 4/5 questions perfectly correct
- Issue: Playlist query returns duplicates — data quality problem in DB
- Key learning: Relationships in schema prompt are critical for JOIN accuracy
- Tomorrow: Read LangChain agents docs, understand ReAct loop