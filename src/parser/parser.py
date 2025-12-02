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

###список городов
#for i in range(len(links_list)):
    #print(names_list[i] + ' - ' + links_list[i])


###передае в функцию список с сылками на города
def takeCity(links_list):
    cities = []
    for link in links_list:
        cities.append(str(link[28:]))
    return cities[1:]





url = ("https://tabiturient.ru")




##функция делает гет запрос с рандомными параметрами, выводит весь список
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

## мы сортируем по <a> и получаем список ссылок с вложенными элементами
n_links = sorted_naps.find_all('a')

#в первый список кладем хрефы -  которые мы мщем с помощью in
nap_link_list = []
for n_link in n_links:
    if 'href' in n_link.attrs:
        nap_link_list.append(n_link['href'])

nap_name_list = []


### делаем переменную которая находит все b
for n_link in n_links:
    f = n_link.find('b')
    f = str(f)
    nap_name_list.append(f[3:-4])

###вывод списка напрвлений

#for i in range(len(nap_link_list)):
    #print(nap_name_list[i] + ' - ' + nap_link_list[i])


### функция поиска универов
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


#print(uni)


###Парсим все универы во всех городах
def findUnisInCity(links_list):
    citiesList = takeCity(links_list)
    for city in citiesList:
        soup = BeautifulSoup(findUni(city), 'html.parser')
        print(f'Универы города - {city}')
        vuz_list = soup.find_all('table', class_='vuzlist p20')
        for vuz in vuz_list:
            short_name_tag = vuz.find('span', class_='font3').text
            long_name_tag = vuz.find('span', class_='font2').text
            if short_name_tag and long_name_tag:
                short_name = short_name_tag.strip()
                full_name = long_name_tag.strip()

                print(f"Кратко: {short_name}")
                print(f"Полное: {full_name}\n\n")
        print("-" * 30)

###вызов функции присылает все вузы по городам

#findUnisInCity(links_list)



#здесь я сделал клон функции findNap, но уже с пост запросом - старая нам еще пригодится
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
#findNapsInCity(links_list)



def findNapsInUni(vuz):
    global url
    url_4 = url + "/vuzu/"+vuz+'/about/'
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

    r = requests.get(url_4,  headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    spec_body = soup.find('div', class_='p40 pm40')
    specs = spec_body.find_all('a')
    for spec in specs:
        link = spec['href']
        code = str(spec.find('span',class_='font11'))[21:44]
        name = str(spec.find('b'))[3:-4]
        print('Ссылка - ' + link + ',  - ' + code + ' - ' + name)
        print()


print(findNapsInUni('asu'))


### пройтись по всем направлениям в вузе - рудн например
### перейдя по ссылке сделать запрос и получить модальное окно
### затем оттуда - вывести данные в findNapsInUni()