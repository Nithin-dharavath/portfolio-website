import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

DATABASE_URL = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}".format(
    user=quote_plus(DB_CONFIG["user"]),
    password=quote_plus(DB_CONFIG["password"]),
    host=DB_CONFIG["host"],
    port=DB_CONFIG["port"],
    database=DB_CONFIG["database"],
)
