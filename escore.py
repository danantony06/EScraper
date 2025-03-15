from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pdb
import itertools
from supabase import create_client,Client
import os
from dotenv import load_dotenv
load_dotenv()

supaUrl = os.getenv("SUPABASE_URL")
supaKey = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supaUrl, supaKey)

# Set up Selenium WebDriver (Make sure you have ChromeDriver installed)
driver = webdriver.Chrome()  


# ################delete = supabase.table("HitRates").delete().eq("Source", "Escore").execute()



teamNames = []  # List of Team names for all top rated teams
completedGames =[] #Expanding list of completed games to make sure matches arent double counted
playerTeam = {} # Dictionary assigning players to their teams
statTracker = {}


ogUrl = f'https://escorenews.com/en/csgo/team?s=3'  #OG Website to get top Ranked Teams
driver.get(ogUrl)
time.sleep(3)
soup = BeautifulSoup(driver.page_source, "html.parser")  #Load Page
rankTable = soup.find("table",id="team_s")              #Find Tables with top-Ranked Teams
allTeamUrls = rankTable.find_all("a",class_= "teamNameIco")   
for teamUrl in allTeamUrls:
    url = teamUrl.get("href") #Get all hrefs to go to expanded versions of each Team
    teamName = url.split('/')[3] +" " + url.split('/')[4]  #Slice href to get team Name and append to teamNames list
    teamNames.append(teamName)
    driver.get(f'https://escorenews.com{url}') #Load in expanded team view
    soup = BeautifulSoup(driver.page_source, "html.parser")
    rosterTable = soup.find("table",class_ ="table table-hover table-striped table-sm const")  #Gather roster data of team
    rosterAnchors = rosterTable.find_all("a",class_ = "playerName")
    for anchor in rosterAnchors:
        if anchor.find("span") != None:         #Loop through players in teams roster and store in playerTeam Dict
            player = anchor.find("span").get_text().strip()
            playerTeam[player] = teamName
    recentMatchesTable = soup.find("div", id="matches_s2")  #Find div with all teams recent matches
    recentMatches = recentMatchesTable.find_all("a",class_ = "article v_gl704")
    for match in recentMatches:
        if match.get("href") != None: #Get every href to go to expanded view of all recent matches
            match = match.get("href")
        if match not in completedGames:  #Check if it is a match we have scraped before, if not, open the expanded view
            driver.get(f'https://escorenews.com{match}')
            soup = BeautifulSoup(driver.page_source,"html.parser")
            if soup.find("span",class_ = "sct") != None:
                matchDate = soup.find("span",class_ = "sct").get_text()
            maps = soup.find_all("strong",class_="map")  #Find the different maps played in the match 
            if len(maps) >= 2:
                mapsPlayed = [maps[0].get_text(),maps[1].get_text()] # Store the maps in a mapsPlayed Variable
                for i in [1, 2]:
                    url = f'https://escorenews.com{match}#{i}' #Use ranged for loop to expand the tables for player data for maps 1 and 2
                    driver.get(url)
                    driver.refresh()
                    time.sleep(1)
                    try:
                        WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located((By.ID, "match_data1")) # Load in expanded view for data for map i
                                )
                    except Exception as error:
                        print(f"Error loading match data for {match}: {error}")
                        continue
                    soup = BeautifulSoup(driver.page_source, "html.parser") 
                    map1Table = soup.find("div", id="match_data1")
                    map2Table = soup.find("div", id="match_data2") 
                    time.sleep(1)
                    completedGames.append(match)
                    if i == 1: #If we are on map one, get all the player data from map one and store
                        for tr in map1Table.find_all("tr"):
                            playerName = tr.find("a",class_="playerName")
                            if playerName != None:
                                playerName = playerName.find("span").get_text()
                                # print(playerName)
                            playerStats = tr.find_all("td")
                            if playerStats != None and playerStats != []:
                                stats = []
                                for column in playerStats[0:3]:
                                    stats.append(column.get_text())
                                if playerName != None:
                                    stats.append(mapsPlayed[0])
                                    stats.append(matchDate)
                                    if playerName not in statTracker:
                                        statTracker[playerName] = [stats]
                                    else:
                                        statTracker[playerName].append(stats)

                                stats = []

                    if i == 2:
                        for tr in map2Table.find_all("tr"):
                            playerName = tr.find("a",class_="playerName")
                            if playerName != None:
                                playerName = playerName.find("span").get_text()
                                # print(playerName)
                            playerStats = tr.find_all("td")
                            if playerStats != None and playerStats != []:
                                stats = []
                                for column in playerStats[0:3]:
                                    stats.append(column.get_text())
                                if playerName != None:
                                    stats.append(mapsPlayed[1])
                                    stats.append(matchDate)
                                    if playerName not in statTracker:
                                        statTracker[playerName] = [stats]
                                    else:
                                        statTracker[playerName].append(stats)

                                stats = []
                print(statTracker)
                print(playerTeam)



for participant ,stats in statTracker.items():
    player = participant
    for teams in playerTeam:
        if player == teams:
            teamName = playerTeam[teams]
    for stat in stats:
        kills = stat[0][:stat[0].find("(")]
        headshots = stat[0][(stat[0].find("(")+1):-1]
        assists = stat[1][:stat[1].find("(")]
        deaths = stat[2]
        map = stat[3]
        date = stat[4]
        data = {
            "Player":player,
            "Kills":kills,
            "Headshots":headshots,
            "Assists":assists,
            "Deaths":deaths,
            "Map":map,
            "Date":date,
            "Team":teamName,
            "Source":"Escore"
        }
        response = supabase.table("HitRates").select("id").eq("Player", player).eq("Date", date).eq("Map", map).execute()
        if response.data:
            print(f"Skipping duplicate entry for {player} on {date} ({map})")
            continue
        
        insert = supabase.table("HitRates").insert(data).execute()
        print(f"Inserted data for {player} on {date} ({map})")

