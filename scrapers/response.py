import logging
from functools import lru_cache

import requests


class HTMLFetcher:
    def __init__(self, max_cache_size=100):
        self.get_response = lru_cache(maxsize=max_cache_size)(self._get_response)

    @staticmethod
    def _get_response(url: str, params: dict = None) -> requests.Response | None:
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
            logging.info('Successfully fetched HTML')
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f'An error occurred while fetching HTML from {url}: {e}')
            return None

    def clear_cached_data(self):
        """
        Clear cached data.
        """
        self.get_response.cache_clear()
        logging.info('Cached data cleared.')
