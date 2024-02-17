"""Base object to declare all ORM classes"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sentinel.utils import get_logger
from sentinel.config import DB_URL, cfg
from sentinel.constants import POOL_SIZE, MAX_OVERFLOW, DEFAULT_SQLITE

logger = get_logger(__name__)


def fix_psql_schema(db_conn_url: str) -> str:
    """Fix the deprecated postgres dialect."""
    if db_conn_url.startswith("postgres://"):
        db_conn_url = db_conn_url.replace("postgres://", "postgresql+psycopg2://")
    return db_conn_url


DB_CONN_ARGS = {"check_same_thread": False} if DB_URL == DEFAULT_SQLITE else {}
EXTRA_ARGS = (
    {}
    if DB_URL == DEFAULT_SQLITE
    else {
        "pool_size": cfg.api.pool_size(default=POOL_SIZE, cast=int),
        "max_overflow": cfg.api.max_overflow(default=MAX_OVERFLOW, cast=int),
    }
)

engine = create_engine(DB_URL, connect_args=DB_CONN_ARGS, **EXTRA_ARGS)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class UpdatableBase:
    def update_fields(self, **kwargs):
        for field, val in kwargs.items():
            setattr(self, field, val)


def keyvalgen(obj):
    """Generate attr name/val pairs, filtering out SQLA attrs.

    Source: https://stackoverflow.com/a/54034230
    """
    excl = ("_sa_adapter", "_sa_instance_state")
    for k, v in vars(obj).items():
        if not k.startswith("_") and not any(hasattr(v, a) for a in excl):
            yield k, v


class PrintableBase:
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        params = ", ".join(f"{k}={v}" for k, v in keyvalgen(self))
        return f"{self.__class__.__name__}({params})"
