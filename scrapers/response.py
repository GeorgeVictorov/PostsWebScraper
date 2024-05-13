import logging
from functools import lru_cache

import requests


@lru_cache(maxsize=100)
def get_response_html(url: str, params: dict = None) -> str | None:
    """
    Fetch HTML content from the given URL using GET request.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36'
        }

        if params is None:
            params = {}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        logging.info(response.url)
        html = response.text
        logging.info('Successfully fetched HTML')
        return html
    except requests.exceptions.RequestException as e:
        logging.error(f'An error occurred while fetching HTML from {url}: {e}')
        return None


def clear_cached_data():
    """
    Clear cached data.
    """
    get_response_html.clear_cache()
    logging.info('Cached users config cleared.')
