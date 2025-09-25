.PHONY: help venv install clean run

help:
	@echo "Available options:"
	@echo "  help           - List out the available options"
	@echo "  clean          - Remove temp files in src/temp/"
	@echo "  test		    - Run unit tests"
	@echo "  run            - Execute main.py"
	@echo "  docker-build   - Build Docker image (future enhancement)"

SRC := main.py
TEMP_DIR := src/temp
VIRTUAL_ENV := .venv

run: install
	uv run main.py

clean:
	rm -rf $(TEMP_DIR)/*

test: install
	uv run pytest --maxfail=5 --disable-warnings -q

# Future enhancements
# docker-build:
#	docker build -t ibmdataengineering .