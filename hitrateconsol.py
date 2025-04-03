import os
from dotenv import load_dotenv
from collections import Counter
import pandas as pd
from datetime import datetime
from supabase import create_client,Client
load_dotenv()
supaUrl = os.getenv("SUPABASE_URL")
supaKey = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supaUrl, supaKey)


def parse_date_safely(date_str):
            """Try multiple date formats to parse a date string."""
            date_str = date_str.replace(" EST", "")
            
            formats = [
                "%Y-%m-%d %H:%M:%S",  # 2025-03-10 08:00:00
                "%Y, %B %d, %H:%M",   # 2025, March 10, 08:00
                "%B %d, %H:%M",       # March 10, 08:00
                "%Y-%m-%d %H:%M"      # 2025-03-10 08:00
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
                    
            raise ValueError(f"Could not parse date: {date_str}")



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
    lowestLine = "N/A"
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
                    lowestLine = float(finalsource["ParlayPlay_Line"])
            except:
                pass
            try:
                if float(finalsource["HotstreakLine"]) < lowestLine:
                    lowestLine = float(finalsource["HotstreakLine"])
            except:
                pass
            
            for sourcedata in HitRateData:
                try:
                    statPlayer = sourcedata["Player"]
                    if currentPlayer.lower() == statPlayer.lower():
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
                    lowestLine = float(finalsource["ParlayPlay_Line"])
            except:
                pass
            try:
                if float(finalsource["HotstreakLine"]) < lowestLine:
                    lowestLine = float(finalsource["HotstreakLine"])
            except:
                pass

            for sourcedata in HitRateData:
                try:
                    statPlayer = sourcedata["Player"]
                    if currentPlayer.lower() == statPlayer.lower():
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
        # try:
        #     for date in stats:
        #         format_str = "%Y-%m-%d %H:%M:%S"
        #         try:
        #             datetime.strptime(date[2], format_str)
        #         except ValueError:
        #             try:
        #                 date_str = date[2]
        #                 date_str_no_tz = date_str.replace(" EST", "")
                        
        #                 date_obj = datetime.strptime(date_str_no_tz, "%B %d, %H:%M")
                        
        #                 date_obj = date_obj.replace(year=2025)
                        
        #                 formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S") + " EST"
        #                 date[2] = formatted_date
                        
        #                 print(f"Successfully converted '{date_str}' to '{formatted_date}'")
        #             except ValueError as e:
        #                 print(f"Failed to parse date '{date[2]}': {e}")
        # except Exception as e:
        #     print(f"Error processing dates: {e}")



        # Use this function for sorting
        try:
            stats.sort(key=lambda x: parse_date_safely(x[2]), reverse=True)
            print("Successfully sorted dates!")
        except Exception as e:
            print(f"Error sorting dates: {e}")
            # Optionally print the problematic dates
            for s in stats:
                print(f"Date: {s[2]}")        




    if len(stats) > 8:
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
            Last_5_Rate = round((summed/5) * 100)
            playerHSAverages[player].append(f"L5_{Last_5_Rate}")
        except:
            pass
        try:
            Last_10 = chunked_stats[0:10]
            summed = 0
            for game in Last_10:
                if game > float(lowestHSLine):
                    summed += 1
            Last_10_Rate = round((summed/10) * 100)
            playerHSAverages[player].append(f"L10_{Last_10_Rate}")
            
        except:
            Last_10_Rate = "Not Enough Data"
            pass  

        try:
            Last_15 = chunked_stats[0:15]
            summed = 0
            for game in Last_15:
                if game > float(lowestHSLine):
                    summed += 1
            Last_15_Rate = round((summed/15) * 100)
            playerHSAverages[player].append(f"L15_{Last_15_Rate}")

        except:
            Last_15_Rate = "Not Enough Data"

            pass
        try:
            HitRateAll = chunked_stats
            summed = 0
            for game in HitRateAll:
                if game > float(lowestHSLine):
                    summed += 1
            AllTime_Rate = round((summed/len(HitRateAll)) * 100)
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
    if len(stats) > 8:
        stat_values =[]
        dates = [date[2] for date in stats]
        date_counts = Counter(dates)
        single_date = next((date for date, count in date_counts.items() if count == 1), None)
        if single_date:
            index_to_remove = dates.index(single_date)  
            stats.pop(index_to_remove) 
        
        try:
            stats.sort(key=lambda x: parse_date_safely(x[2]), reverse=True)
            print("Successfully sorted dates!")
        except Exception as e:
            print(f"Error sorting dates: {e}")
            for s in stats:
                print(f"Date: {s[2]}")        



    if len(stats) > 8:
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
            Last_5_Rate = round((summed/5) * 100)
            playerKillAverages[player].append(f"L5_{Last_5_Rate}")
        except:
            pass
        try:
            Last_10 = chunked_stats[0:10]
            summed = 0
            for game in Last_10:
                if game > float(lowestKillLine):
                    summed += 1
            Last_10_Rate = round((summed/10) * 100)
            playerKillAverages[player].append(f"L10_{Last_10_Rate}")
            
        except:
            pass  

        try:
            Last_15 = chunked_stats[0:15]
            summed = 0
            for game in Last_15:
                if game > float(lowestKillLine):
                    summed += 1
            Last_15_Rate = round((summed/15) * 100)
            playerKillAverages[player].append(f"L15_{Last_15_Rate}")

        except:
            pass
        try:
            HitRateAll = chunked_stats
            summed = 0
            for game in HitRateAll:
                if game > float(lowestKillLine):
                    summed += 1
            AllTime_Rate = round((summed/len(HitRateAll)) * 100)
            playerKillAverages[player].append(f"AT_{AllTime_Rate}")

        except:
            pass       

        game_averages = []


        firstThree_ema = pd.Series(recentWeights).ewm(span=2, adjust=False).mean().iloc[-1]
       
        last_ema =pd.Series(nonRecent).ewm(span=4, adjust=False).mean().iloc[-1]
        combined_ema = (firstThree_ema * 0.6) + (last_ema * 0.4) 

        playerKillAverages[player].append(round(float(combined_ema),2))
        playerKillAverages[player].append(lowestKillLine)


for player_lines in FinalData:

    # Initialize variables (default values)
    Player_Insert = player_lines["Player"]
    Matchup_Insert = player_lines["Matchup"]
    Stat_Type_Insert = player_lines["Stat_Type"]
    PrizePicks_Insert = player_lines["PrizePicks_Line"]
    Underdog_Insert = player_lines["Underdog_Line"]
    ParlayPlay_Insert = player_lines['ParlayPlay_Line']
    HotStreak_Insert = player_lines['HotstreakLine']
    HotStreakOver_Insert = player_lines['HotstreakOver']
    HotStreakUnder_Insert = player_lines['HotstreakUnder']
    Date_Insert = player_lines["Date"]
    
    stats_List = None
    Last5_Insert = None
    Last10_Insert = None
    Last15_Insert = None
    AllTime_Insert = None
    EMA_Insert = None
    LowestLine_Insert = None

    # Determine which stats source to use
    if "Kills" in Stat_Type_Insert or "kills" in Stat_Type_Insert:
        stats_source = playerKillAverages
    else:
        stats_source = playerHSAverages

    try:
        # Fetch the stats for the player
        stats_List = stats_source[Player_Insert]
        
        # Extract values from the stats list (assuming format is consistent)
        Last5_Insert = stats_List[0].split("_")[1]
        Last10_Insert = stats_List[1].split("_")[1]
        Last15_Insert = stats_List[2].split("_")[1]
        AllTime_Insert = stats_List[3].split("_")[1]
        try:
            EMA_Insert = str(round(stats_List[4]))
        except:
            EMA_Insert = str(round(stats_List[4][0]))
 # Convert to string
        LowestLine_Insert = str(stats_List[5])  # Convert to string
    except KeyError:
        Last5_Insert = "No Data Available"
        Last10_Insert = "No Data Available"
        Last15_Insert = "No Data Available"
        AllTime_Insert = "No Data Available"
        EMA_Insert = "No Data Available"
        LowestLine_Insert = "No Data Available"
        print(f"No stats found for {Player_Insert}")
        pass  # Skip the current iteration if no stats available

    try:
        # Prepare the data for insertion into the database
        data = {
            "Player": Player_Insert,
            "Matchup": Matchup_Insert,
            "Stat_Type": Stat_Type_Insert, 
            "PrizePicks": PrizePicks_Insert,
            "Underdog": Underdog_Insert,
            "ParlayPlay": ParlayPlay_Insert,
            "HotStreak": HotStreak_Insert,
            "Over": HotStreakOver_Insert,
            "Under": HotStreakUnder_Insert,
            "Date": Date_Insert,
            "L5": Last5_Insert,
            "L10": Last10_Insert,
            "L15": Last15_Insert,
            "AllTime": AllTime_Insert,
            "EMA": EMA_Insert,
            "LowestLine": LowestLine_Insert
        }

        # Insert into the database
        insert = supabase.table("FinalConsolidated").insert(data).execute()
        print(insert)
    except Exception as e:
        print(f"Error while trying to insert data for {Player_Insert}: {e}")
        continue



                

