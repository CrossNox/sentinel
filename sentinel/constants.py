"""Useful constants to use throughout sentinel and beyond."""

import enum
import pathlib


class Environments(str, enum.Enum):
    DEV = "development"
    STG = "staging"
    PRD = "production"

POOL_SIZE: int = 50
MAX_OVERFLOW: int = 200
DEFAULT_PORT = 5000
DEFAULT_HOST = "0.0.0.0"
DEFAULT_WORKERS = 2
DEFAULT_PRETTY = False
DEFAULT_VERBOSE = 0
DEFAULT_STRUCTURED = True

DEFAULT_SQLITE_LOC = pathlib.Path(__name__).parent.parent / "sentinel.db"
DEFAULT_SQLITE = f"sqlite:////{DEFAULT_SQLITE_LOC.resolve()}"
