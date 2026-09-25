from langchain_openai import ChatOpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL


def get_llm():
    return ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL,
        temperature=0
    )
