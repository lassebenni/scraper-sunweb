from time import sleep
from typing import Dict, List
import requests
import json
import math
import collections

def flatten(dictionary, parent_key=False, separator='.'):
    """
    Turn a nested dictionary into a flattened dictionary
    :param dictionary: The dictionary to flatten
    :param parent_key: The string to prepend to dictionary's keys
    :param separator: The string used to separate flattened keys
    :return: A flattened dictionary
    """

    items = []
    for key, value in dictionary.items():
        new_key = str(parent_key) + separator + key if parent_key else key
        if isinstance(value, collections.MutableMapping):
            items.extend(flatten(value, new_key, separator).items())
        elif isinstance(value, list):
            for k, v in enumerate(value):
                items.extend(flatten({str(k): v}, new_key).items())
        else:
            items.append((new_key, value))
    return dict(items)


def scrape_sunweb():
    res = []

    offset = 0
    limit = 50

    url = f"https://www.sunweb.nl/api/sitecore/SearchApi/GetSearchResponse?Duration%5B0%5D=8-10&sort=Price&contextitemid=38b1ea16-284c-40c9-af10-61c5bb8ce520&isFirstUserRequest=True&Allocation=20&isFirstLoad=true&offset={offset}&limit={limit}"

    payload={}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    first: List[Dict] = response.json()
    listings = [flatten(x) for x in first['results']]
    res.append(listings)

    total_results = first['pagination']['totalResults']
    total_trips = math.ceil(total_results / limit)
    current_trip = 1

    while current_trip < total_trips:
        sleep(1)
        current_trip += 1
        offset += limit
        url = f"https://www.sunweb.nl/api/sitecore/SearchApi/GetSearchResponse?Duration%5B0%5D=8-10&sort=Price&contextitemid=38b1ea16-284c-40c9-af10-61c5bb8ce520&isFirstUserRequest=True&Allocation=20&isFirstLoad=true&offset={offset}&limit={limit}"
        response = requests.request("GET", url, headers=headers, data=payload)
        listings: List[Dict] = [flatten(x) for x in first['results']]
        res.append(listings)

    return [item for sublist in res for item in sublist] # flatten nested list


def store(res: List[Dict]):
    with open('results.json', 'w') as f:
        json.dump(res, f)


if __name__ == '__main__':
    res = scrape_sunweb()
    store(res)