

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time

# Set up Selenium WebDriver (Make sure you have ChromeDriver installed)
driver = webdriver.Chrome()  



url = 'https://bo3.gg/players?period=last_6_months&tiers=s,a,b&tab=main&sort=rating&order=desc'
driver.get(url)


time.sleep(5)

spoilerButton = driver.find_element(By.XPATH,"//button[contains(text(), 'Ok')]")
spoilerButton.click()
time.sleep(2)
for i in range(5):  # Adjust the range to scroll more times
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(5)  


soup = BeautifulSoup(driver.page_source, "html.parser")

players = [div.get_text() for div in soup.find_all('span', class_="nickname")]

gameData = {}

for player in players:
    playerUrl = f"https://bo3.gg/players/{player}/matches"
    driver.get(playerUrl)
    time.sleep(8)  
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    bb = soup.find_all('a',class_ = "c-global-match-link table-cell")
    for anchor in bb:
        href = anchor.get("href")
        print(href)
        hrefUrl = f"https://bo3.gg/{href}"
        driver.get(hrefUrl)
        time.sleep(8)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        maps = soup.find("div", class_ = "c-nav-match-menu-item c-nav-match-menu-item--game c-nav-match-menu-item--finished")
        if maps != None:
            matchups = maps.find("a", class_ = "menu-link").get("href")
            matchups = matchups.split("/")[2]
            mapsCompleted = maps.find_all("a",class_ ="menu-link")
            if len(mapsCompleted) >= 2:
                map1 = mapsCompleted[0].get("href")
                map2 = mapsCompleted[1].get("href")
                gameData[matchups] = [map1,map2]
                # print(gameData)

        

        # print(matches)
        # participants = soup.find_all('div', class_ = 'table-row')
        # for participant in participants:
        #     participantDiv = participant.find('div',class_ = "c-avatar-with-nickname")
        #     if participantDiv != None:
        #         nickname = participantDiv.find("span",class_="nickname")
        #         if nickname != None and nickname.get_text() == player:
        #             kills = participant.find("div",class_ = "table-cell kills").get_text()
        #             print(kills)


            # print(participantDiv)




    #links = driver.find_elements(By.CLASS_NAME, "c-global-match-link") 
    ##print(f" bb {bb}")
    #print(f"links{links}")
    time.sleep(4)


driver.quit()


print(players)
print(bb)
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
