import logging
import sqlite3
from contextlib import closing

from configurations.config import load_config

POSTS = 'posts_data'


class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.config = load_config()
            self.db_connection = None
            self._initialize_connection()
            self._initialized = True

    def _initialize_connection(self):
        if self.db_connection is None:
            try:
                logging.info('Creating a new database connection...')
                self.db_connection = sqlite3.connect(self.config.db.database)
                logging.info('Database connection created successfully.')
            except sqlite3.Error as e:
                logging.error(f'Error creating database connection: {e}.')

    def get_connection(self):
        if self.db_connection is not None:
            logging.info('Reusing existing database connection...')
            return self.db_connection
        else:
            self._initialize_connection()
            return self.db_connection

    def create_table(self):
        try:
            with self.db_connection as con:
                with closing(con.cursor()) as cur:
                    cur.execute(
                        f'''create table if not exists {POSTS} (
                            id integer primary key,
                            title text,
                            snippet text,
                            post_url text,
                            image_url text,
                            is_delivered integer default 0)'''
                    )
                    self.db_connection.commit()
            logging.info(f'Table {POSTS} created or verified')
        except Exception as e:
            logging.error(f'Error creating table {POSTS}: {e}')

    def close_database(self):
        if self.db_connection:
            try:
                self.db_connection.close()
                logging.info('Database connection closed.')
            except Exception as e:
                logging.error(f'Error closing database connection: {e}.')
        else:
            logging.warning('No open database connection to close or connection is already closed.')
