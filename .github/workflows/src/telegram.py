import os
import aiohttp
import asyncio

TOKEN   = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
URL     = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

async def send(text: str):
    """Send one message to the channel."""
    payload = {"chat_id": CHAT_ID, "text": text}
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json=payload) as resp:
            resp.raise_for_status()

async def send_lines(lines: list[str]):
    """Send several messages (one per fixture)."""
    for line in lines:
        await send(line)
