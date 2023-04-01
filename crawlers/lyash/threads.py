import requests
import threading
import time
from seed_list import SEEDLIST
import ping
import asyncio


def launch_crawler(url):
    asyncio.run(ping.fetch(url))


THREADS = 6

threads = []

for i in range(THREADS):
    threads.append(threading.Thread(target=launch_crawler, args=(SEEDLIST.pop(),)))
    # threads.append(threading.Thread(target=lambda: launch_crawler(SEEDLIST.pop())))
    pass

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()


# # Define a list of URLs to scrape
# urls = [
#     'https://www.example.com/page1',
#     'https://www.example.com/page2',
#     'https://www.example.com/page3',
#     # Add more URLs here...
# ]
#
# # Define a function that performs the scraping
# def scrape_url(url):
#     # Make a request to the URL
#     response = requests.get(url)
#
#     # Process the response data here...
#     print(response.content)
#
# # Define the number of threads to use
# num_threads = 5
#
# # Define a function that runs the scraping function in a thread
# def run_scraping_thread():
#     while urls:
#         # Get the next URL from the list
#         url = urls.pop(0)
#
#         # Scrape the URL
#         scrape_url(url)
#
# # Create a list of threads
# threads = []
# for i in range(num_threads):
#     # Create a new thread and add it to the list
#     t = threading.Thread(target=run_scraping_thread)
#     threads.append(t)
#
# # Start the threads
# for t in threads:
#     t.start()
#
# # Wait for all threads to complete
# for t in threads:
#     t.join()
#
# # Sleep for a bit to avoid overwhelming the website with requests
# time.sleep(1)
