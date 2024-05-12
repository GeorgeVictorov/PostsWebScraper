import logging

from config_data.config import load_config
from logger.logger import setup_logger
from database.db import Database
from scrapers.trv import get_edu_trv_post, trv_url


def init_db():
    try:
        db_manager = Database()
        db_manager.create_table()
        logging.info(f'Database initialized successfully.')
    except Exception as e:
        logging.error(f'Error initializing database: {e}')


if __name__ == '__main__':
    setup_logger()
    init_db()

    config = load_config()
    print(config.db.database)
    print(get_edu_trv_post(trv_url))
