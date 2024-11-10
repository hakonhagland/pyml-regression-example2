from typing import Protocol

from pathlib import Path
from unittest.mock import Mock

# NOTE: These type aliases cannot start with "Test" because then pytest will
#       believe that they are test classes, see https://stackoverflow.com/q/76689604/2173773


class PrepareConfigDir(Protocol):  # pragma: no cover
    def __call__(self, add_config_ini: bool) -> Path:
        pass


class PrepareDataDir(Protocol):  # pragma: no cover
    def __call__(self, datafiles_exists: bool) -> Path:
        pass


class MockRequestGet(Protocol):  # pragma: no cover
    def __call__(self, datafile_contents: bytes) -> Mock:
        pass


class DataFileContents(Protocol):  # pragma: no cover
    def __call__(self, filename: str) -> bytes:
        pass
