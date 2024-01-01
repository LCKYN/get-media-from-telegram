import asyncio
import os

from dotenv import load_dotenv

from src.telegram_media_downloader import TelegramMediaDownloader

load_dotenv()

if __name__ == "__main__":
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")
    session_string = os.getenv("SESSION_STRING")
    group_url = 1234567890

    downloader = TelegramMediaDownloader(api_id, api_hash, session_string, group_url)
    asyncio.run(downloader.run())
