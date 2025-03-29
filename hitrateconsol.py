import requests
import json
import os
from dotenv import load_dotenv
from collections import Counter
import pandas as pd
import time
from datetime import datetime
from supabase import create_client,Client
load_dotenv()
supaUrl = os.getenv("SUPABASE_URL")
supaKey = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supaUrl, supaKey)




def fetch_all_data(table):
    page = 1
    all_data = []
    while True:
        response = supabase.table(table).select("*").range((page-1)*1000, page*1000-1).execute()
        
        if not response.data:
            break
        
        all_data.extend(response.data)
        page += 1
    
    return all_data


HitRateData = fetch_all_data("HitRates")
FinalData = fetch_all_data("FinalData")

killStats = {}
headShotStats = {}
for finalsource in FinalData:
    try:
        if "Kills" in finalsource["Stat_Type"] or "kills" in finalsource["Stat_Type"]:
            currentPlayer = finalsource["Player"]
            lowestLine = 100
            try:
                if float(finalsource["PrizePicks_Line"]) < lowestLine:
                    lowestLine = float(finalsource["PrizePicks_Line"])
            except:
                pass
            try:
                if float(finalsource["Underdog_Line"]) < lowestLine:
                    lowestLine = float(finalsource["Underdog_Line"])
            except:
                pass
            try:
                if float(finalsource["ParlayPlay_Line"]) < lowestLine:
                    lowestLine = float(finalsource["ParlayPlayLine"])
            except:
                pass 
            
            for sourcedata in HitRateData:
                try:
                    statPlayer = sourcedata["Player"]
                    if currentPlayer == sourcedata["Player"]:
                        if currentPlayer not in killStats:
                            killStats[currentPlayer] = [[sourcedata["Kills"],sourcedata["Map"],sourcedata["Date"],lowestLine]]
                            print(f"Updated {currentPlayer}'s Hit Rate for Kills")
                        else:
                            killStats[currentPlayer].append([sourcedata["Kills"],sourcedata["Map"],sourcedata["Date"],lowestLine])
                            print(f"Updated {currentPlayer}'s Hit Rate for Kills")
                except:
                    continue
        else:
            currentPlayer = finalsource["Player"]
            lowestLine = 100
            
            if finalsource["PrizePicks_Line"] != "N/A":
                if float(finalsource["PrizePicks_Line"]) < lowestLine:
                    lowestLine = float(finalsource["PrizePicks_Line"])
            if finalsource["Underdog_Line"] != "N/A":
                if float(finalsource["Underdog_Line"]) < lowestLine:
                    lowestLine = float(finalsource["Underdog_Line"])
            if finalsource["ParlayPlay_Line"] != "N/A":
                if float(finalsource["ParlayPlay_Line"]) < lowestLine:
                    lowestLine = float(finalsource["ParlayPlay_Line"])

            for sourcedata in HitRateData:
                try:
                    statPlayer = sourcedata["Player"]
                    if currentPlayer == sourcedata["Player"]:
                        if currentPlayer not in headShotStats:
                            headShotStats[currentPlayer] = [[sourcedata["Headshots"],sourcedata["Map"],sourcedata["Date"],lowestLine]]
                            print(f"Updated {currentPlayer}'s Hit Rate for Headshots")
                        else:
                            headShotStats[currentPlayer].append([sourcedata["Headshots"],sourcedata["Map"],sourcedata["Date"],lowestLine])
                            print(f"Updated {currentPlayer}'s Hit Rate for Headshots")
                except:
                    continue
    except:
        continue


