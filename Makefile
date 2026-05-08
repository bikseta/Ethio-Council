.PHONY: up down build logs validate shell-db

up:
	docker-compose up -d --build

down:
	docker-compose down

build:
	docker-compose build

logs:
	docker-compose logs --tail=200

validate:
	python -m compileall services
	cd frontend && npm run build

shell-db:
	docker-compose exec db psql -U ecfe_user -d ecfe_db
