import requests
import os
from dotenv import load_dotenv
from supabase import create_client,Client

load_dotenv()
PRIZELINES = os.getenv("PRIZEPICKS1")
PRIZEPLAYERS  = os.getenv("PRIZEPICKS2")

supaUrl = os.getenv("SUPABASE_URL")
supaKey = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supaUrl, supaKey)




stat_kind = {}
playerData = {}
finalizedData = {}


lines = requests.get(PRIZELINES)
players = requests.get(PRIZEPLAYERS) # Theese are the API requests to get JSON data regarding players and lines
if lines.status_code and players.status_code== 200:

   #Initialized empty dictionary at the beggining of the file. Now we will loop through player JSON Data where we will be mapping player ID to player name
    for player in players.json()['included']:
         if player['type'] == "new_player":
              playerData[player['id']]= player['attributes']['name']
              
    #Initialized empty dictionary for stat_kind at the beggining of the file. Now we will loop through line JSON Data where we will be mapping player ID to stat type and line score          
    lineData = lines.json()['data'] #JSON daata for player line and line type
    for object in lineData:
            if object['relationships']['new_player']['data']['id'] not in stat_kind:
                stat_kind[object['relationships']['new_player']['data']['id']] = [[object['attributes']['stat_type'],object['attributes']['line_score'],object['attributes']['start_time']]]
            else:
                stat_kind[object['relationships']['new_player']['data']['id']].append([object['attributes']['stat_type'],object['attributes']['line_score'],object['attributes']['start_time']])
    
    for line in stat_kind:
         for player in playerData:
              if player == line:
                   finalizedData[playerData[player]] = stat_kind[line]


Source = "PrizePicks"
delete = supabase.table("PrizePicks").delete().eq("Source", "PrizePicks").execute()

for player,lines in finalizedData.items():
     player = player
     for line in lines:
        stat_type = line[0]
        stat_line = line[1]
        date = line[2]
        data = {
               "Player": player,
               "stat_type":stat_type,
               "stat_line":stat_line, 
               "Date": date,
               "Source":Source
        }
        insert = supabase.table("PrizePicks").insert(data).execute()
        print(insert)
