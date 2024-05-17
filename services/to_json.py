from services.image import image_url_to_base64


def sql_to_json(select_result):
    """
    Convert SQL select result to JSON string.
    """
    post_ids = []
    json_data = []

    for row in select_result:
        post_id, title, snippet, post_url, image_url = row
        image_url = image_url_to_base64(image_url)
        post_data = {
            'Title': title,
            'Text': snippet,
            'Source': post_url,
            'Picture': '' if image_url == 'Image Not Found' else image_url
        }
        post_ids.append(post_id)
        json_data.append(post_data)

    return post_ids, json_data
