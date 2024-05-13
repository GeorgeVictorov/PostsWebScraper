import logging
import sqlite3
from contextlib import closing

from database.db import Database

POSTS = 'posts_data'


def save_post_to_db(*args):
    """
    Insert scraped data to db.
    """
    database = Database()
    con = database.get_connection()
    try:
        with closing(con.cursor()) as cur:
            cur.execute(
                f'''insert into {POSTS} (title, snippet, post_url, image_url)
                    values (?, ?, ?, ?) ''',
                args
            )
            con.commit()
        logging.info('Post successfully saved to db.')
    except sqlite3.Error as e:
        con.rollback()
        logging.error(f'Error saving post: {e}')
