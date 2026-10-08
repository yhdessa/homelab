# Microservice App (Flask + Nginx + Redis + Postgres)

> 🌐 **Language:** English | [Русский](README.ru.md)

## About the project

Production-like microservice application with clear separation of concerns:

- **Flask** (`flweb`) — application / business logic
- **Nginx** — reverse proxy & entry point (port 80)
- **Redis** — in-memory state storage (counter)
- **Postgres** — relational database (running, ready for future integration)
- **Docker Compose** — infrastructure orchestration

The app demonstrates:
- External access only through reverse proxy
- Internal services hidden from the outside world
- Stateless + stateful services working together
- Security best practices for containerized environments
- 12-factor configuration via environment variables

## Architecture

External clients → `Nginx:80/443` → `Flask (flweb:5000)`  
`Flask` ↔ `Redis` (state/counter)  
`Flask` ↔ `Postgres` (health-checked on `/health`)

![Architecture diagram](https://i.ibb.co/chZxCLnC/1.png)

All internal communication happens over the Docker network.  
User traffic enters through Nginx; observability UIs
(Prometheus `:9090`, Grafana `:3001`, Loki `:3100`) are exposed for local use.

## Components

### Nginx
- Listens on ports 80 (HTTP → redirect) and 443 (HTTPS)
- Proxies requests to `flweb:5000`
- Adds security headers
- Hides internal service structure

### Flask (`flweb`)
- Serves:
  - `/` — main page
  - `/counter` — incrementing counter example
  - `/health` — Redis + Postgres health check (JSON)
  - `/metrics` — Prometheus metrics
- Uses **Redis** to persist counter value
- Checks **Postgres** connectivity on `/health`
- Runs with **Gunicorn** (not Flask dev server)

### Redis
- Stores counter state between requests
- Persistence intentionally disabled (`--save "" --appendonly no`)  
  → minimal data at rest (security choice)

### Postgres
- Stores relational data; connectivity is verified on `/health`
- Credentials are injected via Docker secrets (`secrets/` + `.env` fallback)

## Observability

- **Prometheus** (`:9090`) scrapes `flask`, `nginx` exporter and itself
  (`cadvisor` / `node-exporter` jobs are Linux-only, see below)
- **Grafana** (`:3001`, `admin/admin`) ships pre-provisioned Prometheus +
  Loki datasources and the **Homelab overview** dashboard
- **Loki** (`:3100`) collects container logs via Promtail
  (works fully on Linux hosts; see notes below)

## Security baseline

- `.env` is git-ignored
- All services run as **non-root** users where possible
- `flweb` container:
  - `cap_drop: ALL`
  - read-only root filesystem + tmpfs mounts for writable paths
  - `no-new-privileges: true`
- Nginx & flweb use security headers
- Redis without persistence (least privilege principle)

## Configuration (12-Factor style)

All configuration comes from **environment variables** — no config files baked into images.

Required / commonly used variables:

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

Secrets (`secrets/db_*`) and the local TLS cert are git-ignored —
`scripts/init-dev.sh` creates them on first run (see Launch).

## Launch

```bash
./scripts/init-dev.sh   # one-time: creates git-ignored secrets/, local TLS cert, certbot webroot
docker compose up --build
```

Or in detached mode:

```bash
docker compose up --build -d
```

After startup:

- **Home page** → http://localhost/  
  ![Home page](https://i.ibb.co/ymvM7KrT/2.png)

- **Counter** (increments on each refresh) → http://localhost/counter  
  ![Counter page](https://i.ibb.co/nM21tKPf/3.png)

