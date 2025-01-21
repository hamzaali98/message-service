# Variables
UVICORN_CMD= .venv/bin/uvicorn app.main:app --reload
PYTHON_CMD= .venv/bin/python
DOTENV_CMD=dotenv

# Commands
setup-env:
	@bash setup_env.sh

run-local:
	@cp .env .env.current && $(UVICORN_CMD)

run-dev:
	@cp .env.dev .env.current && $(UVICORN_CMD)

check_db_connection:
	$(PYTHON_CMD) test_connection.py

clean-env:
	@rm -f .env.current

.PHONY: run-local run-dev check_db_connection install test lint migrate clean-env

