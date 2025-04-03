import requests
import json
import os
from dotenv import load_dotenv
import time
from datetime import datetime
from supabase import create_client,Client
load_dotenv()
supaUrl = os.getenv("SUPABASE_URL")
supaKey = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supaUrl, supaKey)


delete = supabase.table("FinalData").delete().neq("id", 0).execute()


PrizePicksData = (supabase.table("PrizePicks").select("*").execute())
UnderdogData = (supabase.table("Underdog").select("*").execute())
HotStreakData = (supabase.table("HotStreak").select("*").execute())
ParlayPlayData = (supabase.table("ParlayPlay").select("*").execute())
HitRateData = (supabase.table("HitRates").select("*").execute())


players = {}

correctPlayerNames = []
for source_data in [PrizePicksData]:
    for data in source_data:
        try:
            for row in data[1]:
                name = row["Player"]
                if name[-1] == "-":
                    name = name[:-1]
                correctPlayerNames.append(name)
        except:
            continue

for source_data in [PrizePicksData,UnderdogData,HotStreakData,ParlayPlayData]:
    for data in source_data:
        try:
            for row in data[1]:
                try:
                    source = row["Source"]
                    if source == "Hotstreak":
                        matchup = row["Matchup"]
                        currentPlayer = row["Player"]
                        for names in correctPlayerNames:
                            if currentPlayer.lower() == names.lower():
                                currentPlayer = names
                                break
                        stat_type = row["stat_type"]
                        stat_line = row["stat_line"]
                        date1 = row["Date"]
                        date_obj = datetime.strptime(date1, "%Y-%m-%dT%H:%M:%S")
                        gameDate = date_obj.strftime("%B %d, %Y %I:%M %p")
                        overOdds = float(row["Over"])
                        decimalOver = 1/overOdds
                        if decimalOver > 2:
                            americanOver = (decimalOver-1) * 100
                        elif decimalOver < 2:
                            americanOver = round(-1*(100/ (decimalOver-1)))
                        underOdds = float(row["Under"])
                        decimalUnder = 1/underOdds
                        if decimalUnder > 2: 
                            americanUnder = (decimalUnder-1)*100
                        elif decimalUnder < 2:
                            americanUnder = round(-1*(100/ (decimalUnder-1)))


                    if source == "ParlayPlay":
                        matchup = row["Matchup"]
                        currentPlayer = row["Player"][:row["Player"].find("(")]
                        for names in correctPlayerNames:
                            if currentPlayer.lower() == names.lower():
                                currentPlayer = names
                                break
                        playerTeam = row["Player"][row["Player"].find("(")+1:-1]
                        stat_type = row["stat_type"]
                        stat_line = row["stat_line"]
                        date1 = row["Date"]
                        date_obj = datetime.strptime(date1, "%Y-%m-%dT%H:%M:%S")
                        gameDate = date_obj.strftime("%B %d, %Y %I:%M %p")

                    if source == "Underdog":
                        matchup = row["Matchup"]
                        currentPlayer = row["Player"]
                        if currentPlayer[-1] == "-":
                            currentPlayer = currentPlayer[:-1]
                        for names in correctPlayerNames:
                            if currentPlayer.lower() == names.lower():
                                currentPlayer = names
                                break
                        stat_type = row["stat_type"]
                        stat_line = row["stat_line"]
                        date1 = row["Date"]
                        date_obj = datetime.strptime(date1, "%Y-%m-%dT%H:%M:%SZ")
                        gameDate = date_obj.strftime("%B %d, %Y %I:%M %p")

                    if source == "PrizePicks":
                        currentPlayer = row["Player"]
                        stat_type = row["stat_type"]
                        if stat_type == "MAP 3 Kills" or stat_type == "MAP 3 Headshots":
                            continue
                        stat_line = row["stat_line"]
                        date1 = row["Date"]
                        date_obj = datetime.strptime(date1, "%Y-%m-%dT%H:%M:%S")
                        gameDate = date_obj.strftime("%B %d, %Y %I:%M %p")

                        
                    if currentPlayer not in players:
                        players[currentPlayer] = {}

                    if stat_type not in players[currentPlayer]:
                        players[currentPlayer][stat_type] = {}
                    if source == "ParlayPlay":
                        players[currentPlayer][stat_type][source] = stat_line,matchup,gameDate
                    elif source == "Hotstreak":
                        players[currentPlayer][stat_type][source] = stat_line,matchup,gameDate,americanOver,americanUnder
                    elif source == "Underdog":
                        players[currentPlayer][stat_type][source] = stat_line,matchup,gameDate

                    else:
                        players[currentPlayer][stat_type][source] = stat_line,gameDate
                except:
                    continue
        except:
            continue

