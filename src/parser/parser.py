import requests
from bs4 import BeautifulSoup

url1 = "https://tabiturient.ru/ajax/ajcity.php"

params = {
    "method": "getSpecList",
    "region_id": "2",
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

soup = BeautifulSoup(r.text, "html.parser")
links = soup.find_all("a")

links_list = []
names_list = []

for link in links:
    if 'href' in link.attrs:
        links_list.append(link['href'])

for link in links:
    city = link.find('span')
    city = str(city)
    names_list.append(city[23:-11])

for i in range(len(links_list)):
    print(names_list[i] + ' - ' + links_list[i])

url = ("https://tabiturient.ru")


def findNap():
    global url
    url_4 = url + "/ajax/ajnap.php"

    params = {
        "method": "getSpecList",
        "region_id": "2",
        "city_id": "1149",
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://tabiturient.ru/",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = requests.get(url_4, params=params, headers=headers)
    return response.text


naps = findNap()

sorted_naps = BeautifulSoup(naps, 'html.parser')

n_links = sorted_naps.find_all('a')

nap_link_list = []
for n_link in n_links:
    if 'href' in n_link.attrs:
        nap_link_list.append(n_link['href'])

nap_name_list = []

for n_link in n_links:
    f = n_link.find('b')
    f = str(f)
    nap_name_list.append(f[3:-4])

for i in range(len(nap_link_list)):
    print(nap_name_list[i] + ' - ' + nap_link_list[i])