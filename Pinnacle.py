import requests
import json
games = "https://guest.api.arcadia.pinnacle.com/0.1/leagues/230488/matchups?brandId=0"
prices = "https://guest.api.arcadia.pinnacle.com/0.1/leagues/230488/markets/straight"




payload = {}
headers = {}

gameData = requests.request("GET", games, headers=headers, data=payload)
priceData = requests.request("GET", prices, headers=headers, data=payload)

db = gameData.json()
cc = priceData.json()
print(db)

