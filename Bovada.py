import requests
import json
import datetime
#import os
#from dotenv import load_dotenv
#load_dotenv()

#BOVADA = os.getenv("BOVADA")

url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/esports/counter-strike-2?marketFilterId=def&liveOnly=false&eventsLimit=50&lang=en"

payload = {}
headers = {
  'Cookie': 'Device-Type=Desktop|false; _hjSessionUser_510373=eyJpZCI6ImU2OGQ3NDllLWNhMGMtNWM5OC05MjNmLTc1NDNiOTQyZDAwYSIsImNyZWF0ZWQiOjE3Mzk5MDQ5MDUyMjgsImV4aXN0aW5nIjp0cnVlfQ==; VISITED=true; ln_grp=2; odds_format=AMERICAN; variant=jn:0|dt:d|os:ns|cntry:US|cur:USD|lgn:0|pb:0; LANG=en; _hjSession_510373=eyJpZCI6IjkzYzU3OWJmLTljNDgtNDA1Ny1iYTczLWMxZjQ0NTBlODlhZSIsImMiOjE3NDA1MTE1NzE0MjgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; wt_rla=205099820688534%2C3%2C1740518026908; JSESSIONID=F4E261C76C99E6E5CE42C3BB72D4FA42; TS01890ddd=014b5d5d079d3657daf3e03cb3c8311d5fde8e3437487d1a0b338e4f2ebc6cd67792964008db4b9fce7f936cadd941b02e5d883755ea7fa2dd86328ed31e9c841cdf01e18969001ff4bbdab3ca9ab7937f8d7ee3f3efbc0b842269690868d5d5aef880f031bbcfa48d8e3c1977a9b267307dfa8c5d; Device-Type=Desktop|false; TS01890ddd=014b5d5d07933e3c25f64c5e8fced5c655fe8c87410829bb6c00106e743f0de6dc678de2114f7061fcd9a359bc006730b6f7441fe9; VISITED=true; variant=v:0|lgn:0|dt:d|os:ns|cntry:US|cur:USD|jn:0|rt:o|pb:0'
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


print(finalDict)







