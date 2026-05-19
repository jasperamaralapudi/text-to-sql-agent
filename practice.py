from dotenv import load_dotenv # type: ignore
from langchain_google_genai import ChatGoogleGenerativeAI # type: ignore
import os
load_dotenv()
llm=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
response=llm.invoke("Say hello in one!")
print(type(response))
response = llm.invoke("Say hello in one sentence.")
print("Content:", response.content)
print("Input tokens:", response.usage_metadata["input_tokens"])
print("Output tokens:", response.usage_metadata["output_tokens"])
print("Finish reason:", response.response_metadata.get("finish_reason"))