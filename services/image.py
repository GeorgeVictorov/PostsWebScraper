import re
import base64
import logging

import requests


def extract_image_url(image_url: str) -> str | None:
    """
    Extracts the URL from the background-image CSS style attribute.
    """
    url_match = re.search(r"url\('([^']+)'\)", image_url)
    if url_match:
        return url_match.group(1)
    return None


def image_url_to_base64(image_url: str) -> str | None:
    """
    Converts an image from a URL to Base64.
    """
    try:
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        image_base64 = base64.b64encode(image_response.content).decode('utf-8')
        logging.info('Image fetched and converted to Base64 successfully.')
        return image_base64
    except requests.exceptions.RequestException as e:
        logging.error('Error fetching image:', e)
        return None
