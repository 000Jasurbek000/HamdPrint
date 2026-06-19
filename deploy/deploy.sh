#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/var/www/hamdprint"
VENV_DIR="$APP_DIR/venv"
USER="www-data"

cd "$APP_DIR"

echo "==> Git yangilanish"
git pull origin main

echo "==> Virtual muhit va paketlar"
source "$VENV_DIR/bin/activate"
pip install -r requirements.txt

echo "==> Migratsiya va statik fayllar"
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "==> Gunicorn qayta ishga tushirish"
sudo systemctl restart hamdprint

echo "Deploy tugadi."
