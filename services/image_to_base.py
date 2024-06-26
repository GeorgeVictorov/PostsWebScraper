import base64
import io
import logging

import requests
from PIL import Image
from scrapers.response import HTMLFetcher

NGINX_MAX_UPLOAD_SIZE = 1_000_000


def compress_image(image, max_size=NGINX_MAX_UPLOAD_SIZE):
    """
    Compresses the given image to fit within the specified maximum size.
    """
    img = Image.open(image)
    img = img.convert("RGB")

    scale = 1
    if max_size:
        orig_size = img.size[0] * img.size[1] * 3
        scale = min(1.0, (max_size / orig_size) ** 0.5)

    new_width = int(img.size[0] * scale)
    new_height = int(img.size[1] * scale)
    img.thumbnail((new_width, new_height))

    img_buffer = io.BytesIO()
    img.save(img_buffer, format="JPEG", quality=85)
    img_buffer.seek(0)
    return img_buffer


def image_url_to_base64(image_url: str) -> str | None:
    """
    Converts an image from a URL to Base64 after compressing it.
    """
    if image_url == 'Image Not Found':
        return 'Image Not Found'
    try:
        html_fetcher = HTMLFetcher()
        image_response = html_fetcher.get_response(image_url)
        image_response.raise_for_status()

        # Compress the image
        compressed_image = compress_image(io.BytesIO(image_response.content))

        # Convert to Base64
        image_base64 = base64.b64encode(compressed_image.read()).decode('utf-8')
        logging.info('Image fetched, compressed, and converted to Base64 successfully.')
        return image_base64
    except requests.exceptions.RequestException as e:
        logging.error('Error fetching image:', e)
        return None
