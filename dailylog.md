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