from scrapy import settings
from scrapy.exceptions import IgnoreRequest
import random
import logging
from urllib.parse import urlparse

class Proxies(object):
    """proxy"""

    def incoming_requests(self, request, spider):
        uri = urlparse(request.url)
        domain = f"{uri.scheme}://{uri.netloc}/"
        
        if ".onion" in domain:
            non_http_link = domain.split(".")[-2].replace("https://", "").replace("http://", "")
            
            if domain[-7:-1] != ".onion" or len(non_http_link) != 16 or len(non_http_link) !=56:
                logging.info("Not valid .onion link, ignoring")
                raise IgnoreRequest()
            
            #proxy lists
            if uri.scheme == "https:":
                proxy_list = settings.get(HTTPS_TOR_PROXIES)
            else:
                proxy_list = settings.get(HTTP_TOP_PROXIES)
            
            edited_uri = uri.replace(".onion", "")
            seed_hash = f"{edited_uri.netloc}"
            random.seed(seed_hash)
            
            request.meta["proxy"] = random.choice(proxy_list)
            
class LimitDomains(object):
    def incoming_requests(self, request, spider):
        host_name = urlparse(request.url).hostname.split(".")
        if len(host_name > 4):
            request.meta["proxy"] = ""
            logging.info(f"Ignoring {request.url}, too many domains")
            raise IgnoreRequest()
                
        