
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import requests

# url = 'https://bo3.gg/players?period=last_6_months&tiers=s,a,b&tab=main&sort=rating&order=desc'

# statsPage = requests.get(url)
# soup = BeautifulSoup(statsPage.text, features="html.parser")
# #print(soup.prettify())
# soupDivs = soup.find_all('div', class_ = "player-info")
# for div in soupDivs:
#     print(div)
url = 'https://app.prizepicks.com/board'
Lines = requests.get(url)
ppSoup = BeautifulSoup(Lines.text,features = 'html.parser')
print(ppSoup.prettify())