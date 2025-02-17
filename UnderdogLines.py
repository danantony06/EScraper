import requests
from bs4 import BeautifulSoup

UnderdogLines = 'https://api.underdogfantasy.com/v2/pickem_search/search_results?sport_id=CS' #UD API for CS lines

Underdog = requests.get(UnderdogLines)
Underdog_CS2_Lines = {} #Initialize Final Dictionary for storing player lines

if Underdog.status_code == 200:
    EsportsProps = Underdog.json() #parse JSON Data
    for prop in EsportsProps['over_under_lines']: #Loop through all over under lines
        seperator = prop['over_under']['title'].find(" ") 
        name = prop['over_under']['title'][0:seperator] #Seperate name from string
        stat_type = prop['over_under']['title'][seperator+1:] #Seperate stat type from string
        line = prop['stat_value'] #Get the line value
        if name not in Underdog_CS2_Lines: #Either insert or append into dictionary based on player name
            Underdog_CS2_Lines[name] = [[stat_type,line]]
        else:
            Underdog_CS2_Lines[name].append([stat_type,line])
        
    print(Underdog_CS2_Lines)




