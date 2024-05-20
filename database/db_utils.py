import logging
from contextlib import closing

from database.db import Database


def get_database_connection():
    """
    Establishes a connection to the database.
    """
    database = Database()
    return database.get_connection()


def execute_select_query(func_name: str, query: str, params: tuple = None, fetchall: bool = False):
    """
    Executes a SELECT query on the database.
    Args:
        func_name (str): The name of the function calling this query.
        query (str): The SELECT query to be executed.
        params (tuple, optional): Parameters to be passed to the query. Defaults to None.
        fetchall (bool): Whether to fetch all results or just one. Defaults to False.
    """
    con = get_database_connection()
    if params is None:
        params = ()
    try:
        with closing(con.cursor()) as cur:
            cur.execute(query, params)
            if fetchall:
                res = cur.fetchall()
                logging.info(f'Successfully executed {func_name}.')
                return res
            else:
                res = cur.fetchone()
                logging.info(f'Successfully executed {func_name}.')
                return res
    except Exception as e:
        logging.error(f'An error occurred while executing {func_name}: {e}')


def execute_dml_query(func_name: str, query: str, params: tuple = None):
    """
    Executes a Data Manipulation Language (DML) query on the database.

    Args:
        func_name (str): The name of the function calling this query.
        query (str): The DML query to be executed.
        params (tuple, optional): Parameters to be passed to the query. Defaults to None.
    """
    con = get_database_connection()
    if params is None:
        params = ()
    try:
        with closing(con.cursor()) as cur:
            cur.execute(query, params)
            con.commit()
            logging.info(f'Successfully executed {func_name}.')
    except Exception as e:
        con.rollback()
        logging.error(f'An error occurred while executing {func_name}: {e}')
