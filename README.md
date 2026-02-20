# Microservice App (Flask + Nginx + Redis + Postgres)

## About the project

This is a production-like microservice application:

- `Flask` — application
- `Nginx` — reverse proxy (entry point)
- `Redis` — state (counter)
- `Postgres` — database (connected, not yet used by the application)
- `Docker Compose` — infrastructure orchestration

## Architecture

```text
User -> Nginx -> Flask -> Redis
                       -> Postgres (not yet used)
```

- External access: `Nginx:80`
- `Flask` only works on the internal Docker network (`flweb:5000`)
- Internal services are hidden behind a reverse proxy

## Components

### Flask (`flweb`)

- Returns the main page: `/`
- Has an endpoint: `/counter`
- Stores the counter state in Redis
- This is the business logic layer

### Nginx

- Accepts HTTP requests on port `80`
- Proxies requests to `flweb:5000`
- Hides the internal architecture of the application

### Redis

- Stores the counter between requests
- Makes the application stateful
- Used by Flask via the internal Docker network

### Postgres

- The database service is running in the infrastructure
- Prepared for the next stage (integration with the application)

## What you can do

- Open the application via `http://localhost`
- Check the reverse proxy (`Nginx -> Flask`)
- Call `/counter` and see the state saved in Redis between requests
- Check inter-service interaction in the Docker network
- Extend the application by adding Flask with Postgres

## Launch

```bash
docker compose up --build
```

After launch:

- Home page: `http://localhost/`
- Counter: `http://localhost/counter`

## Project goal

Assemble and test a small production-like stack with separation of service roles and external access via a reverse proxy.
