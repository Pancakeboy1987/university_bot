import requests
import pprint
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
    rudn = {}
    for spec in specs:
        link = spec['href']
        code = str(spec.find('span',class_='font11'))[21:44]
        name = str(spec.find('b'))[3:-4]
        print('Ссылка - ' + link + ',  - ' + code + ' - ' + name)
        print()
        rudn[code[1::] + ' - ' + name] = []
    pprint.pprint(rudn)


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
    sub_len = (len(subjects))
    score = blocks[2].find_all('span', class_='font3')
    score_len = (len(score))
    print(f'Список предметов егэ для поступления: {[subjects[i].get_text() for i in range(sub_len)]}')
    print(f'Средний  проходной балл на бюджет - {score[1].get_text()}')
    print(f'Кол-во бюджетных мест - {score[2].get_text()}')
    print(f'Средний  балл поступивших на бюджет - {score[3].get_text()}\n')
    program_n = {
        "mid_entry_score": {score[1].get_text()},
        "budget_places": {score[2].get_text()},
        "subjects": {subjects[0].get_text(), subjects[1].get_text(), subjects[2].get_text(),subjects[3].get_text()},
        "mid_score": {score[3].get_text()}
    }
    return program_n








### Здесь будет будем брать id специальности
### По какой-то причине они не совпадают с id направлений
### Далее мы просто должны сделать запрос чтобы узнать инфу с модального кона
def findSpecId(link):
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    spec_body = soup.find_all("div", class_="mobpaddcard")
    program = []

    for spec in spec_body:
        spec_id = str(spec.find('span')['id'])[11::]
        spec_num = str(spec)
        spec_num = requestForInfo(spec_id)
        program.append(spec_num)
    pprint.pprint(program, indent=4, width=40)


### Сюда вставляем ссылки которые получаем из findNapsInUni
findSpecId('https://tabiturient.ru/vuzu/rudn/proxodnoi?1019')



