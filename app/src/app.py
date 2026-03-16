import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Dict, Any

from dotenv import load_dotenv
from flask import Flask, jsonify
import redis
from redis.exceptions import ConnectionError as RedisConnectionError
from pythonjsonlogger import jsonlogger
import psycopg

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "db_web")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

if not all([DB_USER, DB_PASSWORD, DB_NAME]):
    raise ValueError("Missing required DB environment variables")

DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

app = Flask(__name__)
app.config["DEBUG"] = DEBUG
app.config["DATABASE_URL"] = DATABASE_URL

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

json_formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(message)s \
        %(pathname)s %(funcName)s %(lineno)d",
    json_ensure_ascii=False,
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(json_formatter)
logger.addHandler(console_handler)

file_handler = RotatingFileHandler(
    "/tmp/app.log", maxBytes=10 * 1024 * 1024, backupCount=5
)
file_handler.setFormatter(json_formatter)
logger.addHandler(file_handler)

logging.getLogger("werkzeug").setLevel(logging.WARNING)

redis_client: redis.Redis | None = None
if REDIS_HOST:
    try:
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True,
            socket_timeout=5,
            socket_connect_timeout=5,
        )
        redis_client.ping()
        logger.info("Redis connected successfully")
    except RedisConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
        redis_client = None


def get_db_connection() -> psycopg.Connection:
    try:
        conn = psycopg.connect(DATABASE_URL)
        logger.debug("PostgreSQL connection established")
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise


@app.route("/")
def home() -> str:
    return "Homelab DevSecOps"


@app.route("/counter")
def counter() -> str:
    if redis_client is None:
        return "Redis not configured", 503

    try:
        cnt = redis_client.incr("counter")
        return f"Counter: {cnt}"
    except Exception as e:
        logger.error(f"Redis counter error: {e}")
        return "Redis error", 503


@app.route("/health")
def health() -> tuple[Dict[str, Any], int]:
    status: Dict[str, str] = {"status": "healthy"}

    if redis_client:
        try:
            redis_client.ping()
            status["redis"] = "ok"
        except Exception:
            status["redis"] = "error"
    else:
        status["redis"] = "not configured"

    try:
        conn = get_db_connection()
        conn.close()
        status["database"] = "ok"
    except Exception:
        status["database"] = "error"

    code = 200 if all(v == "ok" for v in status.values() if isinstance(v, str)) else 503
    return jsonify(status), code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)
