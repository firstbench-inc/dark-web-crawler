import bs4
from urllib.parse import urlparse
import re
import asyncio
import time
from aiohttp import ClientSession, ClientResponseError
import ssl
import certifi
import aiohttp
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector
from seed_list import SEEDLIST, VISITED
from filter_html import good_filter


def is_valid_url(url):
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return ".onion" in url
    except Exception as e:
        return False


def fetch_links(resp):
    soup = bs4.BeautifulSoup(resp, "lxml")
    links = soup.find_all("a")
    for link in links:
        url = link.get("href")
        if is_valid_url(url):
            yield url


async def filter_resp(resp, url):
    if resp is None:
        return None
    good_filter(resp, url)


async def fetch_url_data(session, url):
    print(url)
    try:
        async with session.get(url, timeout=60) as response:
            resp = await response.text()
    except Exception as e:
        print(e)
        return None
    return resp


async def fetch(url):
    nvisited = 0
    url_queue = []
    prev_resp = None
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = ProxyConnector.from_url(
        "socks5://127.0.0.1:9050", rdns=True, ssl=ssl_context
    )

    async with aiohttp.ClientSession(connector=connector) as session:
        while True:
            resp_task = asyncio.ensure_future(fetch_url_data(session, url))
            filter_task = asyncio.ensure_future(filter_resp(prev_resp, url))
            await asyncio.gather(resp_task, filter_task)
            resp = resp_task.result()
            # print(resp)
            VISITED.append(url)
            nvisited += 1

            if resp is not None:
                for link in fetch_links(resp):
                    url_queue.append(link)
                prev_resp = resp

            while url_queue != []:
                url = url_queue.pop(0)
                if url not in VISITED:
                    break
            else:
                if SEEDLIST == []:
                    break
                url = SEEDLIST.pop()
            continue

        return resp


# asyncio.run(fetch("https://youtube.com"))