playerHSAverages = {}
for player, stats in headShotStats.items():
    if len(stats) > 6:
        stat_values =[]
        
        dates = [date[2] for date in stats]
        date_counts = Counter(dates)
        single_date = next((date for date, count in date_counts.items() if count == 1), None)
        if single_date:
            index_to_remove = dates.index(single_date)  
            stats.pop(index_to_remove) 

    if len(stats) > 6:
        for stat in stats:
            stat_values.append(stat[0])
            lowestHSLine = stat[3]

        chunked_stats =[]
        try:
            for i in range(0, len(stat_values), 2):
                chunked_stats.append(float(stat_values[i:i+2][0]) + float(stat_values[i:i+2][1]))
        except:
            pass
        recentWeights = chunked_stats[0:4]
        nonRecent = chunked_stats[3:]


        playerHSAverages[player] = []
        Last_5_Rate = 0
        Last_10_Rate = 0
        Last_15_Rate = 0
        AllTime_Rate = 0
        try:
            Last_5 = chunked_stats[0:5]
            summed = 0
            for game in Last_5:
                if game > float(lowestHSLine):
                    summed += 1
            Last_5_Rate = round((summed/5) * 100,2)
            playerHSAverages[player].append(f"L5_{Last_5_Rate}")
        except:
            pass
        try:
            Last_10 = chunked_stats[0:10]
            summed = 0
            for game in Last_10:
                if game > float(lowestHSLine):
                    summed += 1
            Last_10_Rate = round((summed/10) * 100,2)
            playerHSAverages[player].append(f"L10_{Last_10_Rate}")
            
        except:
            pass  

        try:
            Last_15 = chunked_stats[0:15]
            summed = 0
            for game in Last_15:
                if game > float(lowestHSLine):
                    summed += 1
            Last_15_Rate = round((summed/15) * 100,2)
            playerHSAverages[player].append(f"L15_{Last_15_Rate}")

        except:
            pass
        try:
            HitRateAll = chunked_stats
            summed = 0
            for game in HitRateAll:
                if game > float(lowestHSLine):
                    summed += 1
            AllTime_Rate = round((summed/len(HitRateAll)) * 100,2)
            playerHSAverages[player].append(f"AT_{AllTime_Rate}")

        except:
            pass
        
        game_averages = []


        firstThree_ema = pd.Series(recentWeights).ewm(span=2, adjust=False).mean().iloc[-1]
       
        last_ema =pd.Series(nonRecent).ewm(span=4, adjust=False).mean().iloc[-1]
        combined_ema = (firstThree_ema * 0.6) + (last_ema * 0.4) 

        
        playerHSAverages[player].append([round(float(combined_ema),2)])
        playerHSAverages[player].append(lowestHSLine)

       

playerKillAverages = {}
for player, stats in killStats.items():
    if len(stats) > 6:
        stat_values =[]
        dates = [date[2] for date in stats]
        date_counts = Counter(dates)
        single_date = next((date for date, count in date_counts.items() if count == 1), None)
        if single_date:
            index_to_remove = dates.index(single_date)  
            stats.pop(index_to_remove) 

    if len(stats) > 6:
        for stat in stats:
            stat_values.append(stat[0])
            lowestKillLine = stat[3] 

        chunked_stats =[]
        try:
            for i in range(0, len(stat_values), 2):
                chunked_stats.append(float(stat_values[i:i+2][0]) + float(stat_values[i:i+2][1]))
        except:
            pass
        recentWeights = chunked_stats[0:4]
        nonRecent = chunked_stats[3:]

        playerKillAverages[player] = []
        Last_5_Rate = 0
        Last_10_Rate = 0
        Last_15_Rate = 0
        AllTime_Rate = 0
        try:
            Last_5 = chunked_stats[0:5]
            summed = 0
            for game in Last_5:
                if game > float(lowestKillLine):
                    summed += 1
            Last_5_Rate = round((summed/5) * 100,2)
            playerKillAverages[player].append(f"L5_{Last_5_Rate}")
        except:
            pass
        try:
            Last_10 = chunked_stats[0:10]
            summed = 0
            for game in Last_10:
                if game > float(lowestKillLine):
                    summed += 1
            Last_10_Rate = round((summed/10) * 100,2)
            playerKillAverages[player].append(f"L10_{Last_10_Rate}")
            
        except:
            pass  

        try:
            Last_15 = chunked_stats[0:15]
            summed = 0
            for game in Last_15:
                if game > float(lowestKillLine):
                    summed += 1
            Last_15_Rate = round((summed/15) * 100,2)
            playerKillAverages[player].append(f"L15_{Last_15_Rate}")

        except:
            pass
        try:
            HitRateAll = chunked_stats
            summed = 0
            for game in HitRateAll:
                if game > float(lowestKillLine):
                    summed += 1
            AllTime_Rate = round((summed/len(HitRateAll)) * 100,2)
            playerKillAverages[player].append(f"AT_{AllTime_Rate}")

        except:
            pass       

        game_averages = []


        firstThree_ema = pd.Series(recentWeights).ewm(span=2, adjust=False).mean().iloc[-1]
       
        last_ema =pd.Series(nonRecent).ewm(span=4, adjust=False).mean().iloc[-1]
        combined_ema = (firstThree_ema * 0.6) + (last_ema * 0.4) 

        playerKillAverages[player].append(round(float(combined_ema),2))
        playerKillAverages[player].append(lowestKillLine)





print("HelloWORLD")
