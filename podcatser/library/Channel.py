from pathlib import Path
from dataclasses import dataclass
from typing import List
from podcatser.library.Episode import Episode
import asyncio as aio
import aiofile
import aiohttp


@dataclass
class Channel:
    name: str
    local_path: Path
    episodes: List[Episode]

    def __post_init__(self):
        self.create_channel_directory()

    def __str__(self):
        return str(self.local_path)

    def create_channel_directory(self) -> None:
        self.local_path.mkdir(parents=True, exist_ok=True)

    async def get_episodes(self) -> None:
        semaphore = aio.BoundedSemaphore(5)
        async with aiohttp.ClientSession() as session:
            tasks = [
                episode.download(session, semaphore)
                for episode in self.episodes
                if not episode.exist and episode.actual
            ]
            await aio.gather(*tasks)
