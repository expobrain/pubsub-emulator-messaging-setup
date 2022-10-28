from pathlib import Path
from typing import List

from google.pubsub_v1.services.publisher.client import PublisherClient
from google.pubsub_v1.services.subscriber.client import SubscriberClient
from pydantic import BaseModel, Field


class ImmutableBaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        allow_mutation = False


class PubSubTopic(ImmutableBaseModel):
    name: str
    subscriptions: List[str]


class PubSubSetupConfig(ImmutableBaseModel):
    topics: List[PubSubTopic] = Field(default_factory=list)


class Context(ImmutableBaseModel):
    project_id: str
    uri: str
    config_path: Path
    publisher_client: PublisherClient
    subscriber_client: SubscriberClient
