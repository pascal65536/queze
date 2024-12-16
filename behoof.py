import os
import json
import uuid
import shutil
import hashlib
import datetime
import string
import random


def load_json(folder_name, file_name):
    """
    Функция загружает данные из JSON-файла. Если указанный каталог
    не существует, она создает его. Если файл не существует,
    функция создает пустой JSON-файл. Затем она загружает
    и возвращает содержимое файла в виде словаря.
    """
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    filename = os.path.join(folder_name, file_name)
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(dict(), f, ensure_ascii=True)
    with open(filename, encoding="utf-8") as f:
        load_dct = json.load(f)
    return load_dct


def save_json(folder_name, file_name, save_dct):
    """
    Функция сохраняет словарь в формате JSON в указанный файл.
    Если указанный каталог не существует, она создает его.
    Затем она записывает переданный словарь в файл с заданным именем.
    """
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    filename = os.path.join(folder_name, file_name)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(save_dct, f, ensure_ascii=False, indent=4)


def upload_file(folder_name, uploaded_file, ext_lst=None):
    """
    Функция загружает файл в указанную папку, проверяет его расширение
    и создает уникальное имя для сохранения.
    Если папка не существует, она создается.
    Файл сохраняется в структуре папок на основе первых двух
    символов уникального имени файла.
    """
    if not ext_lst:
        ext_lst = ["jpg", "png", "gif", "jpeg", "webp"]
    uploaded_file_read = uploaded_file.read()
    filename = uploaded_file.filename
    ext = filename.split(".")[-1].lower()
    if ext not in ext_lst:
        return
    secret_filename = f"{uuid.uuid4()}.{ext}"
    folder = os.path.join(folder_name, secret_filename[:2], secret_filename[2:4])
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, secret_filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file_read)
    return file_path


def get_fake_userdata():

    def get_score(n, rating=0.5):
        alpha = list(string.ascii_lowercase)
        random.shuffle(alpha)
        res = ''
        for i in range(n):
            res += alpha[i] if random.random() > rating else alpha[i].upper()
        return res

    rating = random.random()
    user_data = {
        "last_name": behoof.generate_fake_name(),
        "first_name": behoof.generate_alternating_name(),
        "class_name": f'9{random.choice(behoof.rus_alphabet)}'.upper(),
        "selected_theme": "Тест по информатике",
        "date": datetime.datetime.now().isoformat(),
        "tests": [
            {"theme": "Анимация", "selected": get_score(6, rating)},
            {"theme": "Программирование", "selected": get_score(6, rating)},
            {"theme": "Текст", "selected": get_score(6, rating)},
            {"theme": "Видео", "selected": get_score(6, rating)},
        ],
    }
    user_data["mashup"] = "|".join(
        [f"{test['theme']}_{test['selected']}" for test in user_data["tests"]]
    )
    return user_data


def get_md5hash(word):
    return hashlib.md5(word.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    pass
