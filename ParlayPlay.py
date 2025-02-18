import requests
import cloudscraper

matches = {}
players = {}

scraper = cloudscraper.create_scraper()
url = "https://parlayplay.io/api/v1/crossgame/search/?sport=eSports&league=CSGO&includeAlt=true&version=2&includeBoost=true"

headers = {
    'x-requested-with': 'XMLHttpRequest',
    'x-parlay-request': '1',
    'x-parlayplay-platform': 'web',
    'Cookie': 'sessionid=hac7837fqtzflespad1rv13cx6c1vj0a' 
}

response = scraper.get(url, headers=headers,allow_redirects=False)

# Optionally, if the response is JSON, you can parse and print it as a dictionary
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

         

  
    print(players)




         # If the response is in JSON format
else:
    print(f"Error: {response.status_code}")