finalAssigns = {}
for player, stats in players.items():
    finalAssigns[player] = []
    for stat_type, sources in stats.items():
        entry = {}
        for source, line in sources.items():
            if source == "ParlayPlay":
                entry[source] = [stat_type, line[0],line[1],line[2]]
            elif source == "Hotstreak":
                entry[source] = [stat_type, line[0],line[1],line[2],line[3],line[4]]
            elif source == "Underdog":
                entry[source] = [stat_type, line[0],line[1],line[2]]
            else:
                entry[source] = [stat_type,line[0],line[1]]
        finalAssigns[player].append(entry)

# print(finalAssigns)


HeadshotData = {}
KillData = {}
# for player,lines in finalAssigns.items():
#     KillData[player] = []
#     for sportsBook in lines:
#         for book,data in sportsBook.items():
#             if "Kills" in data[0] or "kills" in data[0]:
#                 if book == "PrizePicks":
#                     PrizePicksLine = data[1]
#                     gameDate = data[2]
#                     KillData[player].append(f"PP:{PrizePicksLine}")
#                 if book == "Underdog":
#                     UnderdogLine = data[1]
#                     gameDate = data[3]
#                     UDMatchup = data[2]
#                     KillData[player].append(f"UD:{UnderdogLine}")
#                 if book == "Hotstreak":
#                     HotstreakLine = data[1]
#                     gameDate = data[3]
#                     HSMatchup = data[2]
#                     HSOver = data[4]
#                     HSUnder = data[5]
#                     KillData[player].append(f"HOT:{HotstreakLine},{HSOver},{HSUnder}")

#                 if book == "ParlayPlay":
#                     PPMatchup = data[2]
#                     gameDate = data[3]
#                     ParlayPlayLine = data[1]
#                     KillData[player].append(f"PPLAY:{ParlayPlayLine}")
                
#                 try:
#                     if PPMatchup:
#                         KillData[player].append(f"Matchup:{PPMatchup}")
#                     elif HSMatchup:
#                         KillData[player].append(f"Matchup:{HSMatchup}")
#                     elif UDMatchup:
#                         KillData[player].append(f"Matchup:{UDMatchup}")
#                 except:
#                     try:
#                         if HSMatchup:
#                             KillData[player].append(f"Matchup:{HSMatchup}")
#                         elif UDMatchup:
#                             KillData[player].append(f"Matchup:{UDMatchup}")
#                     except:
#                         try:
#                             if UDMatchup:
#                                 KillData[player].append(f"Matchup:{UDMatchup}")
#                         except:
#                             continue
#                 KillData[player].append(f"Date:{gameDate}")



# for player,odds in KillData.items():
#     playerInsert = player
#     for odd in odds:
#         if "PP" in odd:
#             PPLine = odd[odd.find(":")+1:]
#         if "UD" in odd:
#             UDLine = odd[odd.find(":")+1:]
#         if "HOT" in odd:
#             Hot = odd[odd.find(":")+1:]
#             Hot = Hot.split(",")
#             HotLine = Hot[0]
#             HotOver = Hot[1]
#             HotUnder = Hot[2]
#         if "Matchup" in odd:
#             gameMatchup = odd[odd.find(":")+1:]
#         if "Date" in odd:
#             finalDate = odd[odd.find(":")+1:]
        
