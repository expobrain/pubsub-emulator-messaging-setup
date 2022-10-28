from pathlib import Path
from unittest.mock import ANY

from click.testing import CliRunner
from pytest_mock import MockerFixture

from pubsub_emulator_messaging_setup import cli
from pubsub_emulator_messaging_setup.cli import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_PROJECT_ID,
    DEFAULT_PUBSUB_URI,
)
from pubsub_emulator_messaging_setup.types import Context


def test_main(mocker: MockerFixture, temporary_path: Path) -> None:
    """
    GIVEN CLI args
        AND an empty Pubsub setup
    WHEN parsing to a Context
    THEN is the expected
    """
    # GIVEN
    config_path = temporary_path / DEFAULT_CONFIG_PATH
    config_path.touch()

    runner = CliRunner()

    m_setup_messaging = mocker.patch("pubsub_emulator_messaging_setup.cli.setup_messaging")

    # WHEN
    actual = runner.invoke(cli.main, ["-c", config_path.as_posix()])

    # THEN
    print(actual.output)
    assert actual.exit_code == 0

    expected = Context.construct(
        project_id=DEFAULT_PROJECT_ID,
        uri=DEFAULT_PUBSUB_URI,
        config_path=config_path,
        publisher_client=ANY,
        subscriber_client=ANY,
    )

    m_setup_messaging.assert_called_once_with(expected)
