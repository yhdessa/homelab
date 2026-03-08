FROM postgres:16-alpine

RUN apk add --no-cache tzdata
ENV TZ=UTC
ENV PGDATA=/var/lib/postgresql/data

HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
  CMD pg_isready -U "${POSTGRES_USER:-postgres}" -d "${POSTGRES_DB:-postgres}" || exit 1

