import json
import requests


def json_get(url, params):
    return json.loads(requests.get(url, params=params).text)


# TODO: jlevine - Add logging
def get_all_pages_for(url, params, picker):
    items = json_get(url, params)
    if 'next' not in items:
        return [picker(items) for items in items['data']]
    else:
        return [picker(items) for items in items['data']] + get_all_pages_for(items['next'], params, picker)