#     data = {
#                       "Player": playerInsert,
#                       "Stat_Type": "Map 1-2 Kills",
#                       "PrizePicks_Line":PPLine,
#                       "Underdog_Line":UDLine,
#                       "ParlayPlay_Line":PPLine,
#                       "HotstreakLine":HotLine,
#                       "HotstreakOver":HotOver ,
#                       "HotstreakUnder":HotUnder,
#                       "Matchup": gameMatchup,
#                       "Date": finalDate,
#                   }
#     insert = supabase.table("FinalData").insert(data).execute()
#     print(insert)




for player,lines in finalAssigns.items():
    KillData[player] = []
    for sportsBook in lines:
        for book,data in sportsBook.items():
            if "Kills" in data[0] or "kills" in data[0]:
                PPMatchup = None
                HSMatchup = None
                UDMatchup = None
                if book == "PrizePicks":
                    PrizePicksLine = data[1]
                    gameDate = data[2]
                    KillData[player].append(f"PP:{PrizePicksLine}")
                if book == "Underdog":
                    UnderdogLine = data[1]
                    gameDate = data[3]
                    UDMatchup = data[2]
                    KillData[player].append(f"UD:{UnderdogLine}")
                if book == "Hotstreak":
                    HotstreakLine = data[1]
                    gameDate = data[3]
                    HSMatchup = data[2]
                    HSOver = data[4]
                    HSUnder = data[5]
                    KillData[player].append(f"HOT:{HotstreakLine},{HSOver},{HSUnder}")

                if book == "ParlayPlay":
                    PPMatchup = data[2]
                    gameDate = data[3]
                    ParlayPlayLine = data[1]
                    KillData[player].append(f"Parlay:{ParlayPlayLine}")
                
                try:
                    if PPMatchup:
                        KillData[player].append(f"Matchup:{PPMatchup}")
                    elif HSMatchup:
                        KillData[player].append(f"Matchup:{HSMatchup}")
                    elif UDMatchup:
                        KillData[player].append(f"Matchup:{UDMatchup}")
                except:
                    try:
                        if HSMatchup:
                            KillData[player].append(f"Matchup:{HSMatchup}")
                        elif UDMatchup:
                            KillData[player].append(f"Matchup:{UDMatchup}")
                    except:
                        try:
                            if UDMatchup:
                                KillData[player].append(f"Matchup:{UDMatchup}")
                        except:
                            continue
                KillData[player].append(f"Date:{gameDate}")






                



for player,odds in KillData.items():
    playerInsert = player
    PPLine = None
    ParlayLine = None
    UDLine = None
    HotLine = None
    HotOver = None
    HotUnder = None
    gameMatchup = None
    finalDate = None
    for odd in odds:
        if "Parlay" in odd:
            ParlayLine = odd[odd.find(":")+1:]
        if "PP" in odd:
            PPLine = odd[odd.find(":")+1:]
        if "UD" in odd:
            UDLine = odd[odd.find(":")+1:]
        if "HOT" in odd:
            Hot = odd[odd.find(":")+1:]
            Hot = Hot.split(",")
            HotLine = Hot[0]
            try:
                HotOver = Hot[2]
                HotUnder = Hot[1]
            except:
                pass
        if "Matchup" in odd:
            gameMatchup = odd[odd.find(":")+1:]
        if "Date" in odd:
            finalDate = odd[odd.find(":")+1:]
    if PPLine == None:
        PPLine = "N/A"
    if UDLine == None:
        UDLine = "N/A"
    if ParlayLine == None:
        ParlayLine = "N/A"
    if HotLine == None:
        HotLine = "N/A"
    data = {
                      "Player": playerInsert,
                      "Stat_Type": "Map 1-2 Kills",
                      "PrizePicks_Line":PPLine,
                      "Underdog_Line":UDLine,
                      "ParlayPlay_Line":ParlayLine,
                      "HotstreakLine":HotLine,
                      "HotstreakOver":HotOver ,
                      "HotstreakUnder":HotUnder,
                      "Matchup": gameMatchup,
                      "Date": finalDate,
                  }
    insert = supabase.table("FinalData").insert(data).execute()
    print(insert)


