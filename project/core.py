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


para = input("give your Paragraph: ")


final_output = prompt.invoke(
    {
        "paragraph": para,
        "format_instructions": parser.get_format_instructions()
    }
)


response = model.invoke(final_output)

movies_data = parser.parse(response.content)

print(movies_data)


response = model.invoke("Hello, how are you?")
print(response.content)
