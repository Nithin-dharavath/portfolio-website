import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

DB_HOST: str = os.getenv("DB_HOST", "localhost")
DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
DB_NAME: str = os.getenv("DB_NAME", "portfolio")
DB_USER: str = os.getenv("DB_USER", "root")
DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

DB_CONFIG: dict[str, str | int] = {
    "host": DB_HOST,
    "port": DB_PORT,
    "database": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
}

DATABASE_URL: str = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}".format(
    user=quote_plus(DB_USER),
    password=quote_plus(DB_PASSWORD),
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)
