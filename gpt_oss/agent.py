import os
from typing import List, Dict, Any
import time
import concurrent.futures as cf
import streamlit as st
from groq import Groq, GroqError
from dotenv import load_dotenv

load_dotenv()


MODEL = "openai/gpt-oss-120b"
MAX_COMPLETION_TOKENS = 1024  # stay within the groq api keys limits
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SAMPLE_PROMPTS = [
    "Explain how to implement a binary search tree in Python.",
    "What are the best practices for API design?",
    "How would you optimize a slow database query?",
    "Explain the concept of recursion with examples.",
]

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found in environment variables")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# helper function


def One_Completions(client: Groq, message: List[Dict[str, str]], temperature: float) -> str:
    """single non-streaming completions with basic retries"""
    delay = 0.5

    retries = 3
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=message,
                temperature=temperature,
                max_completion_tokens=MAX_COMPLETION_TOKENS,
                top_p=1,
                stream=False,
            )
            return response.choices[0].message.content
        except GroqError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == 2:
                raise
            time.sleep(delay)
            delay *= 2


# helper function for the intial answer by using the models


def Generate_intial_answer(client: Groq, prompt: str) -> str:
    """generate intial answer using the models"""
    candidates = []
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        futures = [
            ex.submit(
                One_Completions,
                client,
                [{"role": "user", "content": prompt}],
                0.9,
            )
            for _ in range(3)
        ]
        for fut in cf.as_completed(futures):
            candidates.append(fut.result())

    # sythezsize the candidates
    candidates_text = []
    for i, c in enumerate(candidates):
        candidates_text.append(f"Candidate {i+1}:\n{c}")

    synthesize_prompt = (
        f"You are given 3 candidates. synthesize them into one best answer, "
        f"eliminating repetitions and ensuring coherence:\n\n"
        f"{chr(10).join(candidates_text)}\n\n"
        f"return the single best final answer with more accurate ways"
    )
    return One_Completions(client, [{"role": "user", "content": synthesize_prompt}], 0.2)


# for the Revise the answer and For better improvement of the models

def Revise_answer(client: Groq, prompt: str, answer: str) -> str:
    """Have a critic model identify flaws and missing pieces"""
    critic_prompt = (
        f"Original Questions: {prompt}\n\n"
        f"Answer To Critique:\n{answer}\n\n"
        f"Act as a critical reviewer. List specific flaws, missing information, "
        f"unclear explanations or areas that need improvement. "
        f"Be consistent and constructive but thorough. "
        f"Format as bullet point list starting with >>"
    )

    return One_Completions(client, [{"role": "user", "content": critic_prompt}], 0.3)
