from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model (
    "gemini-3.1-flash-lite-preview",
    model_provider="google_genai",
    temperature=0,
    max_tokens=30,
)

response = model.invoke("What is the capital of France?")

# clean output
if isinstance(response.content, list):
    response_content = response.content[0]["text"]
else:
    response_content = response.content

print(response_content)


# for second reponse about model class model provider




# from langchain.chatopenai import ChatOpenAI
# model = ChatOpenAI(model="gemini-3.1-flash-lite-preview", model_provider="google_genai")
# response = model.invoke("What is the capital of France?")