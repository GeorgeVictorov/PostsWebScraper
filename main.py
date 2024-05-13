import logging
import json

from api.post import send_data_to_api
from configurations.config import load_config
from configurations.urls import TRV_URL
from logger.logger import setup_logger
from database.db import Database

from database.dml import get_post
from services.to_json import sql_to_json

from scrapers.trv import get_edu_trv_post


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

    data = get_post()
    post_ids, json_data = sql_to_json(data)

    print(json_data)

    # send_data_to_api()

    db_instance = Database()
    db_instance.close_database()

