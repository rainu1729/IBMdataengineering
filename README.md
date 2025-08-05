# IBM Data Engineering Web Scraping Project

This project is a modular Python application for web scraping, designed for extensibility and best practices in logging, configuration, and environment management.

## Features
- Web scraping framework (extensible)
- Logging via [loguru](https://github.com/Delgan/loguru)
- Configuration and secrets managed via `.env` and `python-dotenv`
- Modular code structure for easy feature addition
- Makefile for setup, running, and cleaning
- Ready for future enhancements (Docker, database integration, etc.)

## Project Structure
```
IBMdataengineering/
├── Makefile
├── requirements.txt
├── README.md
├── .gitignore
├── .env
├── src/
│   ├── main.py
│   ├── config/
│   │   └── config.py
│   ├── logging/
│   │   └── logger.py
│   ├── scraping/
│   │   └── sample_scraper.py
│   └── temp/
```

## Setup & Usage
1. **Create virtual environment:**
   ```bash
   make venv
   ```
2. **Install dependencies:**
   ```bash
   make install
   ```
3. **Run the project:**
   ```bash
   make run
   ```
4. **Clean temp files:**
   ```bash
   make clean
   ```

## Configuration
- Store database credentials and secrets in `.env` (excluded from git).
- Adjust logging and scraping logic in respective modules under `src/`.

## Future Enhancements
- Docker support (`make docker-build`)
- Advanced scraping features
- Database integration
- Automated tests

## License
MIT
