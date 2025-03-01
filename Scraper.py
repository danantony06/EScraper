
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import requests
import json

url = 'https://bo3.gg/players?period=last_6_months&tiers=s,a,b&tab=main&sort=rating&order=desc'

players = []

statsPage = requests.get(url)
soup = BeautifulSoup(statsPage.text, features="html.parser")
gb = soup.prettify()
json_data = json.dumps({"gb": gb})
soupDivs = soup.find_all('div', class_ = "player-info")

for div in soupDivs:
    gg = div.find("nickname")
    print(gg)
# url = 'https://app.prizepicks.com/board'
# Lines = requests.get(url)
# ppSoup = BeautifulSoup(Lines.text,features = 'html.parser')
# print(ppSoup.prettify())