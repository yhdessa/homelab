#!/bin/sh
# First-run bootstrap for local dev: creates files that are git-ignored
# (and therefore missing on a fresh clone) but required by
# docker-compose.yml bind mounts: secrets/*, nginx self-signed certs,
# and the certbot webroot. Idempotent - never overwrites existing files.
set -eu

cd "$(dirname "$0")/.."

mkdir -p secrets nginx/certs nginx/www

# Docker secrets (values default to .env so compose and app agree)
if [ ! -f secrets/db_user ]; then
  printf '%s' "${DB_USER:-postgres}" > secrets/db_user
  echo "created secrets/db_user"
fi
if [ ! -f secrets/db_password ]; then
  printf '%s' "${DB_PASSWORD:-postgres}" > secrets/db_password
  echo "created secrets/db_password"
fi
if [ ! -f secrets/db_name ]; then
  printf '%s' "${DB_NAME:-homelab}" > secrets/db_name
  echo "created secrets/db_name"
fi
chmod 600 secrets/db_user secrets/db_password secrets/db_name 2>/dev/null || true

# Self-signed cert for local nginx (baked into the image at build time too,
# but compose bind-mounts the host path, so it must exist)
if [ ! -f nginx/certs/selfsigned.crt ] || [ ! -f nginx/certs/selfsigned.key ]; then
  openssl req -x509 -nodes -days 3650 \
    -newkey rsa:2048 \
    -keyout nginx/certs/selfsigned.key \
    -out nginx/certs/selfsigned.crt \
    -subj "/C=RU/ST=YourState/L=YourCity/O=YourOrg/CN=localhost"
  echo "created nginx/certs/selfsigned.{crt,key}"
fi

echo "init done"
