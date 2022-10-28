from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterable

import pytest


@pytest.fixture
def temporary_path() -> Iterable[Path]:
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        yield temp_path
