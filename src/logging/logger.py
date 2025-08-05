from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, format="<green>{time}</green> <level>{message}</level>", level="INFO")
