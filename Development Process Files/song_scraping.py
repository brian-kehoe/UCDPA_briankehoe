import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.azlyrics.com/lyrics/shayneward/icry.html'
response = requests.get(url)
html_soup = BeautifulSoup(response.text, 'html.parser')
singer = html_soup.find('div', class_='lyricsh').h2.text
song_name = \
    html_soup.find('div', class_='col-xs-12 col-lg-8 text-center').find_all('div', class_='div-share')[1].text.split(
        '"')[1]
lyrics = html_soup.find('div', class_='col-xs-12 col-lg-8 text-center').find_all('div')[5].text

data = {'singer': singer, 'song_name': song_name, 'lyrics': lyrics}

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)

import requests
import random

headers_list = [{
    'authority': 'httpbin.org',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'accept-language': 'en-US,en;q=0.9',
    'sec-fetch-dest': 'document',
}  # , {...}
]
headers = random.choice(headers_list)
response = requests.get('https://airquality.ie/assets/php/get-monitors.php', headers=headers)
print(response.json())


