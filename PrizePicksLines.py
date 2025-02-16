import requests

lineApi = 'https://partner-api.prizepicks.com/projections?league_id=265'
playerApi = 'https://partner-api.prizepicks.com/projections?per_page=1000'

stat_kind = {}
playerData = {}
finalizedData = {}


lines = requests.get(lineApi)
players = requests.get(playerApi) # Theese are the API requests to get JSON data regarding players and lines
if lines.status_code and players.status_code== 200:

   #Initialized empty dictionary at the beggining of the file. Now we will loop through player JSON Data where we will be mapping player ID to player name
    for player in players.json()['included']:
         if player['type'] == "new_player":
              playerData[player['id']]= player['attributes']['name']
              
    #Initialized empty dictionary for stat_kind at the beggining of the file. Now we will loop through line JSON Data where we will be mapping player ID to stat type and line score          
    lineData = lines.json()['data'] #JSON daata for player line and line type
    for object in lineData:
            if object['relationships']['new_player']['data']['id'] not in stat_kind:
                stat_kind[object['relationships']['new_player']['data']['id']] = [[object['attributes']['stat_type'],object['attributes']['line_score']]]
            else:
                stat_kind[object['relationships']['new_player']['data']['id']].append([object['attributes']['stat_type'],object['attributes']['line_score']])
    
    for line in stat_kind:
         for player in playerData:
              if player == line:
                   finalizedData[playerData[player]] = stat_kind[line]
    print(finalizedData)
                   
         
else:
    print(f"Error:{lines.status_code}")