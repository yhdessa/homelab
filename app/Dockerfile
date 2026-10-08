FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get upgrade -y --no-install-recommends \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y pip setuptools wheel \
    && rm -rf /root/.cache /tmp/*

FROM python:3.11-slim

WORKDIR /app

# Upgrade OS packages and drop build-time Python packaging tools
# (pip/setuptools/wheel pull vulnerable vendored libs flagged by Trivy
#  and are not needed at runtime since deps already live in /venv).
RUN apt-get update && apt-get upgrade -y --no-install-recommends \
    && rm -rf /usr/local/lib/python3.11/site-packages/pip* \
    /usr/local/lib/python3.11/site-packages/setuptools* \
    /usr/local/lib/python3.11/site-packages/wheel* \
    /usr/local/lib/python3.11/site-packages/pkg_resources* \
    /usr/local/lib/python3.11/site-packages/_distutils_hack* \
    /usr/local/lib/python3.11/site-packages/distutils-precedence.pth \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /root/.cache

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

RUN groupadd -r appgroup && useradd -r -g appgroup -m appuser

COPY --chown=appuser:appgroup src ./src
COPY --chown=appuser:appgroup gunicorn_json_logging.py ./

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=5 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health', timeout=5)" || exit 1

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
