.PHONY: up down logs build db-init migrate shell-core shell-db

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

build:
	docker-compose build

db-init:
	docker-compose exec postgres psql -U $${POSTGRES_USER:-postgres} -d $${POSTGRES_DB:-ethio_council} -f /docker-entrypoint-initdb.d/init.sql

migrate:
	docker-compose exec core-platform-service alembic upgrade head

shell-core:
	docker-compose exec core-platform-service /bin/sh

shell-db:
	docker-compose exec postgres psql -U $${POSTGRES_USER:-postgres} -d $${POSTGRES_DB:-ethio_council}
