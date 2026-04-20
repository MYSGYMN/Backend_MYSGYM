SHELL := /bin/bash

COMPOSE := docker compose
SERVICE := mysql
CONTAINER := mysql-gym
BACKUP_DIR := backups
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: help up down restart logs ps mysql-root mysql-app backup seed venv install install-dev flask-run flask-shell

help:
	@echo "Comandos disponibles:"
	@echo ""
	@echo "Base de datos (MySQL):"
	@echo "  make up         - Levanta MySQL con Compose"
	@echo "  make down       - Baja el stack"
	@echo "  make restart    - Reinicia el stack"
	@echo "  make logs       - Muestra logs de MySQL"
	@echo "  make ps         - Muestra estado de servicios"
	@echo "  make mysql-root - Abre consola MySQL como root"
	@echo "  make mysql-app  - Abre consola MySQL como app_user"
	@echo "  make backup     - Genera dump SQL en backups/"
	@echo "  make seed       - Carga datos de prueba desde seeds/seed.sql"
	@echo ""
	@echo "Python/Flask:"
	@echo "  make venv       - Crea entorno virtual"
	@echo "  make install    - Instala dependencias"
	@echo "  make install-dev - Instala dependencias + dev"
	@echo "  make flask-run  - Levanta servidor Flask (puerto 5000)"
	@echo "  make flask-shell - Abre shell de Flask"

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

restart: down up

logs:
	$(COMPOSE) logs -f $(SERVICE)

ps:
	$(COMPOSE) ps

mysql-root:
	docker exec -it $(CONTAINER) mysql -u root -p

mysql-app:
	docker exec -it $(CONTAINER) mysql -u app_user -p gimnasio

backup:
	@mkdir -p $(BACKUP_DIR)
	@docker exec $(CONTAINER) sh -c 'mysqldump -u root -p"$$MYSQL_ROOT_PASSWORD" "$$MYSQL_DATABASE"' > $(BACKUP_DIR)/gimnasio_$$(date +%F_%H-%M-%S).sql
	@echo "Backup generado en $(BACKUP_DIR)/"

seed:
	@set -a; source .env; set +a; docker exec -i $(CONTAINER) mysql -u root -p"$$MYSQL_ROOT_PASSWORD" "$$MYSQL_DATABASE" < seeds/seed.sql
	@echo "Seed cargado desde seeds/seed.sql"

venv:
	python3 -m venv $(VENV)
	@echo "Entorno virtual creado en $(VENV)/"

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Dependencias instaladas"

install-dev: install
	$(PIP) install pytest pytest-cov black flake8

flask-run:
	$(PYTHON) run.py

flask-shell:
	$(PYTHON) -c "from app import create_app; app = create_app(); app.app_context().push(); import code; code.interact(local=locals())"
