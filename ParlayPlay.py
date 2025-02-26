import requests
import cloudscraper
import os
from dotenv import load_dotenv

load_dotenv()
PARLAYPLAY = os.getenv("PARLAYPLAY")

matches = {}
players = {}
finalDict = {}

scraper = cloudscraper.create_scraper()

headers = {
    'x-requested-with': 'XMLHttpRequest',
    'x-parlay-request': '1',
    'x-parlayplay-platform': 'web',
    'Cookie': 'sessionid=hac7837fqtzflespad1rv13cx6c1vj0a' 
}

response = scraper.get(PARLAYPLAY, headers=headers,allow_redirects=False)

if response.status_code == 200:

    data = response.json()["players"]

    for entry in data: #Aggregate All Game Matchups along with ParlayPlay's Odds on the games
        if entry['match']['matchGroup'] in matches:
            matches[entry['match']['matchGroup']].update([f"{entry['match']['homeTeam']['teamname']}({entry['match']['homeWinProb']}) VS. {entry['match']['awayTeam']['teamname']}({entry['match']['awayWinProb']})"])
        else:
            matches[entry['match']['matchGroup']] = {f"{entry['match']['homeTeam']['teamname']}({entry['match']['homeWinProb']}) VS. {entry['match']['awayTeam']['teamname']}({entry['match']['awayWinProb']})"}
    
    for entry in data:
        if len(entry['stats']) == 2:
            players[f"{entry['player']['fullName']} {entry['player']['team']['teamname']}"] = [f"{entry['stats'][0]['altLines']['values'][0]['marketName']}({entry['stats'][0]['altLines']['values'][0]['selectionPoints']})",f"{entry['stats'][-1]['altLines']['values'][0]['marketName']}({entry['stats'][0]['altLines']['values'][0]['selectionPoints']})"]
        else:
            players[f"{entry['player']['fullName']} {entry['player']['team']['teamname']}"] = [f"{entry['stats'][0]['altLines']['values'][0]['marketName']}({entry['stats'][0]['altLines']['values'][0]['selectionPoints']})"]

         

  

    for player in players:
       for match in matches.values():
            for game in match:
                n = player.find(" ")
                player_team = player[n:].strip()
                if player_team in game:
                    if game not in finalDict:
                        finalDict[game] = [[player, players[player]]]
                    else:
                        finalDict[game].append([player,players[player]])
                    
    print(finalDict)




else:
    print(f"Error: {response.status_code}")
