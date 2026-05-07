# Ethio-Council ECFE Digital Platform Makefile

.PHONY: help setup start stop restart status logs clean test migrate

help:
	@echo ""
	@echo "Ethio-Council ECFE Digital Platform"
	@echo "====================================="
	@echo "Available commands:"
	@echo "  setup     - Set up and start the entire platform"
	@echo "  start     - Start all services"
	@echo "  stop      - Stop all services"
	@echo "  restart   - Restart all services"
	@echo "  status    - Show service status"
	@echo "  logs      - Show logs for all services"
	@echo "  test      - Run basic health tests"
	@echo "  clean     - Clean up everything (including data)"
	@echo "  migrate   - Run Alembic migrations"
	@echo ""
	@echo "Development commands:"
	@echo "  dev-logs SERVICE=name    - Show logs for specific service"
	@echo "  dev-shell SERVICE=name   - Open shell in service"
	@echo "  dev-rebuild SERVICE=name - Rebuild specific service"
	@echo ""

setup:
	@echo "🚀 Setting up Ethio-Council platform..."
	@cp -n .env.example .env || true
	@docker-compose up -d --build

start:
	@echo "🚀 Starting services..."
	@docker-compose up -d

stop:
	@echo "🛑 Stopping services..."
	@docker-compose down

restart:
	@echo "🔄 Restarting services..."
	@docker-compose restart

status:
	@echo "📊 Service Status:"
	@docker-compose ps

logs:
	@docker-compose logs -f

test:
	@echo "🧪 Running health checks..."
	@curl -sf http://localhost:8001/health && echo " core-platform-service: OK" || echo " core-platform-service: FAIL"
	@curl -sf http://localhost:8002/health && echo " gis-service: OK" || echo " gis-service: FAIL"
	@curl -sf http://localhost:8003/health && echo " analytics-service: OK" || echo " analytics-service: FAIL"
	@curl -sf http://localhost:8004/health && echo " crisis-service: OK" || echo " crisis-service: FAIL"

clean:
	@echo "🧹 Cleaning up everything..."
	@docker-compose down -v
	@docker system prune -f
	@rm -rf logs/ data/
	@echo "Cleanup complete"

migrate:
	@echo "📦 Running Alembic migrations..."
	@docker-compose exec core-platform-service alembic upgrade head

dev-logs:
	@docker-compose logs -f $(SERVICE)

dev-shell:
	@docker-compose exec $(SERVICE) /bin/bash

dev-rebuild:
	@docker-compose up -d --build $(SERVICE)

dev-psql:
	@docker-compose exec postgres psql -U postgres -d ethio_council
