import logging

import typer
import uvicorn
from sentinel.config import cfg
from sentinel.constants import (DEFAULT_HOST,
                                                     DEFAULT_PORT,
                                                     DEFAULT_STRUCTURED,
                                                     DEFAULT_WORKERS)
from sentinel.utils import (DEFAULT_PRETTY,
                                                 DEFAULT_STRUCTURED,
                                                 DEFAULT_VERBOSE,
                                                 config_logging, to_bool)

cli = typer.Typer()


@cli.callback()
def main(
    verbose: int = typer.Option(
        cfg.server.verbose(default=DEFAULT_VERBOSE, cast=int),
        "--verbose",
        "-v",
        count=True,
        help="Level of verbosity. Can be passed more than once for more levels of logging.",
    ),
    pretty: bool = typer.Option(
        cfg.server.pretty(default=DEFAULT_PRETTY, cast=to_bool),
        "--pretty/--plain",
        help="Whether to pretty print the logs with colors",
    ),
    structured: bool = typer.Option(
        cfg.server.structured(default=DEFAULT_STRUCTURED, cast=to_bool),
        "--structured/--unstructured",
        "-s/-u",
        help="Output structured logs instead of plain text",
    ),
):
    config_logging(verbose, pretty, structured)

@cli.command()
def server(
    host: str = typer.Option(
        cfg.api.host(default=DEFAULT_HOST), help="Host to bind to"
    ),
    port: int = typer.Option(
        cfg.api.port(default=DEFAULT_PORT), help="Port to bind to"
    ),
    reload: bool = typer.Option(False, help="Live reloading"),
    workers: int = typer.Option(
        cfg.api.workers(default=DEFAULT_WORKERS), min=1, help="Amount of workers to use"
    ),
):
    uvicorn_server = uvicorn.Server(
        uvicorn.Config(
            "sentinel.api.app:app",
            reload=reload,
            reload_dirs=["sentinel/"],
            host=host,
            port=port,
            workers=workers,
            log_level=logging.getLevelName(
                logging.getLogger().getEffectiveLevel()
            ).lower(),
            log_config={"version": 1},
        )
    )

    uvicorn_server.run()
