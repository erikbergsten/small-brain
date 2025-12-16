from openai import AsyncOpenAI
import os
import ssl
from httpx_aiohttp import HttpxAiohttpClient

# Configuration via environment variables
OPENAI_API_KEY = os.getenv("SMALL_BRAIN_API_KEY")
OPENAI_BASE_URL = os.getenv("SMALL_BRAIN_BASE_URL")
CA_CERT = os.getenv("SMALL_BRAIN_CA_CERT")
CA_PATH = os.getenv("SMALL_BRAIN_CA_PATH")

ssl_ctx = ssl.create_default_context(capath=CA_PATH, cafile=CA_CERT)
http_client = HttpxAiohttpClient(verify=ssl_ctx)

client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    http_client=http_client,
)

async def stop():
    await client.close()
