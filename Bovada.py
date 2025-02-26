import requests
import json
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

BOVADA = os.getenv("BOVADA")


payload = {}
headers = {
  'Cookie': 'Device-Type=Desktop|false; TS01890ddd=014b5d5d07e05445c24eeaf64c61aedeb71bc04be1e372aae1f1b7c47e126fe903d9e5f97509b021554690626b0a1c63c669b4614c; VISITED=true; variant=v:0|lgn:0|dt:d|os:ns|cntry:US|cur:USD|jn:0|rt:o|pb:0'
}

response = requests.request("GET", BOVADA, headers=headers, data=payload)
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







