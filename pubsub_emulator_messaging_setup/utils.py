from pathlib import Path

import yaml

from pubsub_emulator_messaging_setup.types import PubSubSetupConfig


def load_config(config_filename: Path) -> PubSubSetupConfig:
    raw = yaml.safe_load(config_filename.open())
    config = PubSubSetupConfig.parse_obj(raw)

    return config
