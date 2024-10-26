import requests
from bs4 import BeautifulSoup
from datetime import datetime

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

last_known_date = datetime(2024, 10, 23) 

# check for new episodes.
check_new_podcast(url, last_known_date)
