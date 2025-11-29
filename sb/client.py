from openai import DefaultAioHttpClient
from openai import AsyncOpenAI
import os

# Configuration via environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE")

client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    http_client=DefaultAioHttpClient(),
)

async def stop():
    await client.close()
