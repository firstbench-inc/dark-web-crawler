import requests
import bs4
from urllib.parse import urlparse
import re

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
            pattern = r"^http:\/\/[a-z2-7]{16}\.onion\/?$"
            return bool(re.match(pattern, url))
    except ValueError:
        return False


class TorReq:
    def __init__(self):
        self.session = requests.session()
        self.session.proxies = {
            "http": "socks5h://127.0.0.1:9050",
            "https": "socks5h://127.0.0.1:9050",
        }
        self.nvisited = 0
        self.visited = []
        self.response = ""
        self.url_stack = []

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
        except Exception as e:
            print(e)
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
                self.chain()

    def chain(self):
        url = self.url_stack.pop(0)
        self.get(url)


x = TorReq()
seed_list = ['http://qigcb4g4xxbh5h06.onion ', 'http://qjxejztupq4x7re.onion', 'http://a2rfh7u5ryldaocg.onion', 'http://qhvqofwtqx7ddpzy.onion', 'http://tl7n3gkpjnyvl7c2.onion', 'http://vijs2fmpd72nbqok.onion', 'http://xlv5dckljs4vhmhm.onion', 'http://cmgvqnxjoiqthvrc.onion', 'http://у7pm60f53hzeb7u2.onion', 'http://fosyxyjdgzbeacry.onion', 'http://2xcd24wfjiqwzwnr.onion', 'http://e4nybovdbcwaqlyt.onion', 'http://ihdhoeoovbtgutfm.onion', 'http://oscbw3h7wrfxqi4m.onion', 'http://vyrxto4jsgoxvilf.onion', 'http://uqxc5rgqum7ihsey.onion', 'http://uted272mruszpl4z.onion', 'http://kkvj4mhsttfcrksj.onion', 'http://jute7c4nqhc3czjanxoynuaeqjdiw2rdenjec5fzajgdtymrkf5xiyid.onion', 'http://Ifhu7crxlscozvquvj5zyaepnzowqghijugih2phq34gbqwg25kutqad.onion', 'http://lgvlgiguxjaiknspz3ddgtd57ckapz6m6qh5cnzei6q230goex3zp7id.onion', 'http://qn2jfaleeshn7jmxstfjszbotwp6nlusnpqfjqsdglc73r2leqsthhad.onion', 'http://rhbyafmqy2pwrokhzmpdyemvohib34g4qdbjilvnihy3fawbjs7bbbid.onion', 'http://rjann5eombayqugdlf4clvddvhw5545lrllng6lpf6cf2msibd6datqd.onion', 'http://yxrfбuf2mvuazmt4.onion', 'http://763k6h7u3kx5m27mkoraoqt64ftglix5tphgugyxzghfczzkgl74hyd.onion', 'http://bf3xcbgqlpkv2zkxkhwygmjnflmi4xweb7qefa3chmnnuffzufg6nvad.onion', 'http://gvefwipd7xtjv54xgj5itvub6ys6kbv7uqw5sb25nhshtfvfxmduo7id.onion ', 'http://jjb24xrxdlmezul7zg3fcsqpwxcsy3qhc2ufvsl6qccndasmda4vahqd.onion ', 'http://ocpb44b4vs6ed24dnlkrxu6ixc6qapebacsqst55cn4d6ndnnxq6wsqd.onion ', 'http://ptoccrf6l4atxf4n.onion', 'http://ptpd5veqnscjdexvrydq20бpoqln2wose7v4d6n45zioj3z7qxkuypad.onion', 'http://u7y7hnemlzjimmdk.onion', 'http://umd2fe56bmjmasuk.onion', 'http://wbpcdrudlxgbvrrlhjxo2vlsrqltj54tpcbptfb52nk2voroepeaefad.onion ', 'http://7jcj4uy4tzegxqoiott4y3i3t3y42ukw2kc64c4misayxaxp3yrvljqd.onion ', 'http://7jcj4uy4tzegxqoiott4y3i313y42ukw2kc64c4misayxaxp3yrvljqd.onion', 'http://xke7mh3qjekqccqq.onion']
for i in seed_list:
    x.get(i)
