import requests
from bs4 import BeautifulSoup
from naps import allCitiesList, takeCity
#ебаный пайтон

url = ("https://tabiturient.ru")


def findUni(city):
    global url
    url_5 = url + "/ajax/ajvuz1.php"

    data = {
        'page1': 'city',
        'page2': city,
        'vuz': '',
        'limit': '10000',
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://tabiturient.ru/",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = requests.post(url_5, data=data, headers=headers)
    return response.text

### Здесь реализован запрос по id вуза, чтобы узнать его англ.название

def findLink(id):
    global url
    url_6 = url + "/ajax/ajshowmoreinfof4.php"

    data = {
        'id': id,
        'specid': ''
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://tabiturient.ru/",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = requests.post(url_6, data=data, headers=headers)
    soap = BeautifulSoup(response.text, 'html.parser')
    links = soap.find_all('a')
    eng = str(links[0]['href'])[28:-6]
    return eng



###Парсим все универы во всех городах
def findUnisInCity(links_list):
    citiesList = takeCity(links_list)
    for city in citiesList:
        soup = BeautifulSoup(findUni(city), 'html.parser')
        print(f'Универы города - {city}')
        vuz_list = soup.find_all('div', class_='mobpadd20')
        for vuz in vuz_list:
            idVuz = str(vuz['id'])[3:]
            eng_name = str(findLink(idVuz))
            short_name_tag = vuz.find('span', class_='font3').text
            long_name_tag = vuz.find('span', class_='font2').text
            if short_name_tag and long_name_tag:
                short_name = short_name_tag.strip()
                full_name = long_name_tag.strip()

                print(f"Кратко: {short_name}")
                print(f"Полное: {full_name}")
                print(f"Название для ссылки - {eng_name}")
                print(f"ID = {idVuz}\n\n")

        print("-" * 30)

###вызов функции присылает все вузы по городам

findUnisInCity(links_list=allCitiesList())