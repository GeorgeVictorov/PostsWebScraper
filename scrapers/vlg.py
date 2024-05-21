import logging
import random

from bs4 import BeautifulSoup
from database.dml import save_post_to_db, select_titles
from scrapers.response import HTMLFetcher


def get_vlg_post(url: str, max_retries: int = 3, total_retries: int = 0):
    """
    Get a random post from the page.
    """
    html_fetcher = HTMLFetcher()

    if total_retries >= 3:
        logging.info('Total retries limit reached. Stopping attempts.')
        return None, None, None, None

    if max_retries == 0:
        logging.info('Max retries reached. Resetting and trying again.')
        html_fetcher.clear_cached_data()
        return get_vlg_post(url, 3, total_retries + 1)

    try:
        html = html_fetcher.get_response(url).text
        soup = BeautifulSoup(html, 'html.parser')
        posts = soup.find_all('div', class_='base-PostCard--PostCard__container')

        post = random.choice(posts)

        try:
            title = post.find('span', class_='base-PostCard-_-FeatureCard--FeatureCard__title').text.replace('\xa0',
                                                                                                             ' ')
        except AttributeError:
            title = 'Title Not Found'

        if title not in select_titles() and title != 'Title Not Found':
            try:
                snippet = post.find('span',
                                    class_='base-PostCard-_-FeatureCard--FeatureCard__bodyPreamble').text.replace(
                    '\xa0', ' ')
            except AttributeError:
                snippet = 'Snippet Not Found'

            try:
                post_url = 'https://www.the-village.ru' + post.a.get('href')
            except (AttributeError, KeyError):
                post_url = 'URL Not Found'

            try:
                image_url = post.find('img').get('src')
            except (AttributeError, KeyError):
                image_url = 'Image Not Found'

            logging.info('Post from VLG fetched successfully!\n')
            html_fetcher.clear_cached_data()
            return save_post_to_db(title, snippet, post_url, image_url)

        elif max_retries > 0:
            logging.info('Starting a new retry.\n')
            return get_vlg_post(url, max_retries - 1, total_retries)

    except Exception as e:
        logging.error(f'An error occurred: {e}')
        return None, None, None, None
