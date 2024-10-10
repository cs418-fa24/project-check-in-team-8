import pandas as pd
import numpy as np
import requests
import csv
from bs4 import BeautifulSoup

obj = {}
header = []
done = False
for team in ['dal', 'phi', 'wsh', 'nyg']:
    url = f'https://www.espn.com/nfl/team/stats/_/name/{team}/season/2024'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('section', class_='StatLeaders')

    name_arr = soup.find_all('span', class_='db')
    team_name = f'{name_arr[0].text} {name_arr[1].text}'
    obj[team_name] = []

    for item in table.find_all('a'):
        stat_type = item.find('h2').text
        name = item.find('span', class_='Athlete__PlayerName').text
        stat = item.find('div', class_='clr-gray-01').text
        if not done:
            header.extend([f'{stat_type} Leader', f'{stat_type}'])
        obj[team_name].extend([name, stat])
    done = True

    for i in range(len(obj[team_name]), 10):
       obj[team_name].append('N/A')

df = pd.DataFrame(data=obj, index=header).T
df.to_csv('NFC_East.csv', header=True, index=True, index_label='Team')