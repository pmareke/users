.DEFAULT_GOAL := help 

.PHONY: help
help:  ## Show this help.
	@grep -E '^\S+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

pre-requirements:
	@scripts/pre-requirements.sh

.PHONY: local-setup
local-setup: pre-requirements ## Sets up the local environment (e.g. install git hooks)
	scripts/local-setup.sh
	make install

.PHONY: build
build: ## Install the app packages
	docker build -f Dockerfile -t users .

.PHONY: up
up: ## Start the stack
	docker compose up

.PHONY: down
down: ## Stop the stack
	docker compose down

.PHONY: stop
stop: ## Stop running containers
	docker stop $$(docker ps -a -q)

.PHONY: install
install: pre-requirements ## Install the app packages
	uv python install 3.12.8
	uv python pin 3.12.8
	uv sync --no-install-project

.PHONY: update
update: pre-requirements ## Updates the app packages
	uv lock --upgrade

.PHONY: add-dev-package
add-dev-package: pre-requirements ## Installs a new package in the app. ex: make add-dev-package package=XXX
	uv add --dev $(package)

.PHONY: add-package
add-package: pre-requirements ## Installs a new package in the app. ex: make add-package package=XXX
	uv add $(package)

.PHONY: dev
dev: pre-requirements ## Runs the app in production mode
	fastapi dev

.PHONY: run
run: pre-requirements ## Runs the app in production mode
	fastapi run

.PHONY: check-typing
check-typing: pre-requirements  ## Run a static analyzer over the code to find issues
	ty check .

.PHONY: check-lint
check-lint: pre-requirements ## Checks the code style
	ruff check

.PHONY: check-format
check-format: pre-requirements  ## Check format python code
	ruff format --check

checks: check-typing check-lint check-format ## Run all checks

.PHONY: lint
lint: pre-requirements ## Lints the code format
	ruff check --fix

.PHONY: format
format: pre-requirements  ## Format python code
	ruff format

.PHONY: test-unit
test-unit:  ## Run tests.
	pytest tests -x -ra tests/unit

.PHONY: test-integration
test-integration: ## Run integration tests
	docker compose run --rm --entrypoint /code/integration-tests-entrypoint.sh api python -m pytest tests/integration -ra -x

test: test-unit test-integration ## Run all tests

.PHONY: migration
migration: ## Generate a new migration, ex: make migration name=XXX
	docker compose run --build --rm --entrypoint alembic api revision --autogenerate -m $(name)

.PHONY: pre-commit
pre-commit: pre-requirements check-lint check-format check-typing test
