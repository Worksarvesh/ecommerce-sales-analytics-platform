from contextlib import contextmanager
from pathlib import Path
import sys

import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine

sys.path.append(str(Path(__file__).resolve().parents[1]))
from config import config  # noqa: E402


def get_db_connection(dict_cursor: bool = False):
    """Return a psycopg2 connection using environment variables."""
    cursor_factory = RealDictCursor if dict_cursor else None
    return psycopg2.connect(
        host=config.database.host,
        database=config.database.name,
        user=config.database.user,
        password=config.database.password,
        port=config.database.port,
        cursor_factory=cursor_factory,
    )


@contextmanager
def db_cursor(dict_cursor: bool = False):
    connection = get_db_connection(dict_cursor=dict_cursor)
    try:
        cursor = connection.cursor()
        yield cursor
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def get_sqlalchemy_engine():
    """Return a SQLAlchemy engine for pandas and analytics workflows."""
    return create_engine(config.database.sqlalchemy_url, pool_pre_ping=True)
