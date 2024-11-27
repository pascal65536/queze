import json
import pandas as pd

"""
Плоский файл в excel
"""


# Функция для преобразования JSON в Excel
def json_to_excel(json_file, excel_file):
    # Чтение JSON файла
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Создание объекта ExcelWriter
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        # Получаем название теста
        test_title = data["test"]["title"]

        # Создаем DataFrame из вопросов и ответов
        questions = data["test"]["questions"]
        df = pd.DataFrame(questions)

        # Переименовываем столбцы
        df.rename(columns={"question": "Вопрос", "answer": "Ответ"}, inplace=True)

        # Записываем DataFrame на отдельный лист в Excel
        df.to_excel(writer, sheet_name=test_title[:31], index=False)


# Пример использования функции
json_file = "queze/2.json"  # Укажите путь к вашему JSON файлу
excel_file = "queze/2.xlsx"  # Укажите имя выходного Excel файла
json_to_excel(json_file, excel_file)
