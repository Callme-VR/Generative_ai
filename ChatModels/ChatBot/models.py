import os
from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage



model = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0
)

messages = []

# short term memory chatbot with append the old  and response of the chat in the list and pass the list to the model to get the response with the history of the chat


print("________________ CHATBOT WITH HISTORY ________________")

while True:
    prompt = input("User : ")

    if prompt == "0":
        break

    messages.append(HumanMessage(content=prompt))

    response = model.invoke(messages)

    messages.append(AIMessage(content=response.content))

    print("Bot 🤖:", response.content)

print(messages)