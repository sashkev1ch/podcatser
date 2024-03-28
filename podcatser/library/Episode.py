from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from urllib.request import urlopen
from shutil import copyfileobj


@dataclass
class Episode:
    name: str
    link: str
    publish_date: datetime
    local_path: Path

    def __str__(self):
        return f"episode: {self.name}, published: {self.publish_date}"

    @property
    def exist(self) -> bool:
        return self.local_path.exists()

    @property
    def actual(self) -> bool:
        delta = datetime.now(tz=self.publish_date.tzinfo) - self.publish_date
        return delta.days <= 60

    def download(self) -> None:
        with urlopen(self.link) as response:
            with open(self.local_path, "wb") as out_file:
                copyfileobj(response, out_file)
