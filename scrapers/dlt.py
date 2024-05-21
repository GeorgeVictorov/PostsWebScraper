import logging
import random

from bs4 import BeautifulSoup
from database.dml import save_post_to_db, select_titles
from scrapers.response import HTMLFetcher


def get_dlt_rss_post(url: str, max_retries: int = 3, total_retries: int = 0):
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
        return get_dlt_rss_post(url, 3, total_retries + 1)

    try:
        xml_data = html_fetcher.get_response(url).text
        soup = BeautifulSoup(xml_data, 'xml')
        posts = soup.find_all('item')

        post = random.choice(posts)

        try:
            title = post.find('title').text
        except AttributeError:
            title = 'Title Not Found'

        if title not in select_titles() and title != 'Title Not Found':
            desc_soup = BeautifulSoup(post.find('description').text, 'html.parser')

            try:
                snippet = desc_soup.p.text.replace('\n', '').replace('\xa0', ' ').strip()
                if snippet == '':
                    for elem in desc_soup.find_all('p'):
                        if elem != '\n' and elem != '':
                            snippet = elem.text.replace('\n', '').replace('\xa0', ' ').strip()
            except AttributeError:
                snippet = 'Snippet Not Found'

            try:
                post_url = post.find('link').text
            except (AttributeError, KeyError):
                post_url = 'URL Not Found'

            try:
                image_url = 'https://diletant.media' + desc_soup.find('img').get('src')
            except (AttributeError, KeyError):
                image_url = 'Image Not Found'

            logging.info('Post from DLT fetched successfully!\n')
            html_fetcher.clear_cached_data()
            return save_post_to_db(title, snippet, post_url, image_url)

        elif max_retries > 0:
            logging.info('Starting a new retry.\n')
            return get_dlt_rss_post(url, max_retries - 1, total_retries)

    except Exception as e:
        logging.error(f'An error occurred: {e}')
        return None, None, None, None
