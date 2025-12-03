import requests
from bs4 import BeautifulSoup
from __init__ import headers

url = ("https://tabiturient.ru")

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


print(findNapsInUni('rudn'))


### Здесь получаю инфу о каждом направлении
def requestForInfo(spec_id):
    global url
    url9 = url + "/ajax/ajshowmoreinfof2.php"
    data = {
        "id": spec_id,
    }
    r = requests.post(url9, headers=headers, data=data)
    soup = BeautifulSoup(r.text, "html.parser")
    blocks = soup.find_all('div', class_='p40 pm40')
    subjects = blocks[1].find_all('b', class_='font11')
    score = blocks[2].find_all('span', class_='font3')
    print(f'Список предметов егэ для поступления: {subjects[0].get_text()}, {subjects[1].get_text()}, {subjects[2].get_text()}, {subjects[3].get_text()}')
    print(f'Средний  проходной балл на бюджет - {score[1].get_text()}')
    print(f'Кол-во бюджетных мест - {score[2].get_text()}')
    print(f'Средний  балл поступивших на бюджет - {score[3].get_text()}\n')








### Здесь будет будем брать id специальности
### По какой-то причине они не совпадают с id направлений
### Далее мы просто должны сделать запрос чтобы узнать инфу с модального кона
def findSpecId(link):
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    spec_body = soup.find_all("div", class_="mobpaddcard")

    for spec in spec_body:
        spec_id = str(spec.find('span')['id'])[11::]
        requestForInfo(spec_id)



### Сюда вставляем ссылки которые получаем из findNapsInUni
findSpecId('https://tabiturient.ru/vuzu/rudn/proxodnoi?1002')





