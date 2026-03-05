import os
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI

load_dotenv()

model = ChatMistralAI(
    model="ministral-8b-latest",
    temperature=0,
    max_tokens=30,
)

response = model.invoke("What is the capital of India?")

print(response.content)