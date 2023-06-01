# Get a menu list on the main page classroom.its.ac.id by parsing the HTML

import requests
from bs4 import BeautifulSoup

url = 'https://classroom.its.ac.id'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

azsdfgbn = soup.find('nav', attrs={'aria-label': 'Custom menu'})


print(azsdfgbn.get_text())

