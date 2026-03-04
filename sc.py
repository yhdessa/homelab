import os

from dotenv import load_dotenv
from flask import Flask
import redis

load_dotenv()

DB_HOST = os.environ["DB_HOST"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))

DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)

app = Flask(__name__)
app.config["DATABASE_URL"] = DATABASE_URL
app.config["DEBUG"] = DEBUG

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    socket_connect_timeout=3,
    socket_timeout=3,
)


@app.route("/")
def home():
    return "Homelab DevSecOps"


@app.route("/counter")
def counter():
    cnt = redis_client.incr("counter")
    return f"Counter: {cnt}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)
