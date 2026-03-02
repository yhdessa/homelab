from flask import Flask
import redis
import os
from pathlib import Path

app = Flask(__name__)
redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

@app.route("/")
def home():
    return "Homelab DevSecOps"

@app.route("/counter")
def counter():
    cnt = redis_client.incr("counter")
    return f"Counter: {cnt}"

def read_secret(secret_name: str, fallback: str = "") -> str:
    path = Path(f"/run/secrets/{secret_name}")
    if path.is_file():
        return path.read_text(encoding="utf-8").strip()
    return os.getenv(secret_name.upper(), fallback)

"""
DB_USER = read_secret("db_user", "appuser")
DB_PASS = read_secret("db_password", "devpass")
DB_NAME = read_secret("db_name", "app_production")
DB_HOST = "db_web"  # имя сервиса в docker-compose

DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
