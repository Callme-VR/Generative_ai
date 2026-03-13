import os
from typing import List, Dict, Any
import time
import concurrent.futures as cf
import streamlit as st
from groq import Groq, GroqError


MODEL = "openai/gpt-oss-120b"
MAX_COMPLETION_TOKENS = 1024  # stay within the groq api keys limits
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found in environment variables")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# helper function


def One_Completions(client: Groq, message: List[dict[str, str]], temperature: float) -> str:
    "single non-Straming completions with basic Retries"
