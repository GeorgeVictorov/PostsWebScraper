import json


def sql_to_json(data: tuple) -> str:
    """
    Convert SQL select result to JSON string.
    """
    post_data = {
        'Source': data[2],
        'Title': data[0],
        'Text': data[1]
    }

    json_string = json.dumps(post_data, ensure_ascii=False)

    return json_string
