# Ethio-Council — ECFE Digital Platform

Digital scaffold for the **Evangelical Churches Fellowship of Ethiopia (ECFE)** platform.

## Services

| Service | Port | Description |
|---------|------|-------------|
| core-platform-service | 8000 | Authentication, churches, ministries, denominations, leaders, hierarchy, diaspora |
| gis-registration-service | 8001 | GIS-based field registration and geo metadata |
| crisis-response-service | 8002 | Incident, volunteer, and relief coordination |
| analytics-service | 8003 | Platform analytics and dashboard aggregation |
| frontend | 3001 | React + TypeScript management portal |
| db | 5432 | PostgreSQL 15 shared datastore |

## Quick Start

```bash
cp .env.example .env
docker-compose up --build
```

## Seed Login

- **Username:** `admin`
- **Email:** `admin@ecfe.org`
- **Password:** `Admin@2024!`

## Core API Areas

- `/api/v1/auth`
- `/api/v1/churches`
- `/api/v1/ministries`
- `/api/v1/denominations`
- `/api/v1/leaders`
- `/api/v1/hierarchy`
- `/api/v1/diaspora`

## Service Directories

- `services/core-platform-service`
- `services/gis-registration-service`
- `services/analytics-service`
- `services/crisis-response-service`
