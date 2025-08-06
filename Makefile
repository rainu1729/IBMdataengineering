.PHONY: help venv install clean run

help:
	@echo "Available options:"
	@echo "  help           - List out the available options"
	@echo "  venv           - Create a Python virtual environment"
	@echo "  install        - Install dependencies from requirements.txt"
	@echo "  clean          - Remove temp files in src/temp/"
	@echo "  test		    - Run unit tests"
	@echo "  run            - Execute src/main.py"
	@echo "  docker-build   - Build Docker image (future enhancement)"

VENV_DIR := venv
REQ := requirements.txt
SRC := src/main.py
TEMP_DIR := src/temp

venv:
	python3 -m venv $(VENV_DIR)
	@echo "Virtual environment created in $(VENV_DIR)"

install: venv
	$(VENV_DIR)/bin/pip install --upgrade pip
	$(VENV_DIR)/bin/pip install -r $(REQ)

run: install
	$(VENV_DIR)/bin/python -m src.main

clean:
	rm -rf $(TEMP_DIR)/*

test: install
	$(VENV_DIR)/bin/python -m pytest --maxfail=5 --disable-warnings -q

# Future enhancements
# docker-build:
#	docker build -t ibmdataengineering .