# BUKHARA HAMD PRINT

Django asosidagi nashriyot veb-sayti — kitoblar katalogi, yangiliklar, maqolalar va admin panel.

## Texnologiyalar

- Python 3.11+
- Django 5.2
- PostgreSQL
- Gunicorn + Nginx (production)
- WhiteNoise (statik fayllar)
- Jazzmin (admin panel)

## Lokal ishga tushirish

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/macOS

pip install -r requirements.txt
copy .env.example .env         # Windows
# cp .env.example .env         # Linux

# .env faylida DB parolini va SECRET_KEY ni to'ldiring
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Sayt: http://127.0.0.1:8000/  
Admin: http://127.0.0.1:8000/admin/

## GitHub ga yuklash

1. GitHub da yangi repository yarating (masalan: `hamdprint`)
2. Lokal repoda:

```bash
git init
git add .
git commit -m "Initial commit: HAMDPRINT Django sayti"
git branch -M main
git remote add origin https://github.com/SIZNING_USERNAME/hamdprint.git
git push -u origin main
```

> `.env` fayli git ga kirmaydi — parollar faqat serverda saqlanadi.

## Serverga deploy (Ubuntu + Nginx)

### 1. Server tayyorlash

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip nginx postgresql postgresql-contrib git
```

### 2. PostgreSQL

```bash
sudo -u postgres psql
CREATE DATABASE hamdprint;
CREATE USER hamdprint_user WITH PASSWORD 'kuchli_parol';
GRANT ALL PRIVILEGES ON DATABASE hamdprint TO hamdprint_user;
\q
```

### 3. Loyihani klonlash

```bash
sudo mkdir -p /var/www/hamdprint
sudo chown $USER:$USER /var/www/hamdprint
git clone https://github.com/SIZNING_USERNAME/hamdprint.git /var/www/hamdprint
cd /var/www/hamdprint

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Muhit o'zgaruvchilari

```bash
cp .env.example .env
nano .env
```

Production uchun `.env` namunasi:

```env
DJANGO_SECRET_KEY=uzun-tasodifiy-kalit
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com,server-ip
DJANGO_CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com
DJANGO_SECURE_SSL_REDIRECT=True

DB_NAME=hamdprint
DB_USER=hamdprint_user
DB_PASSWORD=kuchli_parol
DB_HOST=localhost
DB_PORT=5432
```

### 5. Django sozlash

```bash
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 6. Gunicorn (systemd)

```bash
sudo cp deploy/hamdprint.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable hamdprint
sudo systemctl start hamdprint
```

### 7. Nginx

```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/hamdprint
sudo ln -s /etc/nginx/sites-available/hamdprint /etc/nginx/sites-enabled/
# nginx.conf ichida server_name ni o'z domeningizga o'zgartiring
sudo nginx -t
sudo systemctl reload nginx
```

### 8. SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### Keyingi yangilanishlar

Serverda:

```bash
cd /var/www/hamdprint
bash deploy/deploy.sh
```

## Loyiha tuzilmasi

```
HAMDPRINT/
├── config/          # Django sozlamalari
├── core/            # Bosh sahifa, qidiruv, aloqa
├── catalog/         # Kitoblar, mualliflar
├── blog/            # Yangiliklar, maqolalar
├── accounts/        # Foydalanuvchi hisobi
├── templates/       # HTML shablonlar
├── static/          # CSS, JS, rasmlar
├── deploy/          # Nginx, systemd, deploy skript
└── manage.py
```

## Admin panel

Kitoblar, kategoriyalar, yangiliklar va maqolalarni `/admin/` orqali boshqaring.  
Bosh sahifa matnlari shablonda doimiy; faqat kitob sonlari avtomatik yangilanadi.

## Xavfsizlik

- `.env` faylini hech qachon git ga qo'shmang
- Production da `DJANGO_DEBUG=False` bo'lishi shart
- `DJANGO_SECRET_KEY` ni har bir muhit uchun alohida yarating