for player,lines in finalAssigns.items():
    HeadshotData[player] = []
    for sportsBook in lines:
        for book,data in sportsBook.items():
            if "Headshots" in data[0] or "headshots" in data[0]:
                PPMatchup = None
                HSMatchup = None
                UDMatchup = None
                if book == "PrizePicks":
                    PrizePicksLine = data[1]
                    gameDate = data[2]
                    HeadshotData[player].append(f"PP:{PrizePicksLine}")
                if book == "Underdog":
                    UnderdogLine = data[1]
                    gameDate = data[3]
                    UDMatchup = data[2]
                    HeadshotData[player].append(f"UD:{UnderdogLine}")
                if book == "Hotstreak":
                    HotstreakLine = data[1]
                    gameDate = data[3]
                    HSMatchup = data[2]
                    HSOver = data[4]
                    HSUnder = data[5]
                    HeadshotData[player].append(f"HOT:{HotstreakLine},{HSOver},{HSUnder}")

                if book == "ParlayPlay":
                    PPMatchup = data[2]
                    gameDate = data[3]
                    ParlayPlayLine = data[1]
                    HeadshotData[player].append(f"Parlay:{ParlayPlayLine}")
                
                try:
                    if PPMatchup:
                        HeadshotData[player].append(f"Matchup:{PPMatchup}")
                    elif HSMatchup:
                        HeadshotData[player].append(f"Matchup:{HSMatchup}")
                    elif UDMatchup:
                        HeadshotData[player].append(f"Matchup:{UDMatchup}")
                except:
                    try:
                        if HSMatchup:
                            HeadshotData[player].append(f"Matchup:{HSMatchup}")
                        elif UDMatchup:
                            HeadshotData[player].append(f"Matchup:{UDMatchup}")
                    except:
                        try:
                            if UDMatchup:
                                HeadshotData[player].append(f"Matchup:{UDMatchup}")
                        except:
                            continue
                HeadshotData[player].append(f"Date:{gameDate}")






                



for player,odds in HeadshotData.items():
    playerInsert = player
    PPLine = None
    ParlayLine = None
    UDLine = None
    HotLine = None
    HotOver = None
    HotUnder = None
    gameMatchup = None
    finalDate = None
    for odd in odds:
        if "Parlay" in odd:
            ParlayLine = odd[odd.find(":")+1:]
        if "PP" in odd:
            PPLine = odd[odd.find(":")+1:]
        if "UD" in odd:
            UDLine = odd[odd.find(":")+1:]
        if "HOT" in odd:
            Hot = odd[odd.find(":")+1:]
            Hot = Hot.split(",")
            HotLine = Hot[0]
            try:
                HotOver = Hot[2]
                HotUnder = Hot[1]
            except:
                pass
        if "Matchup" in odd:
            gameMatchup = odd[odd.find(":")+1:]
        if "Date" in odd:
            finalDate = odd[odd.find(":")+1:]
    if PPLine == None:
        PPLine = "N/A"
    if UDLine == None:
        UDLine = "N/A"
    if ParlayLine == None:
        ParlayLine = "N/A"
    if HotLine == None:
        HotLine = "N/A"    
    data = {
                      "Player": playerInsert,
                      "Stat_Type": "Map 1-2 Headshots",
                      "PrizePicks_Line":PPLine,
                      "Underdog_Line":UDLine,
                      "ParlayPlay_Line":ParlayLine,
                      "HotstreakLine":HotLine,
                      "HotstreakOver":HotOver ,
                      "HotstreakUnder":HotUnder,
                      "Matchup": gameMatchup,
                      "Date": finalDate,
                  }
    insert = supabase.table("FinalData").insert(data).execute()
    print(insert)

