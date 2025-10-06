# 🚀 Руководство по развертыванию ГАРАНТ СДЕЛОК 3.0

## 📋 Предварительные требования

### Системные требования:
- **Python 3.8+**
- **Node.js 16+** (для фронтенда)
- **PostgreSQL 13+** (для продакшена)
- **Redis 6+** (для кэширования)
- **Nginx** (для веб-сервера)

### Облачные платформы:
- **VPS/Cloud**: DigitalOcean, AWS, Google Cloud, Vultr
- **База данных**: PostgreSQL, MongoDB Atlas
- **Кэширование**: Redis Cloud, AWS ElastiCache
- **CDN**: Cloudflare, AWS CloudFront

## 🏗️ Архитектура развертывания

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Лендинг       │    │  Telegram Bot   │    │   AI System     │
│   (Tilda/HTML)  │◄──►│   (Python)      │◄──►│   (Python)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CDN/Static    │    │   PostgreSQL    │    │     Redis       │
│   (Cloudflare)  │    │   (Database)    │    │   (Cache)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Пошаговое развертывание

### 1. Подготовка сервера

#### Ubuntu/Debian:
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка необходимых пакетов
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib redis-server git

# Создание пользователя для приложения
sudo adduser --system --group --shell /bin/bash garant
sudo usermod -aG sudo garant
```

#### CentOS/RHEL:
```bash
# Обновление системы
sudo yum update -y

# Установка необходимых пакетов
sudo yum install -y python3 python3-pip nginx postgresql-server postgresql-contrib redis git

# Инициализация PostgreSQL
sudo postgresql-setup initdb
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

### 2. Настройка базы данных

```bash
# Переключение на пользователя postgres
sudo -u postgres psql

# Создание базы данных и пользователя
CREATE DATABASE garant_sdelok;
CREATE USER garant_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE garant_sdelok TO garant_user;
\q
```

### 3. Клонирование и настройка проекта

```bash
# Переключение на пользователя приложения
sudo su - garant

# Клонирование репозитория
git clone https://github.com/your-username/garant-sdelok-3.0.git
cd garant-sdelok-3.0

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

### 4. Настройка конфигурации

```bash
# Создание файла конфигурации
cp .env.example .env
nano .env
```

#### Пример конфигурации `.env`:
```env
# Telegram Bot
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
WEBHOOK_URL=https://your-domain.com/webhook

# Database
DATABASE_URL=postgresql://garant_user:secure_password@localhost/garant_sdelok

# Redis
REDIS_URL=redis://localhost:6379/0

# AI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
AI_MODEL=gpt-3.5-turbo

# Blockchain (опционально)
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/your-project-id
PRIVATE_KEY=your-private-key-here

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here

# Monitoring
SENTRY_DSN=your-sentry-dsn-here
```

### 5. Настройка Nginx

```bash
# Создание конфигурации сайта
sudo nano /etc/nginx/sites-available/garant-sdelok
```

#### Конфигурация Nginx:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Лендинг
    location / {
        root /home/garant/garant-sdelok-3.0;
        index garant-sdelok-3.0.html;
        try_files $uri $uri/ =404;
    }
    
    # Webhook для бота
    location /webhook {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # API для AI системы
    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Статические файлы
    location /static/ {
        alias /home/garant/garant-sdelok-3.0/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Активация сайта
sudo ln -s /etc/nginx/sites-available/garant-sdelok /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 6. Настройка SSL (Let's Encrypt)

```bash
# Установка Certbot
sudo apt install certbot python3-certbot-nginx

# Получение SSL сертификата
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Автоматическое обновление
sudo crontab -e
# Добавить строку:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

### 7. Создание systemd сервисов

#### Telegram Bot:
```bash
sudo nano /etc/systemd/system/garant-bot.service
```

```ini
[Unit]
Description=Garant Sdelok Telegram Bot
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=garant
Group=garant
WorkingDirectory=/home/garant/garant-sdelok-3.0
Environment=PATH=/home/garant/garant-sdelok-3.0/venv/bin
ExecStart=/home/garant/garant-sdelok-3.0/venv/bin/python telegram_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### AI System:
```bash
sudo nano /etc/systemd/system/garant-ai.service
```

```ini
[Unit]
Description=Garant Sdelok AI System
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=garant
Group=garant
WorkingDirectory=/home/garant/garant-sdelok-3.0
Environment=PATH=/home/garant/garant-sdelok-3.0/venv/bin
ExecStart=/home/garant/garant-sdelok-3.0/venv/bin/python ai_integration.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 8. Запуск сервисов

