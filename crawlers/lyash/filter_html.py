import re
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse

keyword = "tor"
# url = [
#     "https://www.w3schools.com/charsets/ref_html_ascii.asp",
#     "https://www.cs.cmu.edu/~pattis/15-1XX/common/handouts/ascii.html",
#     "https://www.ascii-code.com/",
#     "https://www.rapidtables.com/code/text/ascii-table.html",
# ]


# def simple_filter(url):
#     # for i in url:
#         # url_check = requests.get(url)
#         if url_check.status_code == 200:
#             html_code = url_check.content.decode()
#             soup = BeautifulSoup(html_code, "html.parser")

#             text = soup.get_text()
#             sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)

#             # for line in sentences:
#             #     if keyword in line:
#             #         print(line)

#             image_tags = soup.find_all("img")

#             if not os.path.exists("crawlers/lyash/filter-results"):
#                 os.mkdir("crawlers/lyash/filter-results")

#             image_urls = []
#             for l in image_tags:
#                 if "src" in l.attrs:
#                     image_urls.append(l["src"])

#             url1 = (url[8:] if "https" in url else url[7:]) + ".txt"
#             if os.name == "posix":
#                 url1 = url1.replace(r"/", "\\")
#             print(url1)
#             output_file = os.path.join("crawlers/lyash/filter-results", url1)
#             f = open(output_file, "w")
#             for k in image_urls:
#                 f.write(k + "\n")
#             for line in sentences:
#                 if keyword in line:
#                         f.write(line + "\n")


def good_filter(url_check, url, keyword="tor"):
    # url_check = url_check.content.decode()
    soup = BeautifulSoup(url_check, "html.parser")

    text = soup.get_text()
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)

    # for line in sentences:
    #     if keyword in line:
    #         print(line)

    image_tags = soup.find_all("img")

    if not os.path.exists("crawlers/lyash/filter-results"):
        os.mkdir("crawlers/lyash/filter-results")

    image_urls = []
    for l in image_tags:
        if "src" in l.attrs:
            image_urls.append(l["src"])

    url1 = (url[8:] if "https" in url else url[7:]) + ".txt"
    if os.name == "posix":
        url1 = url1.replace(r"/", "\\")
    # print(url1)
    output_file = os.path.join("crawlers/lyash/filter-results", url1)
    f = open(output_file, "w")
    for k in image_urls:
        f.write(k + "\n")
    for line in sentences:
        if keyword in line:
            f.write(line + "\n")
