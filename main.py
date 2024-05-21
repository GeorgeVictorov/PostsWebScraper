import logging

from api.post import send_data_to_api
from configurations.config import load_config
from configurations.urls import TRV_URL, VLG_URL, DLT_URL, HLD_URL
from logger.logger import setup_logger
from database.db import Database
from scrapers import get_edu_trv_post, get_vlg_post, get_dlt_rss_post, get_hld_post

functions_and_urls = {
    get_edu_trv_post: TRV_URL,
    get_vlg_post: VLG_URL,
    get_dlt_rss_post: DLT_URL,
    get_hld_post: HLD_URL
}


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

    for func, url in functions_and_urls.items():
        func(url)

    send_data_to_api()

    db_instance = Database()
    db_instance.close_database()
