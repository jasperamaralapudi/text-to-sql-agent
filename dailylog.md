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

## Day 5
- Did: Read and understood about agents, tools and chains in official documentation, watched a youtube video about ReAct AI Agents(5 mins)
- Broke: Got confused about the configuraion of agents and tools, also difference between agents and chains
- Key Learnings: 
- Agents: Agents are AI systems that autonomously plan, reason, and take actions using tools to achieve a goal
- Tools: Tools are external systems or functions that help AI agents to fetch real world data beyond it's trained data or built-in knowledge. In LangChain, tools are wrapped functions that the agent can invoke dynamically according to user query. E.g.: Calling weather APIs, calculations, code execution, SQL tools
- Chains: A Chain is a predefined workflow where the output of the current prompt becomes the input of next prompt to achieve a task step by step. User input -> Prompt Template -> LLM -> Output Parser -> Final Response
- Difference between agents and chains: Chains are predefined workflows, while agents dynamically decide which actions/tools to use based on the situations. If workflow is known beforehand , chains are better. Agents are useful when system needs autonomy and decision-making.
- ReAct Loop: The ReAct loop is an agent reasoning pattern where the LLM alternates between reasoning and taking actions until it reaches a final answer. ReAct loop isn't an agent but a reasoning strategy used by agents.
- In THIS project, what will the "tool" be? : IN Text-to-SQL Project the tool will be query execution tool that allows agents to run SQL queries on a database
- When a user asks "who is the top customer?", what does the agent do step by step? : User query -> Reason: Understand query and plan how to do it. -> Act: Run SQL query on the database ->  Observe: Get the answer -> Reason: Have I got the answer, if no go to action again, if yes give output. -> Final Answer
- Tomorrow: Build pipeline_v1.py, first end-to-end working script.

## Week 1 Wrap-up
- Built: End-to-end pipeline — question → Gemini → SQL → SQLite → results
- Works well: Simple queries, JOINs, aggregations, self-joins, percentage calc
- Issues noted: Rate limit 5 req/min on free tier, ugly column name on Q6
- Key learning: Schema + relationships in prompt = accurate JOIN generation
- Next week (Week 2): Deep dive Chinook, write 20 SQL queries, 
  understand RAG concept before building it

  ## Day 8 — 25 May, 2026
- Did: 11 SQL queries including nested subquery in HAVING, ROW_NUMBER window function
- Key insight: Q10a vs Q10b handle ties differently — subquery returns all ties, ROW_NUMBER picks one
- Bug noted: Q2 alias in WHERE — should use Milliseconds >= 300000 directly
- Tomorrow: 10 business queries + read vanna-ai GitHub repo

## Day 9- 29 May, 2026
- Did: Ran 10 Business Queries and read github vanna.ai readme
- Broke: Had no time , so copied queries from Claude, but learned what I did
- Key Learnings:
  1. **What it does:** Vanna is an open-source text-to-SQL framework that converts natural-language questions into SQL using a RAG-style approach: it retrieves relevant schema, documentation, and past question→SQL examples, then feeds them to an LLM to generate queries. Recent Vanna 2.0 also adds user-aware permissions, streaming tables/charts, and a production-ready chat interface. ([GitHub][1])

  2. **How it differs from my pipeline:** If your pipeline is the typical *schema → prompt → LLM → SQL* flow, Vanna is more retrieval-centric. It stores DDL, documentation, and successful query examples in a vector store and retrieves them at inference time rather than relying mainly on a static prompt. Vanna 2.0 also treats text-to-SQL as part of a broader agent system with permissions, tools, memory, and UI components. 

  3. **What I'd borrow from it:** I would borrow its retrieval strategy—especially storing validated question→SQL pairs and business documentation as reusable context—plus its idea of learning from successful interactions over time ("tool memory"). Those two features are likely to improve SQL accuracy more than simply using a larger model. 
