import requests
from bs4 import BeautifulSoup


url = "https://tabiturient.ru"

page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

print(soup)


city = "moscow"
discipline = '1262'
url2 = url + '/' + 'city' + '/' + city +'/' + discipline +'/'


page2 = requests.get(url2)

soup2 = BeautifulSoup(page2.text, "html.parser")