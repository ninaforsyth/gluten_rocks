.PHONY: up down restart logs test install-test-deps open help

# ---- Config ----
COMPOSE   := docker compose
CONTAINER := gluten-rocks
BASE_URL  := http://localhost:8080

# ---- Default target ----
help:
	@echo ""
	@echo "  gluten.rocks — available commands"
	@echo ""
	@echo "  make up              Start the site locally (http://localhost:8080)"
	@echo "  make down            Stop and remove containers"
	@echo "  make restart         Restart the container"
	@echo "  make logs            Tail nginx logs"
	@echo "  make install-test    Install Python test dependencies"
	@echo "  make test            Run the full test suite"
	@echo "  make open            Open the site in your default browser"
	@echo ""

up:
	@echo "Starting gluten.rocks..."
	$(COMPOSE) up -d --build
	@echo "Site running at $(BASE_URL)"

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) restart $(CONTAINER)

logs:
	$(COMPOSE) logs -f $(CONTAINER)

install-test:
	pip install -r tests/requirements.txt

test: up
	@echo "Waiting for site to be ready..."
	@sleep 2
	@BASE_URL=$(BASE_URL) pytest tests/test_site.py -v

open:
	@open $(BASE_URL) 2>/dev/null || xdg-open $(BASE_URL)
