import requests
import os
from dotenv import load_dotenv
from supabase import create_client,Client
load_dotenv()


supaUrl = os.getenv("SUPABASE_URL")
supaKey = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supaUrl, supaKey)

UNDERDOG = os.getenv("UNDERDOG")



Underdog = requests.get(UNDERDOG)
Underdog_CS2_Lines = {} #Initialize Final Dictionary for storing player lines
playerTeam = {}

if Underdog.status_code == 200:
    EsportsProps = Underdog.json() #parse JSON Data
    for player in EsportsProps['players']:
        pName = player['last_name']
        playerID = player['id']
        for appearance in EsportsProps['appearances']:
            if appearance["player_id"] == playerID:
                playerTeam[pName] = appearance["team_id"]
    for prop in EsportsProps['over_under_lines']: #Loop through all over under lines
        seperator = prop['over_under']['title'].find(" ") 
        name = prop['over_under']['title'][0:seperator] #Seperate name from string
        stat_type = prop['over_under']['title'][seperator+1:] #Seperate stat type from string
        line = prop['stat_value'] #Get the line value
        if name not in Underdog_CS2_Lines: #Either insert or append into dictionary based on player name
            Underdog_CS2_Lines[name] = [[stat_type,line]]
        else:
            if [stat_type,line] not in Underdog_CS2_Lines[name]:
                Underdog_CS2_Lines[name].append([stat_type,line])

for player in Underdog_CS2_Lines:
    if player == "":
        for game in EsportsProps['games']:
            for playerLines in Underdog_CS2_Lines[player]:
                participant = playerLines[0][:playerLines[0].find(" ")]
                if participant in playerTeam:
                    if playerTeam[participant] == game['away_team_id'] or playerTeam[participant] == game['home_team_id']:
                        if [game['scheduled_at'],game['title']] not in playerLines:
                            playerLines.append([game['scheduled_at'],game['title']])
    else: 
        for game in EsportsProps['games']:
            if player in playerTeam:
                if playerTeam[player] == game['away_team_id'] or playerTeam[player] == game['home_team_id']:
                    Underdog_CS2_Lines[player].append([game['scheduled_at'],game['title']])


delete = supabase.table("Underdog").delete().eq("Source", "Underdog").execute()

for player,lines in Underdog_CS2_Lines.items():
    if player == "":
        for playerLines in Underdog_CS2_Lines[player]:
            participant = None
            stat_type = None
            stat_line = None
            date = None
            matchup = None
            participant = playerLines[0][:playerLines[0].find(" ")]
            stat_type = playerLines[0][playerLines[0].find(" "):]
            stat_line = playerLines[1]
            if len(playerLines) > 2:
                date = playerLines[2][0]
                matchup = playerLines[2][1]
            anonData = {
            "Player":participant,
            "Matchup":matchup,
            "stat_type":stat_type,
            "stat_line":stat_line,
            "Date":date,
            "Source":"Underdog"
            }
            insert = supabase.table("Underdog").insert(anonData).execute()
    if len(lines) > 4:
        continue
    if len(lines) == 3:
        participant = None
        stat_type = None
        stat_line = None
        date = None
        matchup = None
        participant = player
        for line in lines[0:2]:
            stat_type = line[0]
            stat_line = line[1]
            date = lines[2][0]
            matchup = lines[2][1]
            multiMatch = {
                "Player":participant,
                "Matchup":matchup,
                "stat_type":stat_type,
                "stat_line":stat_line,
                "Date":date,
                "Source":"Underdog"
            }
            insert = supabase.table("Underdog").insert(multiMatch).execute()


    else: 
        participant = player
        date = lines[2][0]
        matchup = lines[2][1]
        for line in lines[0:2]:
            stat_type = line[0]
            stat_line = line[1]
            data = {
                "Player":participant,
                "Matchup":matchup,
                "stat_type":stat_type,
                "stat_line":stat_line,
                "Date":date,
                "Source":"Underdog"
            }
            insert = supabase.table("Underdog").insert(data).execute()


        




