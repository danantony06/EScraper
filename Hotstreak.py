import requests
import json
import os
from dotenv import load_dotenv
import time


from supabase import create_client,Client

load_dotenv()
supaUrl = os.getenv("SUPABASE_URL")
supaKey = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supaUrl, supaKey)
HOTSTREAK = os.getenv("HOTSTREAK")

# finalData = {}

delete = supabase.table("HotStreak").delete().eq("Source", "Hotstreak").execute()

for i in range(1,20):
  # time.sleep(5)
  finalData = {}
  finalDict = {}
  player_dict = {}
  payload = json.dumps({
    "operationName": "search",
    "query": "query search($query: String, $page: Int, $gameFilter: [String!], $sportFilter: [String!], $teamFilter: [String!], $positionFilter: [String!], $categoryFilter: [String!], $promotedFilter: Boolean, $participantFilter: [String!], $leagueFilter: [String!]) { search(query: $query, page: $page, gameFilter: $gameFilter, sportFilter: $sportFilter, teamFilter: $teamFilter, positionFilter: $positionFilter, categoryFilter: $categoryFilter, promotedFilter: $promotedFilter, participantFilter: $participantFilter, leagueFilter: $leagueFilter) {\n        __typename\ngeneratedAt\ncategoryFilters {\n\n__typename\ncount\ngeneratedAt\nkey\nmeta\nname\n\n}\ngameFilters {\n\n__typename\ncount\ngeneratedAt\nkey\nmeta\nname\n\n}\ngames {\n\n__typename\nid\n... on EsportGame {\n\n__typename\nid\nminimumNumberOfGames\nvideogameTitle\n\n}\n... on GolfGame {\n\n__typename\nid\npairings {\n\n__typename\nid\nbackNine\ncreatedAt\ngameId\ngeneratedAt\nparticipantIds\nteeTime\nupdatedAt\n\n}\ntournament {\n\n__typename\nid\nname\n\n}\n\n}\nleagueId\nopponents {\n\n__typename\nid\ndesignation\ngameId\nteam {\n\n__typename\nid\ncolors {\n\n__typename\nprimary\nsecondary\n\n}\ncreatedAt\ngeneratedAt\nlogoUrl\nmarket\nname\nshortName\nupdatedAt\n\n}\n\n}\nperiod\nreplay\nscheduledAt\nstatus\n\n}\nleagueFilters {\n\n__typename\ncount\ngeneratedAt\nkey\nmeta\nname\n\n}\nmarkets {\n\n__typename\nid\ngeneratedAt\nlines\noptions\nprobabilities\n\n}\nparticipants {\n\n__typename\nid\ncategories\nopponentId\nplayer {\n\n__typename\nid\ndisplayName\nexternalId\nfirstName\nheadshotUrl\ninjuries {\n\n__typename\nid\ncomment\ncreatedAt\ndescription\ngeneratedAt\nstatus\nstatusDate\nupdatedAt\n\n}\nlastName\nnickname\nnumber\nposition\nshortDisplayName\ntraits\n\n}\nposition\n\n}\npositionFilters {\n\n__typename\ncount\ngeneratedAt\nkey\nmeta\nname\n\n}\nsportFilters {\n\n__typename\ncount\ngeneratedAt\nkey\nmeta\nname\n\n}\nteamFilters {\n\n__typename\ncount\ngeneratedAt\nkey\nmeta\nname\n\n}\nstats\ntotalCount\n\n      } }",
    "variables": {
      "query": "*",
      "page": i,
      "sportFilter": [
        "Sport:A0mfMN"
      ]
    }
  })
  headers = {
    'content-type': 'application/json',
    'origin': 'https://app.hotstreak.gg',
    'referer': 'https://app.hotstreak.gg/',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-platform': '"Windows"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'x-requested-with': 'web',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJIb3RTdHJlYWsgKHByb2R1Y3Rpb24pIiwic3ViIjoiSHNmOjpVc2VyOkpwdG12NEciLCJleHAiOjE3NDU3MjY1NzcsImlhdCI6MTc0MzA0ODE3N30.C3j9IJpUxlts4RuesLP6BHvQh0AoxvgNlE2B952y8LU'
  }
  try:
      response = requests.request("POST", HOTSTREAK, headers=headers, data=payload)
      time.sleep(5)
      # print(response.status_code)
      # print(response.text)
      data = response.json()
     ########## print(data['data'])
    #   # data['data']['search']['games'] --> game matchups
      for player in data['data']['search']['markets']:
        playerAttributes = player['id'].split(",")
        player_id = playerAttributes[0]
        stat_type = playerAttributes[1]
        stat_line = player['lines'][0]
        stat_odds = player['probabilities'][0]
        if player_id not in player_dict:
          player_dict[player_id] = [[stat_type,stat_line,stat_odds]]
        else:
          player_dict[player_id].append([stat_type,stat_line,stat_odds])


    #     # Create player dictionary mapping player_id as key to stat type, stat_line, and stat_odds as a list key

      for key in player_dict:
        for participant in data['data']['search']['participants']:
          if key == participant['id']:
            opponentId = participant['opponentId']
            for game in data['data']['search']['games']:
              for opponent in game['opponents']:
                if opponentId == opponent['id']:
                  gameId = opponent['gameId']
                  for gameFilter in data['data']['search']['gameFilters']:
                    if gameId == gameFilter['key']:
                      player_matchup = f"{gameFilter['meta']['teams']['home']} vs. {gameFilter['meta']['teams']['away']}"
                      date = gameFilter['meta']['scheduled_at']

        
            player_name = participant['player']['displayName'] 
            player_headshot = participant['player']['headshotUrl']
            finalDict[player_name] = [[player_dict[key],player_matchup,date]]


      
      finalData.update(finalDict)


      for player, details in finalData.items():
          for entry in details:
              stats, match, match_time = entry
              for stat in stats:
                  stat_name, value, probabilities = stat
                  data = {
                      "Player": player,
                      "stat_type": stat_name,
                      "stat_line": value,
                      "Over": probabilities[0],
                      "Under": probabilities[1],
                      "Matchup": match,
                      "Date": match_time,
                      "Source": "Hotstreak"
                  }
                  insert = supabase.table("HotStreak").insert(data).execute()
                  print(insert)
  except:
    continue



              







#   # CS:GO Sport:A0mfMN
#   # print(json.dumps(data, indent=2))