```bash
# Перезагрузка systemd
sudo systemctl daemon-reload

# Включение автозапуска
sudo systemctl enable garant-bot
sudo systemctl enable garant-ai
sudo systemctl enable nginx
sudo systemctl enable postgresql
sudo systemctl enable redis

# Запуск сервисов
sudo systemctl start garant-bot
sudo systemctl start garant-ai
sudo systemctl start nginx
sudo systemctl start postgresql
sudo systemctl start redis

# Проверка статуса
sudo systemctl status garant-bot
sudo systemctl status garant-ai
```

## 🔧 Настройка мониторинга

### 1. Установка Prometheus и Grafana

```bash
# Создание пользователя для мониторинга
sudo useradd --no-create-home --shell /bin/false prometheus
sudo useradd --no-create-home --shell /bin/false grafana

# Создание директорий
sudo mkdir /etc/prometheus
sudo mkdir /var/lib/prometheus
sudo chown prometheus:prometheus /etc/prometheus
sudo chown prometheus:prometheus /var/lib/prometheus
```

### 2. Настройка логирования

```bash
# Создание директории для логов
sudo mkdir -p /var/log/garant-sdelok
sudo chown garant:garant /var/log/garant-sdelok

# Настройка logrotate
sudo nano /etc/logrotate.d/garant-sdelok
```

```bash
/var/log/garant-sdelok/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 garant garant
    postrotate
        systemctl reload garant-bot
        systemctl reload garant-ai
    endscript
}
```

## 🚀 Развертывание в облаке

### DigitalOcean App Platform

1. **Создание приложения:**
```yaml
# .do/app.yaml
name: garant-sdelok-3.0
services:
- name: telegram-bot
  source_dir: /
  github:
    repo: your-username/garant-sdelok-3.0
    branch: main
  run_command: python telegram_bot.py
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: BOT_TOKEN
    value: ${BOT_TOKEN}
  - key: DATABASE_URL
    value: ${DATABASE_URL}
  - key: REDIS_URL
    value: ${REDIS_URL}

- name: ai-system
  source_dir: /
  github:
    repo: your-username/garant-sdelok-3.0
    branch: main
  run_command: python ai_integration.py
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: OPENAI_API_KEY
    value: ${OPENAI_API_KEY}
  - key: DATABASE_URL
    value: ${DATABASE_URL}

databases:
- name: garant-db
  engine: PG
  version: "13"
  size: db-s-1vcpu-1gb

static_sites:
- name: landing
  source_dir: /
  github:
    repo: your-username/garant-sdelok-3.0
    branch: main
  build_command: echo "Static site"
  output_dir: /
  routes:
  - path: /
    name: landing
```

### Docker развертывание

#### Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "telegram_bot.py"]
```

#### docker-compose.yml:
```yaml
version: '3.8'

services:
  telegram-bot:
    build: .
    command: python telegram_bot.py
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - DATABASE_URL=postgresql://postgres:password@db:5432/garant_sdelok
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    restart: unless-stopped

  ai-system:
    build: .
    command: python ai_integration.py
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://postgres:password@db:5432/garant_sdelok
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=garant_sdelok
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:6-alpine
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./garant-sdelok-3.0.html:/usr/share/nginx/html/index.html
    depends_on:
      - telegram-bot
      - ai-system
    restart: unless-stopped

volumes:
  postgres_data:
```

## 🔒 Безопасность

### 1. Настройка файрвола

```bash
# UFW
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw allow 5432  # PostgreSQL (только для внутренней сети)
sudo ufw allow 6379  # Redis (только для внутренней сети)
```

### 2. Настройка fail2ban

```bash
sudo apt install fail2ban

# Конфигурация для Nginx
sudo nano /etc/fail2ban/jail.local
```

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[nginx-limit-req]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 10
```

### 3. Настройка SSL/TLS

```bash
# Дополнительная безопасность SSL
sudo nano /etc/nginx/snippets/ssl-params.conf
```

```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
add_header Strict-Transport-Security "max-age=63072000" always;
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
```

## 📊 Мониторинг и логирование

### 1. Настройка Sentry

```python
# В telegram_bot.py
import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    integrations=[AioHttpIntegration()],
    traces_sample_rate=1.0,
)
```

### 2. Настройка логирования

```python
# logging_config.py
import logging
import logging.handlers
import os

def setup_logging():
    # Создание директории для логов
    os.makedirs('/var/log/garant-sdelok', exist_ok=True)
    
    # Настройка root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.handlers.RotatingFileHandler(
                '/var/log/garant-sdelok/bot.log',
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )
```

