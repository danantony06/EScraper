import requests
import json
from supabase import create_client,Client
import os
from dotenv import load_dotenv
load_dotenv()


#BOVADA = os.getenv("BOVADA")
supaUrl = os.getenv("SUPABASE_URL")
supaKey = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supaUrl, supaKey)
games = "https://guest.api.arcadia.pinnacle.com/0.1/sports/12/matchups?withSpecials=true&withThreeWaySpecials=true&brandId=0"
prices = "https://guest.api.arcadia.pinnacle.com/0.1/sports/12/markets/straight?primaryOnly=false&withSpecials=true&withThreeWaySpecials=true&moneylineOnly=true"




payload = {}
headers = {}

gameData = requests.request("GET", games, headers=headers, data=payload)
priceData = requests.request("GET", prices, headers=headers, data=payload)

db = gameData.json()
cc = priceData.json()


gameDict = {}
for games in db:
    if "CS2" in games['league']['name']:
        if games['id'] not in gameDict:
            gameDict[games['id']] = [games['participants'][0]['name'], games['participants'][1]['name'],games['startTime']]

gameID = {}

for prices in cc:
    for id in gameDict:
        if id == prices['matchupId']:
            gameID[tuple(gameDict[id])] = [prices['prices'][0]['price'],prices['prices'][1]['price']]



finalDict = {}
for teams in gameDict.values():
    for price in gameID:
        if tuple(teams) == price:
            if tuple(teams) not in finalDict:
                finalDict[tuple(teams)] = gameID[price]

source = "Pinnacle"
response = supabase.table("Game Odds").delete().eq("Source", "Pinnacle").execute()


for match,odds in finalDict.items():
    Team1 = match[0]
    Team2 = match[1]
    date = match[2]
    odds1 = odds[0]
    odds2 = odds[1]

    data = {
        "MatchupID": f"{Team1} vs. {Team2}",
        "Team 1": Team1,
        "Team 2": Team2,
        "Date" : None,
        "LineType": "ML",
        "Odds 1": odds1,
        "Odds 2": odds2,
        "Source": source,
        "Date": date
    }

    response = supabase.table("Game Odds").insert(data).execute()

    print(response)

    
        
