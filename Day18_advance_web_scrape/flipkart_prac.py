"""
    pip install fake-useragent
"""

import random

import requests
from fake_useragent import UserAgent
import time
from bs4 import BeautifulSoup

url = "https://www.flipkart.com/search?q=vastrado%20shirts&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

headers = {
    'User-Agent' : UserAgent().random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'content-type': 'text/html; charset=utf-8',
    'content-encoding': 'gzip',
    'Referer': 'https://www.google.com',
    'Connection' : 'keep-alive',
    # 'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'en-US,en;q=0.9'
}

proxy_list = [
    "163.61.134.53:8080",
    "154.18.220.190:5678",
    "173.245.49.69:80"
]

proxy = random.choice(proxy_list)

proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }

s = requests.Session()

time.sleep(2)
response = s.get(url, headers=headers)


with open("Database/flipkartpage.html", "w", encoding='utf-8') as f:
    soup = BeautifulSoup(response.text, 'html.parser')
    f.write(soup.prettify())

with open("Database/flipkart_all_links", "w") as f:
    links = []
    # print(soup.select("a"))
    for link in soup.select("a"):
        links.append(link.get('href'))
    
    f.write(str(links))
    # print(links)