from typing import Dict, List
import requests
import json



def scrape_sunweb():
    res = []

    offset = 0
    

    url = f"https://www.sunweb.nl/api/sitecore/SearchApi/GetSearchResponse?Duration%5B0%5D=8-10&sort=Price&contextitemid=38b1ea16-284c-40c9-af10-61c5bb8ce520&isFirstUserRequest=True&Allocation=20&isFirstLoad=true&offset=0&limit=50"

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
        # 'Cookie': 'participants={"rooms":[["1989-11-07","1989-11-07"]],"allocation":20}; search-sel={"selectedFilters":[{"filterType":2,"values":["8-10"]}]}; sunwebnl#lang=nl-NL'
    }

    
    response = requests.request("GET", url, headers=headers, data=payload)
    r = json.loads(response.text)



def store(res: List[Dict]):
    with open('results.json', 'w') as f:
        json.dump(res, f)

if __name__ == '__main__':
    scrape_sunweb()
    store()