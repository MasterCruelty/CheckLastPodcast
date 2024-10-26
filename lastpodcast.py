import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import argparse

# Url of the podcast web page from LaunchPadone
url = 'https://www.launchpadone.com/PODCAST-PROFILE-URL'

# Function that check if there's a new podcast published
def check_new_podcast(url, last_date):
    response = requests.get(url)
    if response.status_code != 200:
        print("Error during download web page")
        return False
      
    # Initialize soup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the last date of podcast published, where <span> contains the date in the MM/DD/YYYY format.
    date_span = soup.find("div", class_="dateTime").find_all("span")[-1]  # the last span inside dateTime class should contain the date
    episode_date_str = date_span.text.strip()
    episode_date = datetime.strptime(episode_date_str, "%m/%d/%Y")
    
    if episode_date > last_date:
        print("È stato pubblicato un nuovo episodio!")
        return True
    else:
        print("Nessun nuovo episodio pubblicato.")
        return False

parser = argparse.ArgumentParser(description="Check if there's a new published podcast.")
parser.add_argument("last_date", type=str, help="date of last podcast in this format MM/DD/YYYY")
args = parser.parse_args()

try:
    last_known_date = datetime.strptime(args.last_date, "%m/%d/%Y")
except ValueError:
    print("Error: date must be in this format MM/DD/YYYY")
    exit(1)
 

# check for new episodes. Every 5 minutes it just checks and the program ends when a new podcast is detected.
while True:
    if check_new_podcast(url, last_known_date):
        break
    else:
        time.sleep(300)
