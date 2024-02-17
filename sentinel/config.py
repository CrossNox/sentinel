import urllib.parse

import youconfigme as ycm

from sentinel.constants import DEFAULT_SQLITE, Environments

cfg = ycm.AutoConfig()

env = cfg.env(default=Environments.DEV.value, cast=Environments)

DB_URL: str
try:
    DB_URL = cfg.database.url()
except ycm.ConfigItemNotFound:
    try:
        db_cfg = {
            "host": cfg.api.db_host(),
            "port": cfg.api.db_port(),
            "user": cfg.api.db_user(),
            "password": cfg.api.db_password(),
            "dbname": cfg.api.db_name(),
        }
        DB_URL = (
            "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}".format(
                **{k: urllib.parse.quote_plus(v) for k, v in db_cfg.items()}
            )
        )
    except ycm.ConfigItemNotFound:
        DB_URL = DEFAULT_SQLITE
