import requests
import bs4

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


class TorReq:
    def __init__(self):
        self.session = requests.session()
        self.session.proxies = {
            "http": "socks5h://127.0.0.1:9050",
            "https": "socks5h://127.0.0.1:9050",
        }
        self.nvisited = 0
        self.response = ""

    def get(self):
        # for seed in SEEDLIST:
        #     response = requests.get(seed)
        #     print(response.status_code)

        try:
            response = self.session.get(
                "http://vww6ybal4bd7szmgncyruucpgfkqahzddi37ktceo3ah7ngmcopnpyyd.onion"
            ).content
        except Exception as e:
            print(e)
            pass

        self.response = response
        self.nvisited += 1

    def fetch_links(self):
        soup = bs4.BeautifulSoup(self.response, "lxml")
        links = soup.find_all("a")
        for link in links:
            url = link.get("href")
            print(url)


x = TorReq()


x.get()
x.fetch_links()
