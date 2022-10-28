from pathlib import Path

import click
from loguru import logger

from pubsub_emulator_messaging_setup.core import setup_messaging
from pubsub_emulator_messaging_setup.pubsub import (
    get_publisher_client,
    get_subscriber_client,
)
from pubsub_emulator_messaging_setup.types import Context

DEFAULT_CONFIG_PATH = Path("pubsub.yml")
DEFAULT_PROJECT_ID = "test-project"
DEFAULT_PUBSUB_URI = "localhost:8085"


@click.command
@click.option(
    "--config-path",
    "-c",
    default=DEFAULT_CONFIG_PATH,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help=f"Path to the PubSub YAML config file. Default is {DEFAULT_CONFIG_PATH}",
)
@click.option(
    "--project",
    "-p",
    default=DEFAULT_PROJECT_ID,
    help=f"Default project ID. Default is {DEFAULT_PROJECT_ID}",
)
@click.option(
    "--uri",
    default=DEFAULT_PUBSUB_URI,
    help="Default PubSub emulator URI. Default is {DEFAULT_PUBSUB_URI}",
)
def main(config_path: Path, project: str, uri: str) -> None:
    # Get config
    logger.info("Loading config file")

    # Create PubSub clients
    logger.info(f"Creating PubSub topic client to {uri} in {project}")
    publisher_client = get_publisher_client(uri)

    logger.info(f"Creating PubSub subscriber client to {uri} in {project}")
    subscriber_client = get_subscriber_client(uri)

    #
    context = Context(
        config_path=config_path,
        project_id=project,
        uri=uri,
        publisher_client=publisher_client,
        subscriber_client=subscriber_client,
    )

    setup_messaging(context)
