from datetime import *
from unittest.mock import sentinel
import pandas as pd
import math  # Импортируем math для проверки NaN


def sort_students(data, sort_param, sort_method):
    records = []
    for class_name, students in data.items():
        for student_name, tests in students.items():
            for test in tests:
                records.append({
                    'Класс': class_name,
                    'Имя': student_name,
                    **test
                })
    df = pd.DataFrame(records)
    
    if sort_method == "sort-date":
        sort_method = "Дата"
    elif sort_method == "sort-percent":
        sort_method = "Правильные ответы"
    elif sort_method == "sort-fio":
        sort_method = "Имя"
    
    sorted_df = df.sort_values(by=sort_method, ascending=sort_param)
    
    result_dict = {}
    for index, row in sorted_df.iterrows():
        class_name = row['Класс']
        student_name = row['Имя']
        
        test_data = {}
        for key, value in row.drop(['Класс', 'Имя']).items():
            if not isinstance(value, float) or not math.isnan(value):  # Проверка на NaN
                test_data[key] = value
        
        if class_name not in result_dict:
            result_dict[class_name] = {}
        if student_name not in result_dict[class_name]:
            result_dict[class_name][student_name] = []
        result_dict[class_name][student_name].append(test_data)
            
    return result_dict

#Функция для получения списка данных для вывода(только для администратора)
def get_admin_send_data(data, sort_method=None, school_class=None, sort_param=None):
    send_data = {}
    for key, tests_data in data.items():
        student_name = key.split("_")[0]
        student_class = key.split("_")[-1]

        if student_class not in send_data:
            send_data[student_class] = {}
        if student_name not in send_data[student_class]:
            send_data[student_class][student_name] = []
            
        test_id = 0
        for test_name, tests in tests_data.items():
            for test in tests:
                test.update({"Вид теста": test_name, "id": test_id})
                test_id += 1
                send_data[student_class][student_name].append(test)

    # Преобразуем строку в boolean значение
    sort_param = sort_param == "sort-ahead" if sort_param else None
    # Возвращаем данные без фильтрации и сортировки, если параметры не заданы
    if sort_method is None and school_class is None:
        return send_data
    
    # Фильтрация по классу, если он задан
    if school_class:
      send_data = {sc_class: students for sc_class, students in send_data.items() if sc_class == school_class}

     # Сортировка, если задан метод сортировки и если данные не пустые
    if sort_method and send_data:
      send_data = sort_students(send_data, not(sort_param) , sort_method)
      
    return send_data

#Функции для получения списка данных для вывода(конкретных классов)
def get_send_data(link_class, data, sort_method=None, school_class=None, sort_param=None):
    send_data = {}
    for key, tests_data in data.items():
        student_name = key.split("_")[0]
        student_class = key.split("_")[-1]

        if student_class in link_class:
            if student_class not in send_data:
                send_data[student_class] = {}
            if student_name not in send_data[student_class]:
                send_data[student_class][student_name] = []
            
            test_id = 0
            for test_name, tests in tests_data.items():
                for test in tests:
                    test.update({"Вид теста": test_name, "id": test_id})
                    test_id += 1
                    send_data[student_class][student_name].append(test)

    # Преобразуем строку в boolean значение
    sort_param = sort_param == "sort-ahead" if sort_param else None
    # Возвращаем данные без фильтрации и сортировки, если параметры не заданы
    if sort_method is None and school_class is None:
        return send_data
    
    # Фильтрация по классу, если он задан
    if school_class:
      send_data = {sc_class: students for sc_class, students in send_data.items() if sc_class == school_class}

     # Сортировка, если задан метод сортировки и если данные не пустые
    if sort_method and send_data:
      send_data = sort_students(send_data, not(sort_param) , sort_method)
      
    return send_data


def search_students(classes, search_query):
    if not search_query:
        return classes
    filtered_classes = {}
    for class_name, students in classes.items():
        filtered_students = {}
        for student_name, tests in students.items():
            if search_query.lower() in student_name.lower():
                filtered_students[student_name] = tests
        if filtered_students:
            filtered_classes[class_name] = filtered_students
    return filtered_classes

