from pathlib import Path
from requests import get
from rss_parser import RSSParser
import asyncio as aio
from podcatser.library.utils import get_datetime
from podcatser.library.Episode import Episode
from podcatser.library.Channel import Channel


def prepare_channel_library(project_path: Path, channel_rss_url: str) -> None:
    response = get(channel_rss_url)
    rss = RSSParser.parse(response.text)

    channel_name = rss.channel.title.content.replace(" ", "_")
    channel_dir = project_path.joinpath(f"downloads/{channel_name}")

    episodes = []

    for item in rss.channel.items:
        episode_title = item.title.content.replace(" ", "_").replace("/", "_")
        file_name = f"{episode_title}.mp3"

        episodes.append(
            Episode(
                name=file_name,
                link=item.enclosure.attributes["url"],
                publish_date=get_datetime(item.pub_date.content),
                local_path=channel_dir.joinpath(file_name),
            )
        )

    channel = Channel(name=channel_name, local_path=channel_dir, episodes=episodes)

    loop = aio.get_event_loop()

    if loop.is_closed():
        loop = aio.new_event_loop()

    loop.run_until_complete(channel.get_episodes())
    loop.close()
