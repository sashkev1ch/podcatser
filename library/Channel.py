from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import List
from library.Episode import Episode


@dataclass
class Channel:
    name: str
    local_path: Path
    episodes: List[Episode]

    def __post_init__(self):
        self.create_channel_directory()

    def __str__(self):
        return str(self.local_path)

    def create_channel_directory(self):
        self.local_path.mkdir(parents=True, exist_ok=True)

    def get_episodes(self):
        for episode in self.episodes:
            if not episode.exist and episode.actual:
                print(f"Download {episode}")
                episode.download()
