import textwrap
from pathlib import Path

from google.pubsub_v1.types import Subscription, Topic
from pytest_mock import MockerFixture

from pubsub_emulator_messaging_setup.cli import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_PROJECT_ID,
    DEFAULT_PUBSUB_URI,
)
from pubsub_emulator_messaging_setup.core import setup_messaging
from pubsub_emulator_messaging_setup.pubsub import (
    get_publisher_client,
    get_subscriber_client,
)
from pubsub_emulator_messaging_setup.types import Context


def test_setup(mocker: MockerFixture, temporary_path: Path) -> None:
    """
    GIVEN CLI options
        AND a PubSub setup
    WHEN setting up
    THEN calls to create topics are expected
        AND calls to create subscriptions are expected
    """
    # GIVEN
    config_path = temporary_path / DEFAULT_CONFIG_PATH
    config_path.write_text(
        textwrap.dedent(
            """
                topics:
                - name: test-topic
                  subscriptions:
                  - test-subscription
            """
        )
    )

    context = Context(
        config_path=config_path,
        uri=DEFAULT_PUBSUB_URI,
        project_id=DEFAULT_PROJECT_ID,
        publisher_client=get_publisher_client(DEFAULT_PUBSUB_URI),
        subscriber_client=get_subscriber_client(DEFAULT_PUBSUB_URI),
    )

    spy_create_topic = mocker.spy(context.publisher_client, "create_topic")
    spy_create_subscription = mocker.spy(context.subscriber_client, "create_subscription")

    # WHEN
    setup_messaging(context)

    # THEN
    spy_create_topic.assert_called_once_with(Topic(name="projects/test-project/topics/test-topic"))
    spy_create_subscription.assert_called_once_with(
        Subscription(
            name="projects/test-project/subscriptions/test-subscription",
            topic="projects/test-project/topics/test-topic",
        )
    )
