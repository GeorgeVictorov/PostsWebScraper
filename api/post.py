import logging
import requests

from configurations.config import load_config
from configurations.urls import API_URL
from database.dml import get_post, change_post_status
from services.to_json import sql_to_json


def send_data_to_api():
    """
    Send data to the API endpoint.
    """
    url = API_URL
    config = load_config()

    data = get_post()
    post_ids, json_data = sql_to_json(data)

    headers = {
        'Authorization': str(config.api.token),
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=json_data, headers=headers)
        if response.status_code == 201:
            for post_id in post_ids:
                change_post_status(post_id)
            logging.info('Data added successfully')
        else:
            logging.error(f'Error: {response.status_code}, {response.content}')
    except Exception as e:
        logging.error(f'Error: {e}')
