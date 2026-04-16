import os

from langchain_openai import ChatOpenAI
from app.core.config import settings

llm_qwen = ChatOpenAI(
    # model="qwen-max",
    # model="qwen3-235b-a22b",
    model=settings.DEFAULT_MODEL_NAME,
    base_url=settings.MODEL_BASE_URL,
    api_key=settings.BAILIAN_API_KEY,
    streaming=True,
)