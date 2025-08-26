# Makefile
# Robust venv + pinned installs + linters

SHELL := /bin/bash
VENV_DIR := $(HOME)/.devops
PY := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
PYLINT := $(VENV_DIR)/bin/pylint

.PHONY: setup install test lint all dev clean

setup:
	# Create python virtualenv (idempotent)
	python3 -m venv $(VENV_DIR)
	# Ensure pip/setuptools/wheel are sane (avoid numpy-from-source issues)
	$(PY) -m pip install --upgrade "pip>=23,<25" "setuptools<75" wheel

install: setup
	# Install runtime deps with constraints to force binary NumPy on Py3.9
	$(PIP) install -r requirements.txt -c constraints.txt
	# Ensure pylint available for lint target (if not in requirements.txt)
	$(PIP) install --upgrade pylint

test:
	# (Optional) add your tests here
	# $(PY) -m pytest -vv --cov=myrepolib tests/*.py
	@echo "No tests defined."

lint:
	# Dockerized hadolint (no local install needed). Requires Docker.
	# If you have native hadolint, comment the docker line and uncomment the next one.
	docker run --rm -i hadolint/hadolint < Dockerfile
	# hadolint Dockerfile
	# Python linter
	$(PYLINT) --disable=R,C,W1203,W1202 app.py

dev: install
	# Add any dev-only tools you want here
	@echo "Dev tools ready."

clean:
	# Remove the venv if you need a fresh start
	rm -rf $(VENV_DIR)

all: install lint test