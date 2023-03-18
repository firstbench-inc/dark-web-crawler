import re
import requests
from collections import Counter
from bs4 import BeautifulSoup


keyword = "ASCII"
url = ["https://www.programiz.com/c-programming/examples/ASCII-value-character"]


class CrawlerPipeline:
    def simple_filter():
        for i in range(len(url)):
            url_check = requests.get(url[i])
            if url_check.status_code == 200:
                html_code = url_check.content.decode()
                soup = BeautifulSoup(html_code, "html.parser")

                text = soup.get_text()
                sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)

                for line in sentences:
                    if keyword in line:
                        print(line)
                image_tags = soup.find_all("img")

                # img extract

                image_urls = []
                for tag in image_tags:
                    if "src" in tag.attrs:
                        image_urls.append(tag["src"])

                for img_url in image_urls:
                    print(img_url)
