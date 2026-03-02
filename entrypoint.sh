#!/bin/sh
set -e

[ -f /run/secrets/db_user     ] && export DB_USER=$(cat /run/secrets/db_user)
[ -f /run/secrets/db_password ] && export DB_PASSWORD=$(cat /run/secrets/db_password)
[ -f /run/secrets/db_name     ] && export DB_NAME=$(cat /run/secrets/db_name)

export DATABASE_URL="postgresql://${DB_USER}:${DB_PASSWORD}@db_web:5432/${DB_NAME}"

exec "$@"
