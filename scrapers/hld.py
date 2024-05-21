import json
import logging
import random

from bs4 import BeautifulSoup
from database.dml import save_post_to_db, select_titles
from scrapers.response import HTMLFetcher


def load_more_data(html):
    """"
    Extract the parameters needed to load more posts from the given HTML content.
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        load_more_container = soup.find('div', class_='js-loadmore-data')
        if load_more_container:
            data_query_args = load_more_container.get('data-query-args')
            data_query_args = json.loads(data_query_args.replace('&quot;', '"'))
            current_page = int(load_more_container.get('data-current-page'))
            max_num_pages = data_query_args.get('max_num_pages', 1)
            next_page = current_page + 1 if current_page < max_num_pages else None
            if next_page:
                data_query_args['paged'] = next_page
            logging.info(f"Loading more data. Current page: {current_page}, Next page: {next_page}")
            return data_query_args, next_page
        logging.info("No load more container found.")
    except Exception as e:
        logging.error(f"An error occurred while extracting load more data: {e}")
        return None, None


def get_hld_post(url: str, max_retries: int = 3, total_retries: int = 0, params: dict | None = None):
    """
    Get a random post from the page.
    """
    html_fetcher = HTMLFetcher()

    if total_retries >= 3:
        logging.info('Total retries limit reached. Stopping attempts.')
        return None, None, None, None

    if max_retries == 0:
        logging.info('Max retries reached. Resetting and trying again.')
        html = html_fetcher.get_response(url).text
        params_dict, next_page = load_more_data(html)
        if next_page:
            params = params_dict
        html_fetcher.clear_cached_data()
        return get_hld_post(url, 3, total_retries + 1, params)

    try:
        html = html_fetcher.get_response(url).text
        soup = BeautifulSoup(html, 'html.parser')
        posts = soup.find_all('article')

        post = random.choice(posts)

        try:
            title = post.find('div', class_='post-archive__title').text.strip()
        except AttributeError:
            title = 'Title Not Found'

        if title not in select_titles() and title != 'Title Not Found':
            try:
                snippet = post.find('div', class_='post-archive__desc').text.strip()
            except AttributeError:
                snippet = 'Snippet Not Found'

            try:
                post_url = post.find('div', class_='post-archive__desc').a.get('href')
            except (AttributeError, KeyError):
                post_url = 'URL Not Found'

            try:
                image_url = post.find('img').get('src')
            except (AttributeError, KeyError):
                image_url = 'Image Not Found'

            logging.info('Post from HLD fetched successfully!\n')
            html_fetcher.clear_cached_data()
            return save_post_to_db(title, snippet, post_url, image_url)

        elif max_retries > 0:
            logging.info('Starting a new retry.\n')
            return get_hld_post(url, max_retries - 1, total_retries)

    except Exception as e:
        logging.error(f'An error occurred: {e}')
        return None, None, None, None
