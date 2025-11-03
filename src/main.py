from cli_manager import CLIManager
import logging.config
from config.logging_config import LOGGING_CONFIG
from dotenv import load_dotenv
import os

# python main.py --students ./data/students.json --rooms ./data/rooms.json --format json

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

if __name__ == '__main__' :
    load_dotenv()

    DB_CONFIG ={
    "dbname":os.getenv("DB_NAME"),
    "user":os.getenv("DB_USER"),
    "password":os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port":os.getenv("DB_PORT")
    }   

    logger.info('Starting pipeline')
    manager = CLIManager(DB_CONFIG)
    manager.run()