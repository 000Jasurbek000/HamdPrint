#!/usr/bin/env bash
# Shared hosting (cPanel) uchun yangilash
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$APP_DIR/.env"
ENV_BACKUP="/tmp/hamdprint.env.backup"

cd "$APP_DIR"

echo "==> .env zaxirasi"
[ -f "$ENV_FILE" ] && cp "$ENV_FILE" "$ENV_BACKUP"

echo "==> Git pull"
git pull origin main

[ -f "$ENV_BACKUP" ] && cp "$ENV_BACKUP" "$ENV_FILE" && echo "    .env tiklandi"

echo "==> Paketlar"
pip install -r requirements.txt

echo "==> Migratsiya"
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "Yangilash tugadi. Passenger/cPanel ni qayta ishga tushiring."
