from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()
llm  =ChatGroq(
    api_key=os.getenv("GROK_API_KEY1"),
    model="llama-3.1-8b-instant")

if __name__ == "__main__":
    print("LLM initialized successfully.")
    # You can add more functionality here to interact with the LLM or process data. 
    response = llm.invoke("What is the capital of France?")
    print(response.content)