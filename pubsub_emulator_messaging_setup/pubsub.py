import grpc
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import AlreadyExists
from google.auth.credentials import AnonymousCredentials
from google.pubsub_v1 import GetSubscriptionRequest, GetTopicRequest
from google.pubsub_v1.services.publisher.client import PublisherClient
from google.pubsub_v1.services.publisher.transports.grpc import PublisherGrpcTransport
from google.pubsub_v1.services.subscriber.client import SubscriberClient
from google.pubsub_v1.services.subscriber.transports import SubscriberGrpcTransport
from google.pubsub_v1.types import Subscription, Topic
from loguru import logger


def get_publisher_client(endpoint: str) -> PublisherClient:
    grpc_channel = grpc.insecure_channel(endpoint)
    transport = PublisherGrpcTransport(channel=grpc_channel, credentials=AnonymousCredentials())
    client_options = ClientOptions(api_endpoint=endpoint)
    publisher = PublisherClient(transport=transport, client_options=client_options)

    return publisher


def get_subscriber_client(endpoint: str) -> SubscriberClient:
    grpc_channel = grpc.insecure_channel(endpoint)
    transport = SubscriberGrpcTransport(channel=grpc_channel, credentials=AnonymousCredentials())
    client_options = ClientOptions(api_endpoint=endpoint)
    subscriber = SubscriberClient(transport=transport, client_options=client_options)

    return subscriber


def get_topic_path(client: PublisherClient, project_id: str, topic_name: str) -> str:
    return client.topic_path(project_id, topic_name)


def get_topic(client: PublisherClient, topic_path: str) -> Topic:
    request = GetTopicRequest(topic=topic_path)
    topic = client.get_topic(request)

    return topic


def create_topic(client: PublisherClient, topic_path: str) -> Topic:
    logger.info(f"Creating topic {topic_path} ...")

    request = Topic(name=topic_path)

    try:
        topic = client.create_topic(request)
    except AlreadyExists:
        logger.info(f"Topic {topic_path} exists, retrieving ...")

        topic = get_topic(client, topic_path)
    else:
        logger.info(f"Created topic {topic.name}")

    return topic


def get_subscription_path(
    client: SubscriberClient, project_id: str, subscription_name: str
) -> str:
    return client.subscription_path(project_id, subscription_name)


def get_subscription(client: SubscriberClient, subscription_path: str) -> Subscription:
    request = GetSubscriptionRequest(subscription=subscription_path)
    subscription = client.get_subscription(request)

    return subscription


def create_subscription(
    client: SubscriberClient, topic_path: str, subscription_path: str
) -> Subscription:
    logger.info(f"Creating subscription {subscription_path} ...")

    request = Subscription(name=subscription_path, topic=topic_path)

    try:
        subscription = client.create_subscription(request)
    except AlreadyExists:
        logger.info(f"Subscription {subscription_path} exists, retrieving ...")

        subscription = get_subscription(client, subscription_path)
    else:
        logger.info(f"Created subscription {subscription.name}")

    return subscription
