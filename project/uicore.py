import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser

import os
from dotenv import load_dotenv
load_dotenv()


model = ChatMistralAI(
    model="mistral-small-2506"
)


class Movies(BaseModel):
    title: str
    release_yr: Optional[int]
    Rating: Optional[float]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    summary: Optional[str]


parser = PydanticOutputParser(pydantic_object=Movies)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "extract movies information from the Graph {format_instructions}"
        ),
        (
            "human",
            "{paragraph}"
        )
    ]
)


st.title("Movie Information Extractor")


if "paragraph" not in st.session_state:
    st.session_state.paragraph = ""


paragraph = st.text_area(
    "Enter Movie Paragraph",
    value=st.session_state.paragraph,
    height=250
)


col1, col2 = st.columns(2)

with col1:
    extract = st.button("Extract")

with col2:
    reset = st.button("Reset")


if extract:

    final_output = prompt.invoke(
        {
            "paragraph": paragraph,
            "format_instructions": parser.get_format_instructions()
        }
    )

    response = model.invoke(final_output)

    movies_data = parser.parse(response.content)

    st.write(movies_data)


if reset:
    st.session_state.paragraph = ""
    st.rerun()
