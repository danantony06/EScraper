import requests
import cloudscraper
import os
from dotenv import load_dotenv
from supabase import Client,create_client

load_dotenv()

supaUrl = os.getenv("SUPABASE_URL")
supaKey = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supaUrl, supaKey)
PARLAYPLAY = os.getenv("PARLAYPLAY")
delete = supabase.table("ParlayPlay").delete().eq("Source", "ParlayPlay").execute()

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
            matches[entry['match']['matchGroup']].update([f"{entry['match']['homeTeam']['teamname']}({entry['match']['homeWinProb']}) VS. {entry['match']['awayTeam']['teamname']}({entry['match']['awayWinProb']})*->{entry['match']['matchDate']}"])
        else:
            matches[entry['match']['matchGroup']] = {f"{entry['match']['homeTeam']['teamname']}({entry['match']['homeWinProb']}) VS. {entry['match']['awayTeam']['teamname']}({entry['match']['awayWinProb']})*->{entry['match']['matchDate']}"}
    
    for entry in data:
        if len(entry['stats']) == 2:
            players[f"{entry['player']['fullName']}({entry['player']['team']['teamname']})"] = [f"{entry['stats'][0]['altLines']['values'][0]['marketName']}({entry['stats'][0]['altLines']['values'][0]['selectionPoints']})",f"{entry['stats'][-1]['altLines']['values'][0]['marketName']}({entry['stats'][1]['altLines']['values'][0]['selectionPoints']})"]
        else:
            players[f"{entry['player']['fullName']}({entry['player']['team']['teamname']})"] = [f"{entry['stats'][0]['altLines']['values'][0]['marketName']}({entry['stats'][0]['altLines']['values'][0]['selectionPoints']})"]

         

  

    for player in players:
       for match in matches.values():
            for game in match:
                n = player.find("(")
                player_team = player[n+1:-1].strip()
                if player_team in game:
                    if game not in finalDict:
                        finalDict[game] = [[player, players[player]]]
                    else:
                        finalDict[game].append([player,players[player]])
                    

    for matchup,lines in finalDict.items():
        matchupId = matchup[:matchup.find("*")]
        date = matchup[(matchup.find(">") + 1):]
        for line in lines:
            try:
                player = line[0]
                i = 0
                while i < 2:
                    stat_type = line[1][i][:line[1][i].find("(")]
                    stat_line = line[1][i][line[1][i].find("(")+1:-1]
                    i += 1

                    data = {
                        "Matchup": matchupId,
                        "Player":player,
                        "stat_type":stat_type,
                        "stat_line":stat_line,
                        "Date": date,
                        "Source": "ParlayPlay"
                    }
                    insert = supabase.table("ParlayPlay").insert(data).execute()
                    print(insert)
            except:
                continue




                

else:
    print(f"Error: {response.status_code}")