## 🚀 Автоматическое развертывание

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /home/garant/garant-sdelok-3.0
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          sudo systemctl restart garant-bot
          sudo systemctl restart garant-ai
```

## ✅ Проверка развертывания

### 1. Проверка сервисов

```bash
# Статус всех сервисов
sudo systemctl status garant-bot garant-ai nginx postgresql redis

# Проверка логов
sudo journalctl -u garant-bot -f
sudo journalctl -u garant-ai -f

# Проверка портов
sudo netstat -tlnp | grep -E ':(80|443|5432|6379)'
```

### 2. Тестирование функциональности

```bash
# Тест лендинга
curl -I http://your-domain.com

# Тест API
curl -X POST http://your-domain.com/api/analyze-risk \
  -H "Content-Type: application/json" \
  -d '{"amount": 1000, "asset": "btc"}'

# Тест базы данных
psql -h localhost -U garant_user -d garant_sdelok -c "SELECT 1;"
```

### 3. Нагрузочное тестирование

```bash
# Установка Apache Bench
sudo apt install apache2-utils

# Тест лендинга
ab -n 1000 -c 10 http://your-domain.com/

# Тест API
ab -n 100 -c 5 -p test_data.json -T application/json http://your-domain.com/api/analyze-risk
```

## 🔧 Обслуживание

### 1. Резервное копирование

```bash
# Скрипт резервного копирования
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/garant-sdelok"

# Создание директории
mkdir -p $BACKUP_DIR

# Резервное копирование базы данных
pg_dump -h localhost -U garant_user garant_sdelok > $BACKUP_DIR/db_$DATE.sql

# Резервное копирование файлов
tar -czf $BACKUP_DIR/files_$DATE.tar.gz /home/garant/garant-sdelok-3.0

# Удаление старых бэкапов (старше 30 дней)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

### 2. Мониторинг производительности

```bash
# Скрипт мониторинга
#!/bin/bash
# monitor.sh

# Проверка использования CPU
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)

# Проверка использования памяти
MEM_USAGE=$(free | grep Mem | awk '{printf("%.2f"), $3/$2 * 100.0}')

# Проверка места на диске
DISK_USAGE=$(df -h / | awk 'NR==2{print $5}' | cut -d'%' -f1)

# Отправка уведомления при превышении лимитов
if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
    echo "High CPU usage: $CPU_USAGE%"
fi

if (( $(echo "$MEM_USAGE > 80" | bc -l) )); then
    echo "High memory usage: $MEM_USAGE%"
fi

if [ $DISK_USAGE -gt 80 ]; then
    echo "High disk usage: $DISK_USAGE%"
fi
```

## 🎯 Масштабирование

### 1. Горизонтальное масштабирование

```yaml
# docker-compose.scale.yml
version: '3.8'

services:
  telegram-bot:
    deploy:
      replicas: 3
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}

  ai-system:
    deploy:
      replicas: 2
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}

  nginx:
    ports:
      - "80:80"
      - "443:443"
    # Load balancer конфигурация
```

### 2. Вертикальное масштабирование

```bash
# Увеличение ресурсов сервера
# 1. Остановка сервисов
sudo systemctl stop garant-bot garant-ai

# 2. Обновление конфигурации
sudo nano /etc/systemd/system/garant-bot.service
# Добавить:
# Environment=PYTHONUNBUFFERED=1
# Environment=OMP_NUM_THREADS=4

# 3. Перезапуск сервисов
sudo systemctl daemon-reload
sudo systemctl start garant-bot garant-ai
```

## 🎉 Готово!

Ваша система **ГАРАНТ СДЕЛОК 3.0** успешно развернута и готова к работе!

### Следующие шаги:
1. ✅ Настройте мониторинг
2. ✅ Настройте резервное копирование
3. ✅ Проведите нагрузочное тестирование
4. ✅ Настройте алерты
5. ✅ Документируйте процедуры

### Полезные команды:
```bash
# Перезапуск всех сервисов
sudo systemctl restart garant-bot garant-ai nginx

# Просмотр логов
sudo journalctl -u garant-bot -f

# Проверка статуса
sudo systemctl status garant-bot garant-ai

# Обновление кода
cd /home/garant/garant-sdelok-3.0 && git pull && sudo systemctl restart garant-bot garant-ai
```

**Удачи с вашим революционным проектом! 🚀**