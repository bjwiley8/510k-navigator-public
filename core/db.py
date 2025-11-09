from __future__ import annotations
from sqlalchemy import create_engine

def get_engine(url: str | None = None):
    """
    Return a SQLAlchemy engine. Default is in-memory SQLite for unit tests.
    """
    url = url or "sqlite+pysqlite:///:memory:"
    return create_engine(url, future=True)
