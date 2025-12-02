import requests
from bs4 import BeautifulSoup

url = ("https://tabiturient.ru")

def allCitiesList():
    global url
    url1 = url +'/ajax/ajcity.php'

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

    for link in links:
        if 'href' in link.attrs:
            links_list.append(link['href'])

    return links_list




###передае в функцию список с сылками на города
def takeCity(links_list = allCitiesList()):
    cities = []
    for link in links_list:
        cities.append(str(link[28:]))
    return cities[1:]




def findNapFixed(city):
    global url
    url_4 = url + "/ajax/ajnap.php"

    data = {
        'page1': 'city',
        'page2': city,
        'page3':''
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://tabiturient.ru/",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = requests.post(url_4, data=data, headers=headers)
    return response.text



def findNapsInCity(links_list):
    citiesList = takeCity(links_list)
    for city in citiesList:
        print(city)
        soup = BeautifulSoup(findNapFixed(city), 'html.parser')
        print(f'Направления города - {city}')
        nap_list = soup.find_all('table', class_='specsh')
        for nap in nap_list:
            if nap.find('span', class_='font1')==None:
                code_tag = nap.find_all('span', class_='font2')[0].text
                name_tag = nap.find_all('span', class_='font2')[1].text
                if name_tag and code_tag:
                    code_name = code_tag.strip()
                    full_name = name_tag.strip()

                    print(f"код специальности: {code_name}")
                    print(f"Полное название направления: {full_name}\n\n")
        print("-" * 30)

###вывод всех направлений по городам
if __name__ == '__main__':
   findNapsInCity(links_list=allCitiesList())