import requests
from bs4 import BeautifulSoup





url = "https://tabiturient.ru"

#page = requests.get(url, headers=headers)

#soup = BeautifulSoup(page.text, "html.parser")



url1 = "https://tabiturient.ru/ajax/ajcity.php"

params = {
    "method": "getSpecList",
    "region_id": "1",
    "city_id": "1149",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://tabiturient.ru/",
}

r = requests.get(url1, params=params, headers=headers)

print("STATUS:", r.status_code)
#print("TEXT:", r.text)  # показываем первые 500 символов

#data = r.json()
#print(data)

#print(soup)

##########
#########
#########


soup = BeautifulSoup(r.text, "html.parser")
links = soup.find_all("a")


links_list = []

for link in links:
    if 'href' in link.attrs:
        
        links_list.append(link['href'])

print(links_list)

