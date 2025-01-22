import requests
import qrcode

def get_pixmap_qr(self):
    """
    Генерация QR-кода
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(self.calc())
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    pixmap = QPixmap()
    pixmap.loadFromData(buffered.getvalue())
    return pixmap

def calc(self):
    uuid_dct = behoof.load_json("user", f"{self.uuid}.json")
    user_dct = dict()
    for key, value in uuid_dct.items():
        name, char, test_value = key.split("|")
        for mashup in self.mashup:
            if mashup["theme"] != name:
                continue
            if mashup["char"] != char:
                continue

            if value == test_value.split(":")[0]:
                result = char.upper()
            else:
                result = char.lower()
            user_dct.setdefault(name, list()).append(result)

    tests = list()
    for key in user_dct.keys():
        tests.append({"theme": key, "selected": "".join(user_dct[key])})

    user_data = {
        "last_name": self.user["last_name"],
        "first_name": self.user["first_name"],
        "class_name": self.user["class_name"],
        "selected_theme": self.user["selected_theme"],
        "date": self.user["date"],
        "tests": tests,
    }
    user_data["mashup"] = "|".join(
        [f"{test['theme']}_{test['selected']}" for test in user_data["tests"]]
    )
    return self.get_url(user_data)

def get_url(self, ud):
    # Базовый URL
    base_url = "http://127.0.0.1:5000/get_data?"

    # Создание словаря с параметрами
    params = {
        "mashup": ud["mashup"],
        "date": ud["date"],
        "selected_theme": ud["selected_theme"],
        "class_name": ud["class_name"],
        "first_name": ud["first_name"],
        "last_name": ud["last_name"],
    }
    # Формирование полного URL с параметрами
    full_url = base_url + requests.compat.urlencode(params)
    return full_url