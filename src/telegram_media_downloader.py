import asyncio
import os

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto


class TelegramMediaDownloader:
    def __init__(self, api_id, api_hash, session_string, group_url):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_string = session_string
        self.group_url = group_url
        self.client = TelegramClient(StringSession(session_string), api_id, api_hash)

    async def download_media(self, message, semaphore, download_path):
        async with semaphore:
            if isinstance(message.media, (MessageMediaPhoto, MessageMediaDocument)):
                subfolder = (
                    "photos/"
                    if isinstance(message.media, MessageMediaPhoto)
                    else "videos/"
                )
                await self.client.download_media(
                    message, file=os.path.join(download_path, subfolder)
                )

    def create_directories(self, base_path):
        directories = ["downloads", "downloads/photos", "downloads/videos"]
        for directory in directories:
            path = os.path.join(base_path, directory)
            if not os.path.exists(path):
                os.makedirs(path)

    async def run(self):
        async with self.client:
            await self.client.start()
            print("Client Created")

            base_path = str(self.group_url)
            self.create_directories(base_path)

            group_entity = await self.client.get_entity(self.group_url)
            total_messages = await self.client.get_messages(group_entity, limit=0)
            total_downloaded = 0
            semaphore = asyncio.Semaphore(5)

            last_id = 0
            while total_downloaded < total_messages.total:
                messages = await self.client.get_messages(
                    group_entity, limit=100, offset_id=last_id
                )
                if not messages:
                    break

                tasks = [
                    self.download_media(message, semaphore, base_path)
                    for message in messages
                ]
                await asyncio.gather(*tasks)

                total_downloaded += len(messages)
                last_id = messages[-1].id

            print(f"Downloaded media from {total_downloaded} messages.")