- Tomorrow: Schema Documentation - RAG knowledge database

## Day 10 — 29 May, 2026
- Did: Wrote rich schema documentation for all 11 Chinook tables
- Key insight: 
  1. InvoiceLine is the most important table for revenue queries -
    Revenue = UnitPrice * Quantity. Everything traces back through here.
  2. PlaylistTrack is a pure junction table - no extra columns, 
    just links. Important to note so LLM doesn't try to SELECT non-existent columns.
  3. Employee.ReportsTo is a self-reference - need LEFT JOIN same 
    table twice for manager queries.
- Tomorrow: RAG concepts - embeddings, FAISS, ChromaDB. Reading + video, no code.

## Day 11 — RAG + FAISS + ChromaDB concepts

1. What is an embedding?\
   Text embeddings are numerical representation vectors of a text that allows computers to find 
   similar text even when exact words differ. Similar texts are near, different texts are apart. The vector dimensions are fixed (e.g. Gemini embeddings = 768 numbers). Every piece of text, regardless of length, becomes the same size vector.

2. What is similarity search?\
   Similarity search is the process of finding stored vectors that are similar to query vectors.

3. How does RAG work? (step by step in own words)\
   user question -> embedding -> similarity search in vectordb -> retrieve schema docs -> build prompt -> LLM gives SQL -> Runs it on database -> returns results

4. FAISS vs ChromaDB — one key difference?\
   ChromaDB is a vector database while faiss is a vector search framework. FAISS lives in memory (lost on restart), ChromaDB saves to disk (survives restarts).

