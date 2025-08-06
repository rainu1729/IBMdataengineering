import os
from dotenv import load_dotenv
import ast

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

GDP_DATA_URL = os.getenv('GDP_DATA_URL')
GDP_DATA_DB = os.getenv('GDP_DATA_DB')
GDP_DATA_TABLE = os.getenv('GDP_DATA_TABLE')
GDP_DATA_SCHEMA = ast.literal_eval(os.getenv('GDP_DATA_SCHEMA'))
GDP_DATA_OUTPUT = os.getenv('GDP_DATA_OUTPUT')