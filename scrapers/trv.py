import logging
import re
import random
from typing import Any

from bs4 import BeautifulSoup
from database.dml import save_post_to_db, select_titles
# from scrapers.response import get_response_html, clear_cached_data
from scrapers.response import HTMLFetcher


def extract_image_url(image_url: str) -> str | None:
    """
    Extracts the URL from the background-image CSS style attribute.
    """
    url_match = re.search(r"url\('([^']+)'\)", image_url)
    if url_match:
        return url_match.group(1)
    return None


def get_edu_trv_post(url: str, max_retries: int = 3) -> tuple[str | Any, str | Any, str | Any, str | None]:
    """
    Get a random post from the page.
    """
    html_fetcher = HTMLFetcher()

    if max_retries == 0:
        logging.info('Max retries reached. Resetting and trying again.')
        html_fetcher.clear_cached_data()
        return get_edu_trv_post(url, 3)

    try:
        html = html_fetcher.get_response(url).text
        soup = BeautifulSoup(html, 'html.parser')
        posts = soup.find_all('div', class_='col-sm-6 col-xxl-4 post-col')

        post = random.choice(posts)

        if post.find('div', class_='entry-meta').a.text not in ('Краудфандинг', 'Память'):

            try:
                title = post.find('h2').text
            except AttributeError:
                title = 'Title Not Found'

            if title not in select_titles() and title != 'Title Not Found':
                try:
                    snippet = post.find('div', class_='entry-content').p.text.replace('\xa0', ' ')
                except AttributeError:
                    snippet = 'Snippet Not Found'

                try:
                    post_url = post.find('h2').a['href']
                except (AttributeError, KeyError):
                    post_url = 'URL Not Found'

                try:
                    image_url = extract_image_url(
                        post.find('figure', class_='post-featured-image post-img-wrap').a['style'])
                except (AttributeError, KeyError):
                    image_url = 'Image Not Found'

                logging.info('Post from TRV fetched successfully!\n')
                html_fetcher.clear_cached_data()
                return save_post_to_db(title, snippet, post_url, image_url)

            elif max_retries > 0:
                logging.info('Post in DB, starting a new retry.\n')
                return get_edu_trv_post(url, max_retries - 1)

        elif max_retries > 0:
            logging.info('Starting a new retry.\n')
            return get_edu_trv_post(url, max_retries - 1)

    except Exception as e:
        logging.error(f'An error occurred: {e}')
        return None, None, None, None
