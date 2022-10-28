from pubsub_emulator_messaging_setup.pubsub import (
    create_subscription,
    create_topic,
    get_subscription_path,
    get_topic_path,
)
from pubsub_emulator_messaging_setup.types import Context
from pubsub_emulator_messaging_setup.utils import load_config


def setup_messaging(context: Context) -> None:
    config = load_config(context.config_path)

    for topic_config in config.topics:
        # Create topic
        topic_path = get_topic_path(
            context.publisher_client, context.project_id, topic_config.name
        )

        create_topic(context.publisher_client, topic_path)

        # Create subscriptions
        for subscription_name in topic_config.subscriptions:
            subscription_path = get_subscription_path(
                context.subscriber_client, context.project_id, subscription_name
            )

            create_subscription(context.subscriber_client, topic_path, subscription_path)
