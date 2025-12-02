import requests
from bs4 import BeautifulSoup

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


print(findNapsInUni('asu'))
