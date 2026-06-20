#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/var/www/hamdprint"
VENV_DIR="$APP_DIR/venv"
ENV_FILE="$APP_DIR/.env"
ENV_BACKUP="/tmp/hamdprint.env.backup"

cd "$APP_DIR"

echo "==> .env zaxirasi (server sozlamalari saqlanadi)"
if [ -f "$ENV_FILE" ]; then
  cp "$ENV_FILE" "$ENV_BACKUP"
fi

echo "==> Git yangilanish (faqat kod, .env o'zgarmaydi)"
git pull origin main

if [ -f "$ENV_BACKUP" ]; then
  cp "$ENV_BACKUP" "$ENV_FILE"
  echo "    .env tiklandi"
fi

echo "==> Virtual muhit va paketlar"
source "$VENV_DIR/bin/activate"
pip install -r requirements.txt

echo "==> Migratsiya va statik fayllar"
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "==> Gunicorn qayta ishga tushirish"
sudo systemctl restart hamdprint

echo "Deploy tugadi."
