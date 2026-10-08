# Микросервисное приложение (Flask + Nginx + Redis + Postgres)

> 🌐 **Язык:** [English](README.md) | **Русский**

## О проекте

Продакшн-подобное микросервисное приложение с чётким разделением зон
ответственности:

- **Flask** (`flweb`) — приложение / бизнес-логика
- **Nginx** — reverse proxy и точка входа (порты 80/443)
- **Redis** — in-memory хранилище состояния (счётчик)
- **Postgres** — реляционная база данных
- **Docker Compose** — оркестрация инфраструктуры

Приложение демонстрирует:

- Внешний доступ только через reverse proxy
- Внутренние сервисы скрыты от внешнего мира
- Совместную работу stateless- и stateful-сервисов
- Security best practices для контейнеризированных окружений
- Конфигурацию в стиле 12-factor через переменные окружения

## Архитектура

Внешние клиенты → `Nginx:80/443` → `Flask (flweb:5000)`  
`Flask` ↔ `Redis` (состояние/счётчик)  
`Flask` ↔ `Postgres` (проверка доступности на `/health`)

![Архитектура](https://i.ibb.co/chZxCLnC/1.png)

Всё внутреннее общение идёт по Docker-сети.  
Пользовательский трафик входит через Nginx; интерфейсы observability
(Prometheus `:9090`, Grafana `:3001`, Loki `:3100`) открыты для локального
использования.

## Компоненты

### Nginx

- Слушает порты 80 (HTTP → редирект) и 443 (HTTPS)
- Проксирует запросы на `flweb:5000`
- Добавляет security-заголовки
- Скрывает внутреннюю структуру сервисов

### Flask (`flweb`)

- Отдаёт:
  - `/` — главная страница
  - `/counter` — пример инкрементирующегося счётчика
  - `/health` — health check Redis + Postgres (JSON)
  - `/metrics` — метрики для Prometheus
- Хранит значение счётчика в **Redis**
- Проверяет доступность **Postgres** на `/health`
- Работает под **Gunicorn** (не под dev-сервером Flask)

### Redis

- Хранит состояние счётчика между запросами
- Персистентность сознательно отключена (`--save "" --appendonly no`)  
  → минимум данных на диске (security choice)

### Postgres

- Хранит реляционные данные; доступность проверяется на `/health`
- Реквизиты передаются через Docker secrets (`secrets/` + fallback на `.env`)

## Наблюдаемость (мониторинг)

- **Prometheus** (`:9090`) скрапит `flask`, `nginx`-экспортёр и сам себя
  (джобы `cadvisor` / `node-exporter` — только для Linux, см. ниже)
- **Grafana** (`:3001`, `admin/admin`) — источники Prometheus + Loki и
  дашборд **Homelab overview** уже преднастроены (provisioning)
- **Loki** (`:3100`) собирает логи контейнеров через Promtail
  (полноценно работает на Linux-хостах, см. примечания)

## Базовая безопасность

- `.env` в git-игноре
- Все сервисы по возможности работают от **non-root** пользователей
- Контейнер `flweb`:
  - `cap_drop: ALL`
  - read-only корневая ФС + tmpfs для записываемых путей
  - `no-new-privileges: true`
- Nginx и flweb выставляют security-заголовки
- Redis без персистентности (принцип наименьших привилегий)

## Конфигурация (в стиле 12-Factor)

Вся конфигурация — через **переменные окружения**, конфиги в образы не
запекаются.

Основные переменные:

```text
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
DEBUG
REDIS_HOST
REDIS_PORT
GRAFANA_ADMIN_USER
GRAFANA_ADMIN_PASSWORD
```

Секреты (`secrets/db_*`) и локальный TLS-сертификат в git-игноре —
их создаёт `scripts/init-dev.sh` при первом запуске (см. Запуск).

## Запуск

```bash
./scripts/init-dev.sh   # один раз: создаёт git-ignored secrets/, локальный TLS-сертификат, webroot certbot'а
docker compose up --build
```

Или в фоне:

```bash
docker compose up --build -d
```

После старта:

- **Главная** → http://localhost/  
  ![Главная](https://i.ibb.co/ymvM7KrT/2.png)

- **Счётчик** (растёт при каждом обновлении) → http://localhost/counter  
  ![Счётчик](https://i.ibb.co/nM21tKPf/3.png)
