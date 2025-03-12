from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pdb
import itertools

# Set up Selenium WebDriver (Make sure you have ChromeDriver installed)
driver = webdriver.Chrome()  



ogUrl = 'https://escorenews.com/en/csgo/team'  #OG Website to get top Ranked Teams
driver.get(ogUrl)

teamNames = []  # List of Team names for all top rated teams
completedGames =[] #Expanding list of completed games to make sure matches arent double counted
playerTeam = {} # Dictionary assigning players to their teams
statTracker = {}

time.sleep(3)
for i in range(5):
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
                matchDate = soup.find("span",class_ = "sct").get_text()
                maps = soup.find_all("strong",class_="map")  #Find the different maps played in the match 
                if len(maps) >= 2:
                    mapsPlayed = [maps[0].get_text(),maps[1].get_text()] # Store the maps in a mapsPlayed Variable
                    for i in [1, 2]:
                        url = f'https://escorenews.com{match}#{i}' #Use ranged for loop to expand the tables for player data for maps 1 and 2
                        driver.get(url)
                        driver.refresh()
                        time.sleep(1)
                        WebDriverWait(driver, 8).until(
                            EC.presence_of_element_located((By.ID, "match_data1")) # Load in expanded view for data for map i
                        )
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


#                 # collapsibleData = driver.find_element(By.CLASS_NAME, 'opener collapsed')
#                 # collapsibleData.click()
#                 # time.sleep(2)
#                 # collapsibleData = driver.find_element(By.CSS_SELECTOR, '.opener.collapsed')
#                 # collapsibleData.click()
#                 # time.sleep(4)

                
#                 # collapsibleData = WebDriverWait(driver, 10).until(
#                 #     EC.visibility_of_element_located((By.CLASS_NAME, 'opener.collapsed'))
#                 #     )
#                 map1Table = soup.find("article",rel= "1")
#                 # print(map1Table)
#                 map1StatTable = map1Table.find("table",class_ = "table table-striped table-sm table-hover")
#             #     # map1StatTable.find()









        


#     #     spoilerButton = driver.find_element(By.XPATH,"//button[contains(text(), )]")
# #     spoilerButton.click()
# # time.sleep(2)
# # for i in range(5):  # Adjust the range to scroll more times
# #     driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
# #     time.sleep(5)  

# # validTeams = []
# # players = [div.get_text() for div in soup.find_all('div', class_="table-row")]

# # fraggers = []
# # fragTeams = {}
# # playerStats = {}
# # nicknames = []
# # for rowDiv in soup.find_all('div', class_="table-row"):
# #     if len(rowDiv.find_all('p',class_="default")) >= 2 and rowDiv.find_all('p',class_="default") != None:
# #         for fragger in rowDiv.find_all('p',class_="default"):
# #             player = fragger.get_text()
# #             if rowDiv.find('div',class_="table-cell team") != None:
# #                 validTeam = rowDiv.find('span',class_="team-name")
# #                 team_name = validTeam.find(text=True, recursive=False)
# #                 if team_name not in fragTeams:
# #                     fragTeams[team_name] = [player]
# #                 else:
# #                     fragTeams[team_name].append(player)

# # for team in itertools.islice(fragTeams,2):
# #     if " " not in team:
# #         matchesUrl = f"https://bo3.gg/teams/{team}/matches"
# #     else:
# #          dash = team.split(" ")
# #          dashedTeam = "-".join(dash)
# #          matchesUrl = f"https://bo3.gg/teams/{dashedTeam}/matches"
# #     driver.get(matchesUrl)
# #     time.sleep(3)
# #     soup = BeautifulSoup(driver.page_source, 'html.parser')
# #     bb = soup.find_all('a',class_ = "c-global-match-link table-cell")
# #     for anchor in [bb[0],bb[1]]:
# #         href = anchor.get("href")
# #         hrefUrl = f"https://bo3.gg/{href}"
# #         driver.get(hrefUrl)
# #         time.sleep(5)
# #         soup = BeautifulSoup(driver.page_source, 'html.parser')
# #         maps = soup.find_all("div", class_ = "c-nav-match-menu-item c-nav-match-menu-item--game c-nav-match-menu-item--finished")
# #         for map in maps:
# #             mapLink = map.find("a",class_ = "menu-link").get("href")
# #             mapUrl = f"https://bo3.gg{mapLink}"
# #             driver.get(mapUrl)
# #             time.sleep(3)
# #             soup = BeautifulSoup(driver.page_source,'html.parser')
# #             participants = soup.find_all('div', class_ = 'table-row')
# #             for participant in participants:
# #                 participantDiv = participant.find('div',class_ = "c-avatar-with-nickname")
# #                 if participantDiv != None:
# #                     nickname = participantDiv.find("span",class_="nickname")
# #                     if nickname != None:
# #                         nickname = nickname.get_text()
# #                         nicknames.append(nickname)
# #                         kills = participant.find("div",class_ = "table-cell kills").get_text()
# #                         deaths = participant.find("div",class_ = "table-cell deaths").get_text()
# #                         assists = participant.find("div",class_ = "table-cell assists").get_text()
# #                         form = participant.find("div",class_ = "table-cell form").find("p").get_text()
# #                         scoreMetric = participant.find("div",class_ = "c-table-cell-score table-cell score").find("span").get_text()
# #                         matchupKey = f"PLAYER={nickname}-->{mapLink.split("/")[2]}({mapLink.split("/")[3]})"
# #                         playerStats[matchupKey] = [f"kills:{kills}/deaths:{deaths}/assists:{assists}",f"6 month Comp:{form}",f"CarryScore:{scoreMetric}"]

