import logging
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from .config import DATABASE_URL, DB_HOST

logger = logging.getLogger(__name__)

_connect_args: dict = {}
if "tidbcloud.com" in DB_HOST:
    ssl_ca_path = os.getenv("DB_SSL_CA", "")
    _connect_args["ssl"] = {"ca": ssl_ca_path} if ssl_ca_path else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=_connect_args,
    pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
    pool_pre_ping=True,
    pool_recycle=int(os.getenv("DB_POOL_RECYCLE", "3600")),
    pool_timeout=int(os.getenv("DB_POOL_TIMEOUT", "30")),
    echo=False,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error("Database connection failed: %s", e)
        return False
