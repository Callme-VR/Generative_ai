import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

text = [
    "What is the capital of France?",
    "What is the capital of India?"
]

vectors = embedding.embed_documents(text)

print(vectors)