# Microservice App (Flask + Nginx + Redis + Postgres)

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

External clients → `Nginx:80` → `Flask (flweb:5000)`  
`Flask` ↔ `Redis` (state/counter)  
`Flask` can connect to `Postgres` (prepared but not yet used)

![Architecture diagram](https://i.ibb.co/chZxCLnC/1.png)

All internal communication happens over the Docker network.  
External ports (except Nginx 80) are not exposed.

## Components

### Nginx
- Listens on port 80
- Proxies requests to `flweb:5000`
- Adds security headers
- Hides internal service structure

### Flask (`flweb`)
- Serves:
  - `/` — main page
  - `/counter` — incrementing counter example
- Uses **Redis** to persist counter value
- Runs with **Gunicorn** (not Flask dev server)
- Prepared for future Postgres integration

### Redis
- Stores counter state between requests
- Persistence intentionally disabled (`--save "" --appendonly no`)  
  → minimal data at rest (security choice)

### Postgres
- Database service is running
- Ready for next steps (schema creation, Flask-SQLAlchemy integration, etc.)

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
```

For local development:

```bash
cp .env.example .env
# then edit .env if needed
```

## Launch

```bash
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

