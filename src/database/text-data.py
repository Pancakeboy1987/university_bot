program_entry = {
    "code": code,  # 01.03.02 (Общий для всех форм)
    "name": name,  # Прикладная математика (Общее название)
    "tabiturient_link": full_link,

    # Внутри forms храним словари для каждой формы обучения
    "forms": {
        "ochka": {
            "min_score": 260,
            "budget_places": 45,
            "subjects": "Математика, Русский, Информатика"
        },
        "zaochka": {
            "min_score": 180,  # На заочке баллы обычно ниже
            "budget_places": 10,
            "subjects": "Математика, Русский, Информатика"
        }
        # Если заочки нет, здесь будет пусто или None
    }
}

