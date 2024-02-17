"""Jinja helpers."""
from typing import List
from uuid import uuid4

import jinja2
import sqlparse
from jinjasql import JinjaSql
from pkg_resources import resource_filename
from sentinel.constants import Environments
from sentinel.utils import get_logger

logger = get_logger(__name__)


def wrap(iterable: List) -> List[str]:
    """Quote elements of list."""
    return [f"'{x}'" for x in iterable]


def load_resource(path: str) -> str:
    """Load a package resource by path."""
    with open(  # pylint: disable=unspecified-encoding
        resource_filename("sentinel", f"resources/{path}")
    ) as resource_file:
        return resource_file.read()


def load_sql_query(filename: str) -> str:
    """Load a SQL query from package resources.

    Parameters
    ----------
    filename: Filename to load


    Returns
    -------
    Raw query SQL.
    """
    logger.info("Loading query from %s", filename)
    return load_resource(f"sql/{filename}.sql")


def _prepare_env() -> jinja2.Environment:
    jinja_logging_undef = jinja2.make_logging_undefined(
        logger=logger, base=jinja2.Undefined
    )
    env = jinja2.Environment(
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=jinja_logging_undef,
        autoescape=True,
        loader=jinja2.PackageLoader("sentinel", package_path="resources/"),
    )
    env.filters["wrap"] = wrap
    env.globals.update(dict(uuid4=uuid4, Environments=Environments))
    return env


def render(file: str, **params) -> str:
    """Render a template with given params."""
    env = _prepare_env()

    template: jinja2.Template
    try:
        template = env.get_template(file)
    except jinja2.TemplateNotFound:
        logger.warning("Assuming passed string is a template")
        template = env.from_string(file)

    return template.render(**params)


def render_sql_query(sql: str, **query_context_params) -> str:
    """Render jinja sql with params.
    Parameters
    ----------
    sql : str
        Query to be formatted.
    query_context_params : Any
        Parameters to format the query.
    Returns
    -------
    sql : str
        Formatted query.
    """
    env = _prepare_env()

    try:
        sql = env.get_template(sql)
    except (FileNotFoundError, jinja2.TemplateNotFound):
        logger.warning("Assuming passed string is a template")

    if query_context_params:
        j = JinjaSql(env=env, param_style="pyformat")
        binded_sql, bind_params = j.prepare_query(sql, query_context_params)
        missing_placeholders = [
            k for k, v in bind_params.items() if jinja2.Undefined() == v
        ]

        if len(missing_placeholders) != 0:
            raise ValueError(f"Missing placeholders are: {missing_placeholders}")

        try:
            sql = binded_sql % bind_params
        except KeyError as exc:
            logger.error(exc)
            raise

    return sqlparse.format(sql, reindent=True, keyword_case="upper")
