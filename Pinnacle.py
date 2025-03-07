import requests
import json
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
            gameDict[games['id']] = [games['participants'][0]['name'], games['participants'][1]['name']]

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
print(finalDict)
        
