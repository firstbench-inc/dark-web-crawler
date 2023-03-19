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
    title = soup.find("title")
    for link in links:
        url = link.get("href")
        if is_valid_url(url):
            yield (url, title.string)


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
        print("fetch url", e)
        return None
    return resp


async def post_url_data(session, data):
    if data["content"] is None:
        return
    print(data["link"])

    # data = data.__str__()
    try:
        async with session.post(
            "http://127.0.0.1:9200/logs/my_app",
            headers={"Content-Type": "application/json"},
            # data=bytes(data, "utf-8"),
            json=data,
        ) as resp:
            print(resp.status)
    except Exception as e:
        print("post url", e)

    pass


async def fetch(url):
    nvisited = 0
    url_queue = []
    prev_resp = None
    prev_title = None
    prev_url = url
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = ProxyConnector.from_url(
        "socks5://127.0.0.1:9050", rdns=True, ssl=ssl_context
    )

    es_session = aiohttp.ClientSession()

    async with aiohttp.ClientSession(connector=connector) as session:
        while True:
            data = {"link": prev_url, "content": prev_resp, "title": prev_title}

            resp_task = asyncio.ensure_future(fetch_url_data(session, url))
            # filter_task = asyncio.ensure_future(filter_resp(prev_resp, url))
            filter_task = asyncio.ensure_future(post_url_data(es_session, data))
            await asyncio.gather(resp_task, filter_task)
            resp = resp_task.result()
            # print(resp)

            if resp is not None:
                VISITED.append(url)
                nvisited += 1
                prev_url = url
                for (link, title) in fetch_links(resp):
                    if link not in VISITED:
                        url_queue.append(link)
                    prev_title = title
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


async def fetch_single(url):
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
            continue

        return resp


if __name__ == "__main__":
    asyncio.run(
        fetch("http://torlinkv7cft5zhegrokjrxj2st4hcimgidaxdmcmdpcrnwfxrr2zxqd.onion/")
    )
