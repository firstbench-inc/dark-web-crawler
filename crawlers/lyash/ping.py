import requests
import bs4
from urllib.parse import urlparse
import re
import filter
from seed_list import SEEDS

LIMIT = 100

# SEEDLIST = [
#     "http://torlinkv7cft5zhegrokjrxj2st4hcimgidaxdmcmdpcrnwfxrr2zxqd.onion/",
#     "http://fvrifdnu75abxcoegldwea6ke7tnb3fxwupedavf5m3yg3y2xqyvi5qd.onion/",
#     "http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/wiki/index.php/Main_Page",
#     "http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion/discover",
#     "http://tt3j2x4k5ycaa5zt.onion/",
#     "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/address/",
#     "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/add/onionsadded/",
#     "http://donionsixbjtiohce24abfgsffo2l4tk26qx464zylumgejukfq2vead.onion/?cat=19&pg=1",
#     "http://donionsixbjtiohce24abfgsffo2l4tk26qx464zylumgejukfq2vead.onion/?cat=20&pg=1&lang=en",
#     "http://donionsixbjtiohce24abfgsffo2l4tk26qx464zylumgejukfq2vead.onion/?cat=7&pg=1&lang=en",
#     "https://github.com/alecmuffett/real-world-onion-sites",
# ]


def is_valid_url(url):
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return bool(re.search(r"\.onion/$", url))
    except Exception as e:
        return False


class TorReq:
    def __init__(self, seeds):
        self.session = requests.session()
        self.session.proxies = {
            "http": "socks5h://127.0.0.1:9050",
            "https": "socks5h://127.0.0.1:9050",
        }
        self.nvisited = 0
        self.visited = []
        self.response = ""
        self.url_stack = seeds

    def get(self, url):
        # for seed in SEEDLIST:
        #     response = requests.get(seed)
        #     print(response.status_code)
        if self.nvisited >= LIMIT:
            return
        if url in self.visited:
            return

        try:
            print(url)
            response = self.session.get(url).content
        except:
            print("meow")
            self.chain()
            return
            pass
        try:
            self.response = response
            self.nvisited += 1
            self.visited.append(url)
            self.fetch_links()
        except:
            pass

    def fetch_links(self):
        soup = bs4.BeautifulSoup(self.response, "lxml")
        links = soup.find_all("a")
        for link in links:
            url = link.get("href")
            if is_valid_url(url):
                self.url_stack.append(url)
                # filter.simple_filter(url)
                print('1234567890\n\n')
                self.chain()

    def chain(self):
        url = self.url_stack.pop(0)
        self.get(url)


x = TorReq(SEEDS)
x.get('https://lxwu7pwyszfevhglxfgaukjqjdk2belosfvsl2ekzx3vrboacvewc7qd.onion/')
# print(is_valid_url("http://google.com"))
# print(is_valid_url("http://google.onion"))
# print(is_valid_url("http://glskjdflksjdflskdjflsdkfj"))
# print(is_valid_url("google.onion"))
# print(is_valid_url("google.asldkfjldskfj"))

