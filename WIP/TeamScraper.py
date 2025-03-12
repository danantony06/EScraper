

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import itertools

# Set up Selenium WebDriver (Make sure you have ChromeDriver installed)
driver = webdriver.Chrome()  



url = 'https://bo3.gg/teams/earnings'
driver.get(url)


time.sleep(5)

spoilerButton = driver.find_element(By.XPATH,"//button[contains(text(), 'Ok')]")
spoilerButton.click()
time.sleep(2)
for i in range(5):  # Adjust the range to scroll more times
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(5)  


soup = BeautifulSoup(driver.page_source, "html.parser")

validTeams = []
players = [div.get_text() for div in soup.find_all('div', class_="table-row")]

fraggers = []
fragTeams = {}
playerStats = {}
nicknames = []
for rowDiv in soup.find_all('div', class_="table-row"):
    if len(rowDiv.find_all('p',class_="default")) >= 2 and rowDiv.find_all('p',class_="default") != None:
        for fragger in rowDiv.find_all('p',class_="default"):
            player = fragger.get_text()
            if rowDiv.find('div',class_="table-cell team") != None:
                validTeam = rowDiv.find('span',class_="team-name")
                team_name = validTeam.find(text=True, recursive=False)
                if team_name not in fragTeams:
                    fragTeams[team_name] = [player]
                else:
                    fragTeams[team_name].append(player)

for team in itertools.islice(fragTeams,2):
    if " " not in team:
        matchesUrl = f"https://bo3.gg/teams/{team}/matches"
    else:
         dash = team.split(" ")
         dashedTeam = "-".join(dash)
         matchesUrl = f"https://bo3.gg/teams/{dashedTeam}/matches"
    driver.get(matchesUrl)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    bb = soup.find_all('a',class_ = "c-global-match-link table-cell")
    for anchor in [bb[0],bb[1]]:
        href = anchor.get("href")
        hrefUrl = f"https://bo3.gg/{href}"
        driver.get(hrefUrl)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        maps = soup.find_all("div", class_ = "c-nav-match-menu-item c-nav-match-menu-item--game c-nav-match-menu-item--finished")
        for map in maps:
            mapLink = map.find("a",class_ = "menu-link").get("href")
            mapUrl = f"https://bo3.gg{mapLink}"
            driver.get(mapUrl)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source,'html.parser')
            participants = soup.find_all('div', class_ = 'table-row')
            for participant in participants:
                participantDiv = participant.find('div',class_ = "c-avatar-with-nickname")
                if participantDiv != None:
                    nickname = participantDiv.find("span",class_="nickname")
                    if nickname != None:
                        nickname = nickname.get_text()
                        nicknames.append(nickname)
                        kills = participant.find("div",class_ = "table-cell kills").get_text()
                        deaths = participant.find("div",class_ = "table-cell deaths").get_text()
                        assists = participant.find("div",class_ = "table-cell assists").get_text()
                        form = participant.find("div",class_ = "table-cell form").find("p").get_text()
                        scoreMetric = participant.find("div",class_ = "c-table-cell-score table-cell score").find("span").get_text()
                        matchupKey = f"PLAYER={nickname}-->{mapLink.split("/")[2]}({mapLink.split("/")[3]})"
                        playerStats[matchupKey] = [f"kills:{kills}/deaths:{deaths}/assists:{assists}",f"6 month Comp:{form}",f"CarryScore:{scoreMetric}"]


hitRates = {}
for key,value in playerStats.items():
    for nickname in nicknames:
        if nickname in key:
            if nickname not in hitRates:
                 hitRates[nickname] = [f"{key}:{value}"]
            else:
                # Check if the value is already in the list for this nickname
                if value not in [v.split(":")[1] for v in hitRates[nickname]]:
                    hitRates[nickname].append(f"{key}:{value}")
print(hitRates)

                            
                        # print(nicknames)
                        

                        #     if nickname in playerKey:

                        #         hitRates[nickname] = playerStats[playerKey]
                        #     print(hitRates)
            # print(playerStats)
                
                        

            # print(mapLink)
        # print(maps)
        # participants = soup.find_all('div', class_ = 'table-row')
        # for participant in participants:
        #     participantDiv = participant.find('div',class_ = "c-avatar-with-nickname")
        #     if participantDiv != None:
        #         nickname = participantDiv.find("span",class_="nickname")
        #         if nickname != None and nickname.get_text() == player:
        #             kills = participant.find("div",class_ = "table-cell kills").get_text()
        #             print(f"{nickname}:{kills}")




# for teamName in fragTeams:
#     if " " in teamName:
#         dash = teamName.split(" ")
#         input = "-".join(dash)
#         matchesLinks.append(input)
#     else:
#         matchesLinks.append(teamName)

# print(matchesLinks)



            


                
# gameData = {}

# for player in players:
#     playerUrl = f"https://bo3.gg/players/{player}/matches"
#     driver.get(playerUrl)
#     time.sleep(8)  
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     bb = soup.find_all('a',class_ = "c-global-match-link table-cell")
#     for anchor in bb:
#         href = anchor.get("href")
#         hrefUrl = f"https://bo3.gg/{href}"
#         driver.get(hrefUrl)
#         time.sleep(8)
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         maps = soup.find("div", class_ = "c-nav-match-menu-item c-nav-match-menu-item--game c-nav-match-menu-item--finished")
#         if maps != None:
#             matchups = maps.find("a", class_ = "menu-link").get("href")
#             matchups = matchups.split("/")[2]
#             mapsCompleted = maps.find_all("a",class_ ="menu-link")
#             if len(mapsCompleted) >= 2:
#                 map1 = mapsCompleted[0].get("href")
#                 map2 = mapsCompleted[1].get("href")
#                 gameData[matchups] = [map1,map2]
#                 print(gameData)

        

#         # print(matches)
#         # participants = soup.find_all('div', class_ = 'table-row')
#         # for participant in participants:
#         #     participantDiv = participant.find('div',class_ = "c-avatar-with-nickname")
#         #     if participantDiv != None:
#         #         nickname = participantDiv.find("span",class_="nickname")
#         #         if nickname != None and nickname.get_text() == player:
#         #             kills = participant.find("div",class_ = "table-cell kills").get_text()
#         #             print(kills)


#             # print(participantDiv)




#     #links = driver.find_elements(By.CLASS_NAME, "c-global-match-link") 
#     ##print(f" bb {bb}")
#     #print(f"links{links}")
    # time.sleep(4)


driver.quit()


# print(players)
# print(bb)
# from bs4 import BeautifulSoup
# from concurrent.futures import ThreadPoolExecutor
# import requests
# import json

# url = 'https://bo3.gg/players?period=last_6_months&tiers=s,a,b&tab=main&sort=rating&order=desc'

# players = []

# statsPage = requests.get(url)
# soup = BeautifulSoup(statsPage.text, features="html.parser")
# gb = soup.prettify()
# json_data = json.dumps({"gb": gb})
# soupDivs = soup.find_all('span', class_ = "nickname")

# for div in soupDivs:
#     gg = div.find("nickname")
#     print(gg)
