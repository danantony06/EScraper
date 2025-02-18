import requests
import json

url = "https://api.hotstreak.gg/graphql"

payload = json.dumps({
  "operationName": "search",
  "query": "query search($query: String, $page: Int, $gameFilter: [String!], $sportFilter: [String!], $teamFilter: [String!], $positionFilter: [String!], $categoryFilter: [String!], $promotedFilter: Boolean, $participantFilter: [String!], $leagueFilter: [String!]) { search(query: $query, page: $page, gameFilter: $gameFilter, sportFilter: $sportFilter, teamFilter: $teamFilter, positionFilter: $positionFilter, categoryFilter: $categoryFilter, promotedFilter: $promotedFilter, participantFilter: $participantFilter, leagueFilter: $leagueFilter) {\n        __typename\ngeneratedAt\ncategoryFilters {\n\n__typename\ncount\ngeneratedAt\nkey\nmeta\nname\n\n}\ngameFilters {\n\n__typename\ncount\ngeneratedAt\nkey\nmeta\nname\n\n}\ngames {\n\n__typename\nid\n... on EsportGame {\n\n__typename\nid\nminimumNumberOfGames\nvideogameTitle\n\n}\n... on GolfGame {\n\n__typename\nid\npairings {\n\n__typename\nid\nbackNine\ncreatedAt\ngameId\ngeneratedAt\nparticipantIds\nteeTime\nupdatedAt\n\n}\ntournament {\n\n__typename\nid\nname\n\n}\n\n}\nleagueId\nopponents {\n\n__typename\nid\ndesignation\ngameId\nteam {\n\n__typename\nid\ncolors {\n\n__typename\nprimary\nsecondary\n\n}\ncreatedAt\ngeneratedAt\nlogoUrl\nmarket\nname\nshortName\nupdatedAt\n\n}\n\n}\nperiod\nreplay\nscheduledAt\nstatus\n\n}\nleagueFilters {\n\n__typename\ncount\ngeneratedAt\nkey\nmeta\nname\n\n}\nmarkets {\n\n__typename\nid\ngeneratedAt\nlines\noptions\nprobabilities\n\n}\nparticipants {\n\n__typename\nid\ncategories\nopponentId\nplayer {\n\n__typename\nid\ndisplayName\nexternalId\nfirstName\nheadshotUrl\ninjuries {\n\n__typename\nid\ncomment\ncreatedAt\ndescription\ngeneratedAt\nstatus\nstatusDate\nupdatedAt\n\n}\nlastName\nnickname\nnumber\nposition\nshortDisplayName\ntraits\n\n}\nposition\n\n}\npositionFilters {\n\n__typename\ncount\ngeneratedAt\nkey\nmeta\nname\n\n}\nsportFilters {\n\n__typename\ncount\ngeneratedAt\nkey\nmeta\nname\n\n}\nteamFilters {\n\n__typename\ncount\ngeneratedAt\nkey\nmeta\nname\n\n}\nstats\ntotalCount\n\n      } }",
  "variables": {
    "query": "*",
    "page": 4,
    "sportFilter": [
      "Sport:A0mfMN"
    ]
  }
})
headers = {
  'content-type': 'application/json',
  'origin': 'https://app.hotstreak.gg',
  'referer': 'https://app.hotstreak.gg/',
  'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
  'sec-ch-ua-platform': '"Windows"',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
  'x-requested-with': 'web',
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJIb3RTdHJlYWsgKHByb2R1Y3Rpb24pIiwic3ViIjoiSHNmOjpVc2VyOkpwdG12NEciLCJleHAiOjE3NDIyNzMyNTEsImlhdCI6MTczOTg1NDA1MX0.ykuHAwYlvrvqQCOrCFCTRBnqwjgw_c91AMtxDOs5ZGE'
}

response = requests.request("POST", url, headers=headers, data=payload)
print(response.status_code)
print(response.text)
data = response.json()
print(json.dumps(data, indent=2))

