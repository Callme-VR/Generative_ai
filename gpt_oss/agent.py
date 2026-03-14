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
            if attempt == retries - 1:
                raise
            time.sleep(delay)
            delay *= 2


# helper function for the initial answer using multiple model calls
def Generate_intial_answer(client: Groq, prompt: str) -> str:
    """generate initial answer using multiple parallel completions"""
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

    candidates_text = []
    for i, c in enumerate(candidates):
        candidates_text.append(f"Candidate {i+1}:\n{c}")

    synthesize_prompt = (
        f"You are given 3 candidates. Synthesize them into one best answer, "
        f"eliminating repetitions and ensuring coherence:\n\n"
        f"{chr(10).join(candidates_text)}\n\n"
        f"Return the single best final answer."
    )

    return One_Completions(client, [{"role": "user", "content": synthesize_prompt}], 0.2)


# critic function
def Revise_critics(client: Groq, prompt: str, answer: str) -> str:
    """Have a critic model identify flaws and missing pieces"""

    critic_prompt = (
        f"Original Question: {prompt}\n\n"
        f"Answer To Critique:\n{answer}\n\n"
        f"Act as a critical reviewer. List specific flaws, missing information, "
        f"unclear explanations, or areas that need improvement.\n"
        f"Format as bullet points starting with >>"
    )

    return One_Completions(client, [{"role": "user", "content": critic_prompt}], 0.3)


# revise the answer
def Revise_answer(client: Groq, prompt: str, original_answer: str, critiques: str) -> str:
    """Revise the original answer addressing all critiques"""

    revision_prompt = (
        f"Original question:\n{prompt}\n\n"
        f"Original answer:\n{original_answer}\n\n"
        f"Critiques to address:\n{critiques}\n\n"
        f"Revise the answer to address every critique point. "
        f"Maintain good parts and improve weak areas."
    )

    return One_Completions(client, [{"role": "user", "content": revision_prompt}], 0.2)


# critical improvement loop
def Critical_improvement_loop(
    prompt: str,
    max_iteration: int = 2,
    Groq_api_key: str | None = None,
) -> Dict[str, Any]:

    client_local = Groq(api_key=Groq_api_key or GROQ_API_KEY)

    result: Dict[str, Any] = {
        "iterations": [],
        "Final_answers": "",
        "Total_iterations": 0,
    }

    with st.spinner("Generating initial answer..."):
        initial_answer = Generate_intial_answer(client_local, prompt)

    result["iterations"].append(
        {
            "answer": initial_answer,
            "critiques": None,
            "type": "initial",
        }
    )

    current_answer = initial_answer

    for iteration in range(max_iteration):

        with st.spinner(f"Critiquing iteration {iteration + 1}..."):
            critiques = Revise_critics(client_local, prompt, current_answer)

        with st.spinner(f"Revising iteration {iteration + 1}..."):
            revised_answer = Revise_answer(
                client_local,
                prompt,
                current_answer,
                critiques,
            )

        result["iterations"].append(
            {
                "answer": revised_answer,
                "critiques": critiques,
                "type": f"iteration_{iteration + 1}",
            }
        )

        current_answer = revised_answer

    result["Final_answers"] = current_answer
    result["Total_iterations"] = max_iteration

    return result
