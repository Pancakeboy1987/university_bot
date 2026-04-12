import requests
import pprint
import time
from bs4 import BeautifulSoup
from __init__ import headers

# Если headers вынесены в __init__, оставь импорт.
# Иначе используй этот словарь:
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://tabiturient.ru/",
}

url = "https://tabiturient.ru"


def requestForInfo(spec_id):
    """
    Получает детальную информацию по ID специальности (AJAX запрос).
    """
    global url
    url_ajax = url + "/ajax/ajshowmoreinfof2.php"
    data = {"id": spec_id}

    try:
        r = requests.post(url_ajax, headers=headers, data=data)
        soup = BeautifulSoup(r.text, "html.parser")
        blocks = soup.find_all('div', class_='p40 pm40')

        # Если блок пустой или структура не та, возвращаем пустые данные
        if len(blocks) < 3:
            return None

        # --- 1. Сбор предметов (Динамически) ---
        subjects_elements = blocks[1].find_all('b', class_='font11')
        # Создаем множество (set) из текста всех найденных предметов
        # Это работает для любого количества предметов (1, 2, 3, 4...)
        subjects_set = {s.get_text(strip=True) for s in subjects_elements}

        # --- 2. Сбор баллов (Безопасно) ---
        score_elements = blocks[2].find_all('span', class_='font3')

        # Функция для безопасного получения текста по индексу
        def get_score_safe(index):
            if index < len(score_elements):
                return score_elements[index].get_text(strip=True)
            return "Нет данных"

        # Обычно индексы такие:
        # [0] - мин. балл (иногда отсутствует)
        # [1] - проходной балл
        # [2] - бюджетные места
        # [3] - средний балл
        # Но лучше проверить:

        val_mid_entry = get_score_safe(1)
        val_budget_places = get_score_safe(2)
        val_mid_score = get_score_safe(3)

        # Вывод для отладки
        # print(f'Предметы: {subjects_set}')
        # print(f'Проходной: {val_mid_entry}, Места: {val_budget_places}')

        program_n = {
            "mid_entry_score": {val_mid_entry},
            "budget_places": {val_budget_places},
            "subjects": subjects_set,
            "mid_score": {val_mid_score}
        }
        return program_n

    except Exception as e:
        print(f"Ошибка при запросе info id {spec_id}: {e}")
        return None


def findSpecId(link):
    """
    Переходит по ссылке направления, находит все вариации (профили)
    и собирает по ним детальную статистику.
    """
    full_link = link if link.startswith("http") else url + link

    try:
        r = requests.get(full_link, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        # Находим карточки вариантов поступления
        spec_body = soup.find_all("div", class_="mobpaddcard")
        program_variants = []

        for spec in spec_body:
            # Ищем ID специальности
            span_id = spec.find('span')
            if span_id and span_id.has_attr('id'):
                # id выглядит как 'vuzopisanie12345', берем с 11 символа
                spec_id = str(span_id['id'])[11:]

                # Запрашиваем детали
                details = requestForInfo(spec_id)
                if details:
                    program_variants.append(details)
                    # Небольшая задержка, чтобы не забанили IP при массовом парсинге
                    time.sleep(0.2)

        return program_variants

    except Exception as e:
        print(f"Ошибка при переходе по ссылке {full_link}: {e}")
        return []


def parse_whole_university(vuz_slug):
    """
    Главная функция:
    1. Находит все направления вуза.
    2. Проходит по каждому направлению и собирает детали.
    """
    url_about = url + "/vuzu/" + vuz_slug + '/about/'

    print(f"Начинаем сбор данных для: {vuz_slug}...")

    r = requests.get(url_about, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    spec_body = soup.find('div', class_='p40 pm40')
    if not spec_body:
        print("Не найден список специальностей")
        return {}

    specs_links = spec_body.find_all('a')

    university_data = {}

    for spec in specs_links:
        link = spec['href']

        # Более надежный способ получить код и название
        # .get_text(strip=True) уберет лишние пробелы и \n
        code_tag = spec.find('span', class_='font11')
        name_tag = spec.find('b')

        if code_tag and name_tag:
            code = code_tag.get_text(strip=True)
            name = name_tag.get_text(strip=True)

            # Формируем ключ словаря
            full_name = f"{code} - {name}"
            print(f"Обработка: {full_name}")

            # Получаем список вариантов (профилей) для этого направления
            variants = findSpecId(link)

            university_data[full_name] = variants
        else:
            print("Не удалось распарсить название направления, пропускаем.")

    return university_data


# --- ЗАПУСК ---

# Запускаем полный цикл по вузу (например, rudn)
final_data = parse_whole_university('altsu')

print("\n--- ИТОГОВЫЙ РЕЗУЛЬТАТ ---")
pprint.pprint(final_data)