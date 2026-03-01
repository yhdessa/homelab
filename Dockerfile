FROM python:3.11-alpine AS builder

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache build-base \
    && pip install --no-cache-dir --upgrade pip>=26.0 wheel>=0.46.2 setuptools \
    && pip install --no-cache-dir -r requirements.txt

FROM python:3.11-alpine

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin /usr/local/bin/

COPY . .

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

USER appuser

CMD ["python", "sc.py"]
