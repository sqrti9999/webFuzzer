import requests
import json
from bs4 import BeautifulSoup as Soup
# FIXME catch requests.exceptions.ProxyError when api key is wrong


def start_crawl(url, api_key):
    # TODO AJAXspider
    r = requests.get(url="http://zap/JSON/spider/action/scan",
                     headers={"X-ZAP-API-Key": api_key},
                     params={"url": url},
                     proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})

    if r.status_code == 200:
        return True, json.loads(r.text)["scan"]
    else:
        return False, json.loads(r.text)["message"]


def view_status(scan_id, api_key):
    r = requests.get(url="http://zap/JSON/spider/view/status",
                     headers={"X-ZAP-API-Key": api_key},
                     params={"scanId": scan_id},
                     proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})

    if r.status_code == 200:
        return True, json.loads(r.text)["status"]
    else:
        return False, json.loads(r.text)["message"]


def view_sitemap(scan_id, api_key):
    if not view_status(scan_id, api_key)[0] or view_status(scan_id, api_key)[1] != 100:
        return False, "Crawling is not finished"

    r = requests.get(url="http://zap/JSON/spider/view/addedNodes",
                     headers={"X-ZAP-API-Key": api_key},
                     params={"scanId": scan_id},
                     proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})

    # TODO Visualize sitemap from urls
    raise NotImplementedError


def view_scan_result(scan_id, api_key):
    if not view_status(scan_id, api_key)[0] or view_status(scan_id, api_key)[1] != '100':
        return False, "Crawling is not finished"

    r = requests.get(url="http://zap/JSON/spider/view/fullResults",
                     headers={"X-ZAP-API-Key": api_key},
                     params={"scanId": scan_id},
                     proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})

    if r.status_code == 200:
        return True, r.text
    else:
        return False, json.loads(r.text)["message"]


def find_vector_input(scan_id, api_key):
    spider_result = view_scan_result(scan_id, api_key)
    if not spider_result[0]:
        return False, "Error fetching results: (%s) on crawl.view_scan_result" % spider_result[1]

    # parse api response
    spider_result = json.loads(spider_result[1])['fullResults']
    for _ in spider_result[:]:
        try:
            spider_result.update(_)
        except AttributeError:
            spider_result = _

    # choose only valid responses... (status 2xx)
    valid_responses = [_['messageId'] for _ in spider_result['urlsInScope'] if _['statusCode'].startswith("2")]

    # and fetch those responses
    r = requests.get(url="http://zap/JSON/core/view/messagesById",
                     headers={"X-ZAP-API-Key": api_key},
                     params={"ids": ",".join(valid_responses)},     # FIXME might cause 414 uri too long
                     proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})
    if r.status_code != 200:
        return False, json.loads(r.text)["message"]

    vectors = []
    for _ in json.loads(r.text)['messagesById']:
        s = Soup(_["responseBody"], "html.parser")
        if len(s.select("input")) != 0:
            vectors.append({
                "id": _['id'],
                "url": _['requestHeader'].split(' ')[1],
                "vector": s.select("input")
            })
        del s
    return True, vectors


def find_vector_tracker(scan_id, api_key):
    # TODO Fuzz and find tracker
    return
