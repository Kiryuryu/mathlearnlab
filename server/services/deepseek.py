"""
Unified DeepSeek (OpenAI-compatible) client.
Single place for base_url, default model, and client construction.
"""

from openai import AsyncOpenAI
from server.config import settings

BASE_URL = "https://api.deepseek.com"


def get_client(api_key: str | None = None) -> AsyncOpenAI:
    """Build a DeepSeek AsyncOpenAI client using the provided key or settings default."""
    key = api_key or settings.deepseek_api_key
    return AsyncOpenAI(api_key=key, base_url=BASE_URL)


async def chat_completion(messages: list[dict], *, api_key: str | None = None,
                          model: str | None = None, max_tokens: int | None = None):
    """Perform a single (non-streaming) chat completion against DeepSeek."""
    client = get_client(api_key)
    return await client.chat.completions.create(
        model=model or settings.deepseek_model,
        messages=messages,
        max_tokens=max_tokens,
    )


async def stream_chat(messages: list[dict], *, api_key: str | None = None,
                      model: str | None = None, max_tokens: int | None = None):
    """Open a streaming chat completion against DeepSeek."""
    client = get_client(api_key)
    return await client.chat.completions.create(
        model=model or settings.deepseek_model,
        messages=messages,
        max_tokens=max_tokens,
        stream=True,
    )
