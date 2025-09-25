from src.scraping.scraper import scrape
from src.logging.logger import logger
from src.scraping.gdpdata import run as run_gdp_data
from src.scraping.bank_project import run as run_bank_data


def main():
    logger.info("Main function started.")
    # scrape()
    # run_gdp_data()
    run_bank_data()
    logger.info("Main function finished.")


if __name__ == "__main__":
    main()
