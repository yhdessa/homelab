FROM python:3.11-alpine AS builder

WORKDIR /app
COPY requirements.txt .

RUN apk add --no-cache build-base \
    && pip install --no-cache-dir --upgrade pip wheel setuptools \
    && pip install --no-cache-dir -r requirements.txt

FROM python:3.11-alpine

WORKDIR /app

COPY --from=builder /usr/local /usr/local

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --chown=appuser:appgroup . .

USER appuser

CMD ["python", "sc.py"]
