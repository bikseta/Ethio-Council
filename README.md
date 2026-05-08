# Ethio-Council

Ethio-Council is the National Digital Platform for the Evangelical Churches Fellowship of Ethiopia (ECFE). It provides a multilingual church registry, GIS-enabled field registration, analytics dashboards, diaspora partnership workflows, and crisis response coordination.

## Services

- **core-platform-service** (`8001`) - authentication, church registry, denominations, ministries, leaders, admin hierarchy, diaspora
- **gis-registration-service** (`8002`) - GPS field registration, map feeds, photo metadata
- **analytics-service** (`8003`) - dashboard KPIs and summary reports
- **crisis-response-service** (`8004`) - incidents, volunteers, relief distributions
- **frontend** (`3001`) - React 19 + TypeScript + MUI + Mapbox GL + i18next PWA
- **postgres** (`5434`) - PostgreSQL 15 + PostGIS
- **localstack** (`4566`) - AWS emulation for local development

## Quick start

1. Copy `.env.example` to `.env` and update secrets.
2. Build the stack with `make build`.
3. Start locally with `make up`.
4. Run database initialization with `make db-init` if needed.
5. Apply migrations with `make migrate`.

## Environment variables

Root environment variables are defined in `.env.example`.

Frontend environment variables:

- `REACT_APP_CORE_API_URL`
- `REACT_APP_GIS_API_URL`
- `REACT_APP_ANALYTICS_API_URL`
- `REACT_APP_CRISIS_API_URL`
- `REACT_APP_MAPBOX_TOKEN`

## Internationalization

The frontend supports:

- English (`en`)
- Amharic (`am`)
- Afaan Oromo (`om`)

## Notes

- All services expose `/health` endpoints.
- Core platform authentication uses JWT with `python-jose` and `passlib[bcrypt]`.
- The platform uses PostGIS geometries for church, registration, and incident mapping.
