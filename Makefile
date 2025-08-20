.PHONY: help build up down test test-local test-verbose test-full clean format lint type-check quality debug

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

debug:
	@echo "Отладка pytest..."
	docker-compose exec task-manager bash -c "ls -la tests/"
	docker-compose exec task-manager bash -c "/app/.venv/bin/python -m pytest --collect-only tests/"
	docker-compose exec task-manager bash -c "find tests/ -name '*.py' -type f"

test-debug:
	docker-compose exec task-manager bash -c "/app/.venv/bin/python -m pytest tests/ -v"

test:
	docker-compose exec task-manager bash -c "/app/.venv/bin/python -m pytest tests/ -v --cov=src --cov-report=term-missing"

test-local:
	python3 -m pytest tests/ -v --cov=src --cov-report=term-missing || pytest tests/ -v --cov=src --cov-report=term-missing

test-verbose:
	docker-compose exec task-manager bash -c "/app/.venv/bin/python -m pytest tests/ -vvv --tb=long --show-capture=all --cov=src --cov-report=term-missing"

test-full:
	docker-compose up -d
	sleep 15
	docker-compose exec task-manager bash -c "/app/.venv/bin/python -m pytest tests/ -v --cov=src --cov-report=term-missing"

format:
	docker-compose exec task-manager bash -c "source .venv/bin/activate && black src/ tests/"
	docker-compose exec task-manager bash -c "source .venv/bin/activate && isort src/ tests/"

lint:
	docker-compose exec task-manager bash -c "source .venv/bin/activate && flake8 src/ tests/"
	docker-compose exec task-manager bash -c "source .venv/bin/activate && black --check src/ tests/"
	docker-compose exec task-manager bash -c "source .venv/bin/activate && isort --check-only src/ tests/"

type-check:
	docker-compose exec task-manager bash -c "source .venv/bin/activate && mypy src/"

quality: format lint type-check

clean:
	docker-compose down -v

help:
	@echo "Task Manager API - доступные команды:"
	@echo ""
	@echo "Docker команды:"
	@echo "  make up              - Запустить все сервисы"
	@echo "  make down            - Остановить все сервисы"
	@echo "  make build           - Собрать Docker образы"
	@echo "  make clean           - Очистить все контейнеры и volumes"
	@echo ""
	@echo "Тестирование:"
	@echo "  make test            - Запустить тесты в Docker"
	@echo "  make test-debug      - Запустить тесты без coverage"
	@echo "  make test-verbose    - Запустить тесты с подробным выводом"
	@echo "  make test-full       - Полный цикл: запуск + тесты"
	@echo ""
	@echo "Качество кода:"
	@echo "  make format          - Форматировать код (black, isort)"
	@echo "  make lint            - Проверить код линтером"
	@echo "  make type-check      - Проверить типы"
	@echo "  make quality         - Полная проверка качества"