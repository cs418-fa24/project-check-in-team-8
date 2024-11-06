import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

obj = {}
obj['Name'] = []
obj['Draft Pick'] = []
obj['Date'] = []    
obj['Game Result (W/L)'] = []
obj['Passing Completions'] = []
obj['Passing Attempts'] = []
obj['Passing Yards'] = []
obj['Passing Touchdowns'] = []
obj['Interceptions'] = []
obj['Passer Rating'] = []
obj['Times Sacked'] = []
obj['Rushing Attempts'] = []
obj['Rushing Yards'] = []
obj['Rushing Touchdowns'] = []
obj['Fumbles'] = []


year = 2018
draft_url = f'https://www.pro-football-reference.com/years/{year}/draft.htm'

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}
response = requests.get(draft_url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('tbody')

links = []
pickDict = {}
for row in table.find_all('tr'):
    pos = row.find('td', {'data-stat' : 'pos'})
    if pos != None and pos.text == 'QB':
        player = row.find('td', {'data-stat' : 'player'})
        player_link = player.find('a')
        links.append(player_link['href'].split('.')[0])

        pick_no = row.find('td', {'data-stat' : 'draft_pick'}).text
        player_name = player.text

        pickDict[player_name] = pick_no


for link in links:
    gamelog_url = f'https://www.pro-football-reference.com{link}/gamelog/'
    gamelog_soup = BeautifulSoup(requests.get(gamelog_url, headers=headers).text, 'html.parser')

    name = gamelog_soup.find('h1').text.strip()
    pick = pickDict[name]

    for week in gamelog_soup.select('#stats > tbody > tr'):

        gs = week.find('td', {'data-stat' : 'gs'})
        if gs == None or gs.text.strip() != '*':
            continue

        obj['Name'].append(name)
        obj['Draft Pick'].append(pick)

        date = week.find('td', {'data-stat' : 'game_date'}).text.strip()
        obj['Date'].append(date)

        result = week.find('td', {'data-stat' : 'game_result'}).text.strip()[0]
        obj['Game Result (W/L)'].append(result)

        comps = week.find('td', {'data-stat' : 'pass_cmp'}).text
        obj['Passing Completions'].append(comps)

        atts = week.find('td', {'data-stat' : 'pass_att'}).text
        obj['Passing Attempts'].append(atts)

        passyds = week.find('td', {'data-stat' : 'pass_yds'}).text
        obj['Passing Yards'].append(passyds)

        passtds = week.find('td', {'data-stat' : 'pass_td'}).text
        obj['Passing Touchdowns'].append(passtds)

        ints = week.find('td', {'data-stat' : 'pass_int'}).text
        obj['Interceptions'].append(ints)

        qbr = week.find('td', {'data-stat' : 'pass_rating'}).text
        obj['Passer Rating'].append(qbr)

        sacks = week.find('td', {'data-stat' : 'pass_sacked'}).text
        obj['Times Sacked'].append(sacks)

        rushatts = week.find('td', {'data-stat' : 'rush_att'}).text
        obj['Rushing Attempts'].append(rushatts)

        rushyds = week.find('td', {'data-stat' : 'rush_yds'}).text
        obj['Rushing Yards'].append(rushyds)

        rushtds = week.find('td', {'data-stat' : 'rush_td'}).text
        obj['Rushing Touchdowns'].append(rushtds)

        fumbles = week.find('td', {'data-stat' : 'fumbles'}).text
        obj['Fumbles'].append(fumbles)


df = pd.DataFrame(obj)
df.to_csv("2018.csv")
