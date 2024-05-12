import logging
import random
from typing import Any

import requests
from bs4 import BeautifulSoup
from cachetools import cached, TTLCache
from services.image import extract_image_url

page = random.choice(range(1, 25))
trv_url: str = 'https://www.trv-science.ru/category/edu/page/{}'.format(page)
titles = ('Образование? Высшее?? Забудьте', 'IT для школьников',
          'Среднее или всё же медиана', 'Остановить утрату мозга', 'Гаусс негодует')

cache = TTLCache(maxsize=100, ttl=300)


def clear_cached_data():
    """
    Clear cached data from the cache.
    """
    cache.clear()
    print('Cached users config cleared.')


@cached(cache)
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


def get_edu_trv_post(url: str, max_retries: int = 3) -> tuple[str | Any, str | Any, str | Any, str | None]:
    """
    Get a random post from the page.
    """
    if max_retries == 0:
        logging.info('Max retries reached. Resetting and trying again.')
        clear_cached_data()
        return get_edu_trv_post(url, 3)

    try:
        # noinspection PyCallingNonCallable
        html = get_response_html(trv_url)
        soup = BeautifulSoup(html, 'html.parser')
        posts = soup.find_all('div', class_='col-sm-6 col-xxl-4 post-col')

        post = random.choice(posts)

        if post.find('div', class_='entry-meta').a.text not in ('Краудфандинг', 'Память'):

            title = post.find('h2').text if post.find('h2') else "Title Not Found"

            if title not in titles:
                snippet = post.find('div', class_='entry-content').p.text.replace('\xa0', ' ') if post.find('div',
                                                                                                            class_='entry-content') else "Snippet Not Found"
                post_url = post.find('h2').a['href'] if post.find('h2').a else "URL Not Found"
                image_url = extract_image_url(
                    post.find('figure', class_='post-featured-image post-img-wrap').a['style']) if post.find('figure',
                                                                                                             class_='post-featured-image post-img-wrap') else "Image Not Found"

                logging.info('Post fetched successfully!\n')
                return title, snippet, post_url, image_url

            elif max_retries > 0:
                logging.info('Starting a new retry (post in db).\n')
                return get_edu_trv_post(url, max_retries - 1)

        elif max_retries > 0:
            logging.info('Starting a new retry.\n')
            return get_edu_trv_post(url, max_retries - 1)

    except Exception as e:
        logging.error(f'An error occurred: {e}')
