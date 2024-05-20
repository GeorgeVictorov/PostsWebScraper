import itertools

from configurations.tables_names import POSTS
from database.db_utils import execute_select_query, execute_dml_query


def get_post() -> tuple[int, str, str, str, str] | None:
    """
    Get new post.
    """
    query = f'''
    select id, title,  snippet, post_url, image_url 
    from {POSTS} 
    where is_delivered != 1 order by id'''

    return execute_select_query('get_post', query, fetchall=True)


def select_titles() -> tuple:
    """
    Get all posts titles.
    """
    query = f'select title from {POSTS}'
    res = execute_select_query('select_titles', query, fetchall=True)
    data = tuple(itertools.chain.from_iterable(res))

    return data


def save_post_to_db(*args):
    """
    Insert scraped data to db.
    """
    query = f'''insert into {POSTS} (title, snippet, post_url, image_url)
                values (?, ?, ?, ?) '''
    execute_dml_query('save_post_to_db', query, args)


def change_post_status(post_id):
    """
    Change post status to 'delivered'.
    """
    query = f'''update {POSTS}
                set is_delivered = 1
                where id = ?'''
    execute_dml_query('change_post_status', query, (post_id,))
