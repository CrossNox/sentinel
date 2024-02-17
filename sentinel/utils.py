"""Common code undeserving of its own module."""

import functools
import logging
from typing import Union

import typer
from pythonjsonlogger import jsonlogger
from sentinel.config import cfg
from sentinel.constants import (DEFAULT_PRETTY,
                                                     DEFAULT_STRUCTURED,
                                                     DEFAULT_VERBOSE)

DEFAULT_PRETTY = False
DEFAULT_VERBOSE = 0

def to_bool(s: Union[str, bool]):
    if isinstance(s, bool):
        return s

    if s.lower() in ("yes", "true", "t", "1", "True"):
        return True

    if s.lower() in ("no", "false", "f", "0", "False"):
        return False

    raise ValueError(f"Invalid value for bool: {s}")

class TyperLoggerHandler(logging.Handler):
    """Logging handler that works well with typer."""

    def __init__(self, pretty: bool, *args, **kwargs):
        self.pretty = pretty
        super().__init__(*args, **kwargs)

    def emit(self, record: logging.LogRecord) -> None:
        if not self.pretty:
            typer.secho(self.format(record))
            return

        foreground = None
        background = None
        if record.levelno == logging.DEBUG:
            foreground = typer.colors.BLACK
            background = typer.colors.WHITE
        elif record.levelno == logging.INFO:
            foreground = typer.colors.BRIGHT_BLUE
        elif record.levelno == logging.WARNING:
            foreground = typer.colors.BRIGHT_MAGENTA
        elif record.levelno == logging.CRITICAL:
            foreground = typer.colors.BRIGHT_RED
        elif record.levelno == logging.ERROR:
            foreground = typer.colors.BLACK
            background = typer.colors.BRIGHT_RED
        typer.secho(self.format(record), bg=background, fg=foreground)



def config_once(f):
    """Decorator to force config_logging to be called just once.

    If you run the server from the clerk CLI, config_logging will be called twice:
    - First from the main callback on the CLI
        - This takes YCM config to populate defaults
        - Then uses whatever values you passed
    - Then on the lifespan function from the app
        - This takes YCM config

    Therefore, the second call will override the values passed by the user.
    The easiest solution would be to remove the call in lifespan, but if for
    whatever reason we need to run with the uvicorn CLI or any other ASGI/WSGI
    server, then we'd be unable to config the logging.
    """
    has_been_set = False

    @functools.wraps(f)
    def just_once(*args, **kwargs):
        nonlocal has_been_set
        if has_been_set:
            return
        has_been_set = True
        return f(*args, **kwargs)

    return just_once


@config_once
def config_logging(
    verbose: int = cfg.server.verbose(default=DEFAULT_VERBOSE, cast=int),
    pretty: bool = cfg.server.pretty(default=DEFAULT_PRETTY, cast=to_bool),
    structured: bool = cfg.server.structured(default=DEFAULT_STRUCTURED, cast=to_bool),
):
    """Configure logging for stream and file."""

    level = logging.ERROR
    if verbose == 1:
        level = logging.INFO
    elif verbose > 1:
        level = logging.DEBUG

    logger = logging.getLogger()

    logger.setLevel(level)

    if not structured:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    else:
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s"
        )
    typer_handler = TyperLoggerHandler(pretty=pretty)
    typer_handler.setLevel(level)
    typer_handler.setFormatter(formatter)
    logger.addHandler(typer_handler)


def get_logger(name: str):
    """Create a new logger for name."""
    return logging.getLogger(name)
