from pathlib import Path
from yaml import load, FullLoader
from podcatser.control.control import prepare_channel_library


def main():
    project_path = Path(__file__).parent.parent
    config_path = project_path.joinpath("config/config.yml")

    with open(config_path, "r") as conf:
        config = load(conf, Loader=FullLoader)

    for rss_url in config["rss_channels"]:
        prepare_channel_library(project_path=project_path, channel_rss_url=rss_url)


if __name__ == "__main__":
    main()
