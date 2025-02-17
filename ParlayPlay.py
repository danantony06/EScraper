import requests
import cloudscraper


scraper = cloudscraper.create_scraper()
url = "https://parlayplay.io/api/v1/crossgame/search/?sport=eSports&league=CSGO&includeAlt=true&version=2&includeBoost=true"

# No payload needed for GET requests
headers = {
    'x-requested-with': 'XMLHttpRequest',
    'x-parlay-request': '1',
    'x-parlayplay-platform': 'web',
    'Cookie': 'sessionid=hac7837fqtzflespad1rv13cx6c1vj0a'  # Ensure this is a valid session
}

# Using `requests.get()` directly
response = scraper.get(url, headers=headers,allow_redirects=False)

# Print out the response text (or JSON if it is in JSON format)
print(response.text)

# Optionally, if the response is JSON, you can parse and print it as a dictionary
if response.status_code == 200:
    print(response.json())  # If the response is in JSON format
else:
    print(f"Error: {response.status_code}")
