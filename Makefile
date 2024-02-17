# Nome da imagem no GitHub Container Registry
IMAGE_NAME=ghcr.io/datacosmos-br/odooconnectorapi
# Tag da imagem
TAG=latest

# Caminho para os diretórios de aplicação e teste
APP_DIR=app
ODOO_DIR=odoo

# Docker e Python commands
DOCKER_CMD=docker
PYTHON_CMD=python
FLAKE8_CMD=flake8
PYLINT_CMD=pylint

# Build the Docker image
build:
	@$(DOCKER_CMD) build -t $(IMAGE_NAME):$(TAG) .

# Run the Docker container
run:
	@$(DOCKER_CMD) run --rm -p 8069:8069 $(IMAGE_NAME):$(TAG)

# Push the Docker image to GitHub Container Registry
push:
	@$(DOCKER_CMD) push $(IMAGE_NAME):$(TAG)

# Run Python linting
lint:
	@$(PYLINT_CMD) $(APP_DIR)/*.py $(ODOO_DIR)/*.py

# Run Flake8 for style guide enforcement
flake8:
	@$(FLAKE8_CMD) $(APP_DIR)/*.py $(ODOO_DIR)/*.py

# Execute tests
test:
	@$(PYTHON_CMD) $(ODOO_DIR)/test_odoo_connection.py

# Help command to list available commands
help:
	@echo "Available commands:"
	@echo "  build    Build the Docker image"
	@echo "  run      Run the Docker container"
	@echo "  push     Push the Docker image to GitHub Container Registry"
	@echo "  lint     Run Python linting with Pylint"
	@echo "  flake8   Run Flake8 for style guide enforcement"
	@echo "  test     Execute tests"

# Create a Python distribution package
dist:
	@$(PYTHON_CMD) setup.py sdist

# Install dependencies from requirements.txt
install:
	@pip install -r requirements.txt

# Run Tox to test the project in multiple Python environments
tox:
	@tox

# Run coverage to measure code coverage
coverage:
	@coverage run --source $(APP_DIR) $(ODOO_DIR)
	@coverage report

# Run pylint with coverage
pylint-coverage:
	@pylint --rcfile=.pylintrc --output-format=colorized $(APP_DIR)/*.py $(ODOO_DIR)/*.py
	@coverage report

# Run flake8 with coverage
flake8-coverage:
	@flake8 --format=colorized $(APP_DIR)/*.py $(ODOO_DIR)/*.py
	@coverage report

# Run case tests
case-tests:
	@$(PYTHON_CMD) $(ODOO_DIR)/test_odoo_connection.py -c "import unittest; unittest.main()"