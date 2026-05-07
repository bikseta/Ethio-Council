# Ethio-Council — ECFE Digital Platform

National Digital Platform for the **Evangelical Churches Fellowship of Ethiopia (ECFE)**.

## Services

| Service | Port | Description |
|---------|------|-------------|
| core-platform-service | 8001 | Auth, members, churches, admin |
| gis-service | 8002 | Geographic data & mapping |
| analytics-service | 8003 | Reports & analytics |
| crisis-service | 8004 | Crisis & emergency management |
| frontend | 3000 | React 19 + MUI web app |
| postgres | 5434 | PostGIS database |

## Quick Start

```bash
cp .env.example .env
# Edit .env and set POSTGRES_PASSWORD and SECRET_KEY
make setup
```

## Tech Stack

- **Backend**: FastAPI + SQLAlchemy 2.0 + Alembic + PostGIS
- **Frontend**: React 19 + TypeScript + MUI + Mapbox GL + i18next (EN/AM/OM)
- **Database**: PostgreSQL 15 + PostGIS 3.4
- **Container**: Docker Compose
