from src.config import llm
result = llm.invoke("Say OK")
print(result.content)