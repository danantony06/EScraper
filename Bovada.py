import requests
import json
import datetime
import pandas as pd
from supabase import create_client,Client
import os
from dotenv import load_dotenv
load_dotenv()


#BOVADA = os.getenv("BOVADA")
supaUrl = os.getenv("SUPABASE_URL")
supaKey = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supaUrl, supaKey)

url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/esports?marketFilterId=def&liveOnly=true&eventsLimit=50&lang=en"

payload = {}
headers = {
  'Cookie': 'Device-Type=Desktop|false; _hjSessionUser_510373=eyJpZCI6ImU2OGQ3NDllLWNhMGMtNWM5OC05MjNmLTc1NDNiOTQyZDAwYSIsImNyZWF0ZWQiOjE3Mzk5MDQ5MDUyMjgsImV4aXN0aW5nIjp0cnVlfQ==; VISITED=true; variant=v:1|lgn:0|dt:d|os:w|cntry:US|cur:USD|jn:0|rt:o|pb:0; AB=variant; LANG=en; _hjSession_510373=eyJpZCI6IjI1OTgxN2UwLTA2YzUtNGZmNi05ZTRjLWI4NjQ2MjgyOWFhOCIsImMiOjE3NDEzNzE1NjYyMjgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; ln_grp=2; odds_format=AMERICAN; JSESSIONID=BFF4A481E2DAE0CA25787AC2240E35C7; TS01890ddd=014b5d5d07cba6f7e0df4254a5edd218a7c4f57f7c7c7957866edbaeaf3084756c59b09dfc3d7ba1ab83b6c241c7405439492355b970d65d69e10a040353a2f197b26e41dc404e6605323cc854bbf66928c94f78dd8239ec37d62a9043f58568b93d508ec27c112c1fde95c5005af3ff8ac20a3197adb6e22e7dbb7bf74286f840454b4e9d; wt_rla=205099820688534%2C8%2C1741371566156; Device-Type=Desktop|false; TS01890ddd=014b5d5d076bfca20dbf5d925f1e23a29328a698587ffe36e52ac99ee020dc725a99465e4bc834798171d1ab940e9272acaac40e94; VISITED=true; variant=v:0|lgn:0|dt:d|os:ns|cntry:US|cur:USD|jn:0|rt:o|pb:0',
  'Accept-Language': 'en-US,en;q=0.9',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)
data = response.json()

gameMatchups = {}
moneyLines = {}
totalLines = {}
spreadLines = {}

for path in data:
  for i in range (len(path['events'])):
    gameMatchups[path['events'][i]['description']] = path['events'][i]['startTime']
    for b in range(len(path['events'][i]['displayGroups'][0]['markets'])):
      if path['events'][i]['displayGroups'][0]['markets'][b]['description'] == "Moneyline":
        moneyLines[path['events'][i]['displayGroups'][0]['markets'][b]['outcomes'][0]['description']] = path['events'][i]['displayGroups'][0]['markets'][b]['outcomes'][0]['price']['american']
        moneyLines[path['events'][i]['displayGroups'][0]['markets'][b]['outcomes'][1]['description']] = path['events'][i]['displayGroups'][0]['markets'][b]['outcomes'][1]['price']['american']
      if path['events'][i]['displayGroups'][0]['markets'][b]['description'] == "Total":
        totalLines[path['events'][i]['description']] = [[path['events'][i]['displayGroups'][0]['markets'][b]['outcomes'][0]['description'], path['events'][i]['displayGroups'][0]['markets'][b]['outcomes'][0]['price']['american'], path['events'][i]['displayGroups'][0]['markets'][b]['outcomes'][0]['price']['handicap']],[path['events'][i]['displayGroups'][0]['markets'][b]['outcomes'][1]['description'], path['events'][i]['displayGroups'][0]['markets'][b]['outcomes'][1]['price']['american'], path['events'][i]['displayGroups'][0]['markets'][b]['outcomes'][1]['price']['handicap']]]
      if path['events'][i]['displayGroups'][0]['markets'][b]['description'] == "Point Spread":
        spreadLines[path['events'][i]['displayGroups'][0]['markets'][b]['outcomes'][0]['description']] = [path['events'][i]['displayGroups'][0]['markets'][b]['outcomes'][0]['price']['american'],path['events'][i]['displayGroups'][0]['markets'][b]['outcomes'][0]['price']['handicap']]
        spreadLines[path['events'][i]['displayGroups'][0]['markets'][b]['outcomes'][1]['description']] = [path['events'][i]['displayGroups'][0]['markets'][b]['outcomes'][1]['price']['american'],path['events'][i]['displayGroups'][0]['markets'][b]['outcomes'][1]['price']['handicap']]


finalDict = {}
for matchup in gameMatchups:
  for moneyline in moneyLines:
    if moneyline in matchup:
      time = gameMatchups[matchup]
      if f"{matchup}({datetime.datetime.fromtimestamp(time/1000)})" not in finalDict:
        finalDict[f"{matchup}({datetime.datetime.fromtimestamp(time/1000)})"] = [f"{moneyline} ML:{moneyLines[moneyline]}"]
      else:
        finalDict[f"{matchup}({datetime.datetime.fromtimestamp(time/1000)})"].append(f"{moneyline} ML:{moneyLines[moneyline]}")
  for spreadline in spreadLines:
    if spreadline in matchup:
      finalDict[f"{matchup}({datetime.datetime.fromtimestamp(time/1000)})"].append(f"{spreadline}: {spreadLines[spreadline][1]} spread at {spreadLines[spreadline][0]}")
  for totalline in totalLines:
    if totalline in matchup:
      finalDict[f"{matchup}({datetime.datetime.fromtimestamp(time/1000)})"].append(f"Over/Under {totalLines[totalline][0][2]} total rounds: {totalLines[totalline][0][1]}/{totalLines[totalline][1][1]}")






delete = supabase.table("Game Odds").delete().eq("Source", "Bovada").execute()

for game,odds in finalDict.items():
  index = game.find("(")
  matchup = game[:index]
  date = game[index + 1:-1]
  team1index = matchup.find(" ")
  Team1 = matchup[:team1index]
  Team2 = matchup[(team1index + 3):]
  for odd in odds:
    odds_type = None
    odds1 = None
    odds2 = None
    spreadline = None
    odds_provider = "Bovada"  # Change this if using multiple providers

    if 'ML' in odd:
        team, ml = odd.split(" ML:")
        odds_type = "ML"
        if team.strip() == Team1:
            odds1 = ml
        else:
            odds2 = ml
    elif 'spread' in odd:
        team, spread = odd.split(" spread at ")
        odds_type = "spread"
        if team[:team.find(":")] == Team1:
            odds1 = spread
            spreadLine = team[team.find(":"):] 
        else:
            odds2 = spread
            spreadLine = team[team.find(":")+1:] 

    elif 'Over/Under' in odd:
        odds_type = "O/U"
        odds1, odds2 = odd.split(":")[1].strip().split('/')



    if odds1 or odds2:
      data = {
              "MatchupID": matchup,
                "Team 1": Team1,
                "Team 2": Team2,
                "LineType": odds_type,
                "Odds 1": odds1,
                "Odds 2": odds2,
                "Source": odds_provider,
                "Date": date
            }
      
      insert = supabase.table("Game Odds").insert(data).execute()
      # print(delete)
      # print(insert)

      

# df = pd.DataFrame(finalDict)
# df.to_csv('bovada_odds_pandas.csv', index=False)
# print("Data saved to bovada_odds_pandas.csv")








