from flask import Flask
import redis
import os

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
