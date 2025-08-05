from src.scraping.sample_scraper import scrape
from src.logging.logger import logger


def main():
    logger.info("Main function started.")
    scrape()
    logger.info("Main function finished.")


if __name__ == "__main__":
    main()
