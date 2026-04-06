from sqlalchemy.orm import Session

from models import SessionLocal, City, University, Program, base_engine, Base

from textData import universities_registry


def clean_set_value(value_set):

    if not value_set or not isinstance(value_set, set):
        return "Нет данных"


    val = list(value_set)[0]


    clean_str = str(val).strip().replace('\n', ' ').replace('  ', ' ')

    if not clean_str:
        return "Нет данных"

    return clean_str


def clean_subjects(subjects_set):
    if isinstance(subjects_set, set) and subjects_set:
        # Сортируем по алфавиту для красоты и соединяем
        return ", ".join(sorted(list(subjects_set)))
    return "Нет данных"


def get_or_create_city(session: Session, city_name: str):

    city = session.query(City).filter_by(full_name=city_name).first()
    if not city:
        city = City(full_name=city_name)
        session.add(city)
        session.commit()  # Сохраняем, чтобы получить id
    return city


def load_data():
    session = SessionLocal()

    # Создаем таблицы в БД, если их еще нет
    Base.metadata.create_all(base_engine)

    print(f"Найдено вузов для загрузки: {len(universities_registry)}")
    total_programs = 0

    try:
        # 1. Проходимся по каждому вузу в реестре
        for uni_data in universities_registry:
            city_name = uni_data["city"]
            uni_name = uni_data["name"]
            uni_slug = uni_data["slug"]
            data_dict = uni_data["data"]  # Это словари типа rudn_data, mgu_data и тд

            print(f"\nОбработка: {uni_name} ({city_name})")

            # Если словарь с направлениями пустой (как mgu_data = {}), просто пропускаем
            if not data_dict:
                print(" -> Нет данных по направлениям, пропускаем.")
                continue

            # 2. Получаем или создаем Город
            city_obj = get_or_create_city(session, city_name)

            # 3. Получаем или создаем ВУЗ
            uni_obj = session.query(University).filter_by(slug=uni_slug).first()
            if not uni_obj:
                uni_obj = University(
                    name=uni_name,
                    slug=uni_slug,
                    city_id=city_obj.id
                )
                session.add(uni_obj)
                session.commit()  # Сохраняем, чтобы получить id

            # 4. Загружаем направления (программы)
            programs_added = 0

            # full_name - это строка типа '01.03.01 | Бакалавриат - Математика'
            # variants - это список с вариантами (бюджет, платка и тд)
            for full_name, variants in data_dict.items():

                # Если список вариантов пустой (например, []), пропускаем
                if not variants:
                    continue

                # Проходимся по каждому варианту в списке (очка, платка и тд)
                for variant in variants:
                    # Извлекаем и чистим данные
                    score_str = clean_set_value(variant.get('mid_entry_score'))
                    places_str = clean_set_value(variant.get('budget_places'))
                    subjects_str = clean_subjects(variant.get('subjects'))

                    # Создаем запись в таблице programs
                    new_program = Program(
                        name=full_name,  # Сохраняем целиком с кодом
                        min_score=score_str,  # Например: "217" или "Только платное"
                        budget_places=places_str,  # Например: "40" или "Нет данных"
                        subjects=subjects_str,  # Например: "Математика, Русский язык, Физика"

                        university_id=uni_obj.id,
                        city_id=city_obj.id
                    )

                    session.add(new_program)
                    programs_added += 1

            # Сохраняем все программы этого вуза разом
            session.commit()
            total_programs += programs_added
            print(f" -> Успешно загружено {programs_added} вариантов программ.")

        print("\n==========================================")
        print("ЗАГРУЗКА УСПЕШНО ЗАВЕРШЕНА!")
        print(f"Всего загружено направлений/профилей: {total_programs}")

    except Exception as e:
        # Если что-то пошло не так, откатываем изменения, чтобы не было "битой" базы
        session.rollback()
        print(f"\n!!! ПРОИЗОШЛА ОШИБКА !!!\n{e}")
    finally:
        session.close()


if __name__ == "__main__":
    load_data()