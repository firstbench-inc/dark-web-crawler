
import re
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse

keyword = 'ASCII'
url = ['https://www.w3schools.com/charsets/ref_html_ascii.asp']

def simple_filter():
    for i in range(len(url)):
        url_check = requests.get(url[i])
        if url_check.status_code == 200:
            html_code = url_check.content.decode()
            soup = BeautifulSoup(html_code, 'html.parser')

            text = soup.get_text()
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

            # for line in sentences:
            #     if keyword in line:
            #         print(line)

            image_tags = soup.find_all('img')

            if not os.path.exists('crawler-filter/simple_filter'):
                os.mkdir('crawler-filter/simple_filter') 

            image_urls = []
            for l in image_tags:
                if 'src' in l.attrs:
                    image_urls.append(l['src'])

            output_file = os.path.join('crawler-filter/simple_filter', "image.txt")
            with open(output_file, "w") as f:
                for k in image_urls:
                    f.write(k + "\n")
                for line in sentences:
                 if keyword in line:
                    f.write(line +"\n")
simple_filter()


    
  