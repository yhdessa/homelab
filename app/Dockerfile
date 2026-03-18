FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install --upgrade pip wheel setuptools

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

RUN groupadd -r appgroup && useradd -r -g appgroup -m appuser

COPY --chown=appuser:appgroup . .

USER appuser

CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "2", \
     "--threads", "4", \
     "--timeout", "30", \
     "--worker-tmp-dir", "/tmp", \
     "--pid", "/tmp/gunicorn.pid", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--config", "gunicorn_json_logging.py", \
     "src.app:app"]
