from loguru import logger
import sys

logger.remove()
logger.add("src/datafiles/logs/code_log.log", rotation="1 MB", level="DEBUG", format="<green>{time}</green> <level>{message}</level>")
logger.add(sys.stdout, format="<green>{time}</green> <level>{message}</level>", level="INFO")