5. How will RAG help MY Text-to-SQL project specifically?
   [think: what happens when a DB has 50 tables -
   you can't dump the full schema every time]\
   When a DB has many tables, if we retrieve every schema doc it wastes the tokens and canconfuse the model. RAG helps retrieve relavant docs, relationships, information which allows LLM to generate accurate SQL.

## Day 12 
- Did: 
  - Created eval_questions.json with 20 verified question-SQL pairs
  - Distribution: 8 simple, 7 medium, 5 hard
  - These become the foundation of the 100-question eval set in Week 6
- Tomorrow: Fix pipeline_v1 - rate limiting + clean column names

## Week 2 Wrap-up
- SQL skills: subqueries, HAVING, CASE WHEN, ROW_NUMBER, 3-table JOINs
- RAG understood: embeddings → similarity search → retrieve → prompt → LLM
- FAISS = in-memory, ChromaDB = persistent
- schema_docs.md ready to become RAG vector store in Week 5
- eval_questions.json: 20 verified pairs - foundation of Week 6 evaluation
- pipeline_v2: no more crashes, clean output
- Next week (Week 3): Build the real LangChain SQL agent

## WEEK 3 - Day 1
- Did: Built auto schema extractor (src/schema_extractor.py) using SQLite PRAGMA commands
- How it works: PRAGMA table_info() reads column names, types, primary keys. PRAGMA foreign_key_list() reads foreign key relationships. Loops through all tables and builds a formatted string.
- Output: 2511 characters describing all 11 Chinook tables with data types and FK relationships
- Key insights: 
  - PRAGMA commands are SQLite's built-in way to read DB metadata — no manual schema writing needed
  - Data types (NVARCHAR, NUMERIC, DATETIME) are now included — helps LLM write more type-aware SQL
  - Works on ANY SQLite DB — drop in a different database, schema auto-detected in seconds
  - Also restored pipeline_v1.py to original basic version — no retry, no clean columns — serves as clean historical reference
  - Comparison: v1 (basic) → v2 (retry + clean columns) → v3 (auto schema + validation + self-healing) — clear progression
- Tomorrow: Create src/config.py to remove code duplication across pipeline files, then plug auto-schema in

## WEEK 3 - Day 2
- Did: Created src/config.py — centralised DB path, LLM, prompt, chain. No more duplication across pipeline files.
- Did: Tested auto-schema on 5 questions — all 5 correct, identical results to pipeline_v2
- Finding: Auto-schema uses ~1000-1200 tokens vs ~550-650 for hardcoded schema (roughly 2x)
- Reason: Auto-schema includes data types and FK details — more context for LLM
- Key insight: This token tradeoff is exactly what RAG solves in Week 5 — retrieve only relevant tables instead of full schema
- Tomorrow: sql_validator.py — safety checks + sqlparse validation before any SQL executes

## WEEK 3 - Day 3
- Did: Built sql_validator.py — two layers of protection before any SQL executes
- Layer 1: Keyword blocklist — catches DROP, DELETE, UPDATE, INSERT, ALTER, TRUNCATE, CREATE, REPLACE
- Layer 2: sqlparse type check — confirms query is SELECT only
- Also built clean_sql() — strips markdown backticks LLMs sometimes wrap SQL in
- Key insight: Test 7 caught SQL injection pattern — valid SELECT followed by DROP TABLE. Blocklist scans the full string so it catches this even after a valid SELECT.
- Key insight: clean_sql() is important — Gemini sometimes returns ```sql blocks even when told not to```
- Tomorrow: sql_fixer.py — feed failed SQL + error back to LLM for auto-correction

## WEEK 3 - Day 4
- Did: Built sql_fixer.py — feeds failed SQL + error message back to LLM for auto-correction
- Test 1: Typo in function name (COUTN → COUNT) — fixed
- Test 2: Wrong table name (Customers → Customer) — fixed
- Test 3: Wrong column name (Amount → Total) — fixed
- Key insight: The error message gives the LLM exact context to fix the query — "no such column: Amount" tells it precisely what's wrong
- Key insight: Must run with python -m src.sql_fixer from project root, not python src/sql_fixer.py — otherwise Python can't resolve src imports
- Tomorrow: Run all 20 eval questions, score accuracy by difficulty, save results to eval_results_v1.json

## WEEK 3 - Day 5
- Did: Full eval run completed — 15/20 correct, 75% accuracy
- Breakdown: simple 87.5%, medium 71.4%, hard 60.0%
- Failure Pattern 1 (3 failures — Q9, Q12, Q17): "most X" interpreted as LIMIT 1 
  instead of full ranking. Confirmed same root cause across all 3.
  → Fix: prompt-level instruction to return full ranking unless "top N" specified
- Failure Pattern 2 (2 failures — Q8, Q19): Aggregation/join logic errors
  → Q8: missing HAVING COUNT > 5, returned ungrouped rows
  → Q19: INNER JOIN excluded artists with zero sales — should be LEFT JOIN
  → Fix: needs few-shot examples in Week 5 RAG, not just prompt wording
- 75% accuracy is now the baseline number for pipeline_v1. Target for Week 5 
  RAG + few-shot: 85%+
- Tomorrow: Build pipeline_v3.py combining schema_extractor + sql_validator + sql_fixer

## WEEK 3 - Day 6
- Did: Built pipeline_v3.py — combines auto schema + sql_validator + sql_fixer + rate limit retry
- Verified: 2/2 questions correct before quota exhausted
- Issue: 20/day limit means can't run eval (20 req) + pipeline test on same day
- Fix: Create second API key for backup quota
- Week 3 complete — all modules built and working

## Week 3 Wrap-up
- schema_extractor.py: auto schema from any SQLite DB via PRAGMA
- config.py: centralised setup — no more duplication
- sql_validator.py: safety blocklist + sqlparse check, 7/7 tests passed
- sql_fixer.py: self-healing SQL, 3/3 broken queries auto-corrected
- eval results: 75% accuracy baseline (simple 87.5%, medium 71.4%, hard 60%)
- pipeline_v3.py: all modules combined into production-grade pipeline
- Known failure patterns: "most X" → LIMIT 1, aggregation grouping errors
- Next week: LangChain SQL Agent + conversation memory