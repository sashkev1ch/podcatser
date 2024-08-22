from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
import asyncio as aio
import aiofile
import aiohttp


@dataclass
class Episode:
    name: str
    link: str
    publish_date: datetime
    local_path: Path
    days_of_actual: int = 45

    def __str__(self):
        return f"episode: {self.name}, published: {self.publish_date}"

    @property
    def exist(self) -> bool:
        return self.local_path.exists()

    @property
    def actual(self) -> bool:
        delta = datetime.now(tz=self.publish_date.tzinfo) - self.publish_date
        return delta.days <= self.days_of_actual

    async def download(
        self, session: aiohttp.ClientSession, semaphore: aio.BoundedSemaphore
    ):
        async with semaphore:
            async with session.get(self.link) as resp:
                print(self)
                assert resp.status == 200
                data = await resp.read()

        async with aiofile.async_open(self.local_path, "wb") as outfile:
            await outfile.write(data)
