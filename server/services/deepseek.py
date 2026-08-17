"""
Unified DeepSeek (OpenAI-compatible) client.
Single place for base_url, default model, and client construction.
"""

from openai import AsyncOpenAI
from server.config import settings

BASE_URL = "https://api.deepseek.com"


def resolve_api_key(client_key: str | None = None) -> str:
    """Resolve which DeepSeek key to use for a request.

    Security: in production (debug=False) only the server-configured
    DEEPSEEK_API_KEY is trusted — a client-supplied key is ignored so users
    cannot make the server burn someone else's quota/credits. A client key is
    honored only in debug mode for local development.
    """
    if not settings.debug and client_key:
        return settings.deepseek_api_key
    return client_key or settings.deepseek_api_key


def get_client(api_key: str | None = None, timeout: float = 60.0) -> AsyncOpenAI:
    """Build a DeepSeek AsyncOpenAI client using the provided key or settings default."""
    key = api_key or settings.deepseek_api_key
    return AsyncOpenAI(api_key=key, base_url=BASE_URL, timeout=timeout, max_retries=1)


async def chat_completion(messages: list[dict], *, api_key: str | None = None,
                          model: str | None = None, max_tokens: int | None = None,
                          json_mode: bool = False):
    """Perform a single (non-streaming) chat completion against DeepSeek."""
    client = get_client(api_key)
    kwargs = dict(model=model or settings.deepseek_model, messages=messages, max_tokens=max_tokens)
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    return await client.chat.completions.create(**kwargs)


async def stream_chat(messages: list[dict], *, api_key: str | None = None,
                      model: str | None = None, max_tokens: int | None = None):
    """Open a streaming chat completion against DeepSeek."""
    client = get_client(api_key, timeout=300.0)
    return await client.chat.completions.create(
        model=model or settings.deepseek_model,
        messages=messages,
        max_tokens=max_tokens,
        stream=True,
    )
