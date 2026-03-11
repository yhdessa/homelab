FROM python:3.11-alpine AS builder

WORKDIR /app
COPY requirements.txt .

RUN apk add --no-cache build-base \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TMPDIR=/tmp

WORKDIR /app

COPY --from=builder /usr/local /usr/local

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --chown=appuser:appgroup . .

USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "--timeout", "30", "--worker-tmp-dir", "/tmp", "--pid", "/tmp/gunicorn.pid", "--access-logfile", "-", "sc:app"]
