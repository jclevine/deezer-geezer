import json
import requests
from itertools import chain


def json_get(url, params):
    return json.loads(requests.get(url, params=params).text)


def json_post(url, **kwargs):
    return json.loads(requests.post(url, **kwargs).text)


# TODO: jlevine - Add logging
def get_all_pages_for(url, params, picker):
    items = json_get(url, params)
    if 'next' not in items:
        return [picker(items) for items in items['data']]
    else:
        return list(chain(
            [picker(items) for items in items['data']],
            get_all_pages_for(items['next'], params, picker))
        )
