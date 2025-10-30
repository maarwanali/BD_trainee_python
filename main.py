from cli_manager import CLIManager
import logging.config
from config.logging_config import LOGGING_CONFIG
from dotenv import load_dotenv
import os

# python main.py --students ./data/students.json --rooms ./data/rooms.json --format json

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

if __name__ == '__main__' :

    DB_CONFIG ={
    "dbname":os.environ.get("DB_NAME","database"),
    "user":os.environ.get("DB_USER","root"),
    "password":os.environ.get("DB_PASSWORD","password"),
    "host": os.environ.get("DB_HOST","localhost"),
    "port":os.environ.get("DB_PORT","5432")
    }      
    logging.info('Starting pipeline')
    manager = CLIManager(DB_CONFIG)
    manager.run()