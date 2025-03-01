import re
import os
import sys
import time
import uuid
import string
import behoof
import random
import datetime
from io import BytesIO
from PyQt6.QtWidgets import (
    QFormLayout,
    QMessageBox,
    QComboBox,
    QTabWidget,
    QDialog,
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import QTimer, QTime, Qt
from PIL import Image, ImageDraw, ImageFont


FONT = QFont(None, 16, QFont.Weight.Bold)

style_sheet = "QTabBar::tab {width: 100px; font-weight: bold;}"


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.data_dct = behoof.load_json("data", "collection.json")
        self.mashup = list()
        self.user = None
        self.key = None
        self.test_name = None
        self.test_char = None
        self.test_value = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Локальная тестирующая система")
        self.resize(800, 600)

        if self.user is None:
            title = list()
            for dl in self.data_dct.values():
                title.append(dl["title"])
            self.show_modal_window(title)
            return

        self.uuid = self.user.get("uuid")
        last_name = self.user.get("last_name")
        first_name = self.user.get("first_name")
        selected_theme = self.user.get("selected_theme")
        self.setWindowTitle(f"{selected_theme} | {last_name} {first_name}")

        for dl in self.data_dct.values():
            if dl.get("title") != selected_theme:
                continue

            for tests in dl.get("tests", list()):
                for mashup in dl["mashup"]:
                    if mashup.keys() != tests.keys():
                        continue
                    for key in mashup.keys():
                        mashup_lst = tests[key]
                        for ml in mashup_lst:
                            ml["theme"] = key
                        random.shuffle(mashup_lst)
                        self.mashup.extend(mashup_lst[: mashup[key]])
            break

        self.layout = QVBoxLayout()

        self.user_layout = QHBoxLayout()
        self.username_label = QLabel(f"Имя пользователя: {last_name} {first_name}")
        self.username_label.setFont(FONT)

        self.user_layout.addWidget(self.username_label)
        self.final_button = QPushButton("Закончить")

        self.final_button.clicked.connect(self.on_final)
        self.final_button.setFont(FONT)

        self.user_layout.addWidget(self.final_button)
        self.layout.addLayout(self.user_layout)

        self.time_layout = QHBoxLayout()
        self.current_time_label = QLabel("Текущее время: ")
        self.current_time_label.setFont(FONT)

        self.time_layout.addWidget(self.current_time_label)
        self.start_time = time.time()
        self.app_time_label = QLabel("Время работы приложения: 0 секунд")
        self.app_time_label.setFont(FONT)

        self.time_layout.addWidget(self.app_time_label)
        self.layout.addLayout(self.time_layout)
        self.tab_layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        self.tab_widget.currentChanged.connect(self.on_tab_change)

        self.tab_layout.addWidget(self.tab_widget)
        self.tab_widget.setStyleSheet(style_sheet)

        self.input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите ваш ответ здесь...")
        self.input_field.setFont(FONT)

        self.input_layout.addWidget(self.input_field)
        self.submit_button = QPushButton("Отправить")
        self.submit_button.clicked.connect(self.on_submit)
        self.submit_button.setFont(FONT)

        self.input_layout.addWidget(self.submit_button)
        self.tab_layout.addLayout(self.input_layout)
        self.layout.addLayout(self.tab_layout)
        self.setLayout(self.layout)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.load_content_to_tab_layout(self.mashup)
        self.check_final()

    def check_final(self):
        uuid_dct = behoof.load_json("user", f"{self.uuid}.json")
        user_dct = dict()
        for key in uuid_dct.keys():
            name, char, test_value = key.split("|")
            user_dct.setdefault(name, list()).append(char)
        is_final = True
        for mashup in self.mashup:
            if mashup["char"] not in user_dct.get(mashup["theme"], list()):
                is_final = False
        self.final_button.setDisabled(not is_final)

    def colorize(self, text):
        # Заменить цвет фона
        if len(text) == 0:
            style = "background-color: white;"
        else:
            style = "background-color: lightblue;"
        self.tab_widget.currentWidget().setStyleSheet(style)
        # Обновление стиля
        self.tab_widget.style().unpolish(self.tab_widget)
        self.tab_widget.style().polish(self.tab_widget)
        self.tab_widget.update()

    def on_tab_change(self, index):
        self.key = self.tab_widget.currentWidget().name
        name, char, value = self.key.split("|")
        self.test_name = name
        self.test_char = char
        self.test_value = value

        self.input_field.clear()
        uuid_dct = behoof.load_json("user", f"{self.uuid}.json")
        user_input = uuid_dct.get(self.key, str())
        self.input_field.setText(user_input)
        self.colorize(user_input)
        self.check_final()

    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.current_time_label.setText(f"Текущее время: {current_time}")
        app_time = int(time.time() - self.start_time)
        self.app_time_label.setText(f"Время работы приложения: {app_time} секунд")

    def on_final(self):
        self.hide()
        self.result_window = ResultWindow(self.uuid, self.user, self.mashup)
        self.result_window.show()

    def on_submit(self):
        user_input = self.input_field.text()
        uuid_dct = behoof.load_json("user", f"{self.uuid}.json")
        uuid_dct[self.key] = user_input
        behoof.save_json("user", f"{self.uuid}.json", uuid_dct)
        self.colorize(user_input)
        self.check_final()

    def load_content_to_tab_layout(self, mashup):
        for idx, data in enumerate(mashup):
            tab = QWidget()
            answers = "?".join(f"{z['text']}:{z['weight']}" for z in data["answers"])
            tab.name = f'{data["theme"]}|{data["char"]}|{answers}'
            self.tab_widget.addTab(tab, f"Вопрос {idx + 1}")

            text = "\n".join(data["question"])
            layout = QVBoxLayout()
            text_edit = QTextEdit()
            text_edit.setReadOnly(True)
            text_edit.setPlainText(text)
            text_edit.setFont(FONT)
            layout.addWidget(text_edit)

            dip = data.get("images")
            if not dip:
                tab.setLayout(layout)
                continue

            image_label = QLabel()
            image_path = os.path.join("data", dip)
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                if pixmap.height() > 600:
                    h = int(pixmap.width() * (600 / pixmap.height()))
                    pixmap = pixmap.scaled(h, 600, Qt.AspectRatioMode.KeepAspectRatio)
                image_label.setPixmap(pixmap)
                image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(image_label)
            tab.setLayout(layout)

    def show_modal_window(self, title_lst):
        dialog = AuthorizationDialog(self, title_lst=title_lst)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.user = {
                "last_name": dialog.last_name_input.text(),
                "first_name": dialog.first_name_input.text(),
                "class_name": dialog.class_input.text(),
                "selected_theme": dialog.test_themes_combo.currentText(),
                "tests": list(),
                "date": datetime.datetime.now().isoformat(),
                "uuid": str(uuid.uuid4()),
            }
            self.initUI()


class ResultWindow(QWidget):
    def __init__(self, uuid, user, mashup):
        super().__init__()

        self.uuid = uuid
        self.user = user
        self.mashup = mashup
        self.score, self.count = self.calc_score()
        self.round_score = int((self.score / self.count) * 100)

        self.setWindowTitle(f"Результаты теста")
        self.setGeometry(150, 150, 400, 300)

        last_name = self.user.get("last_name")
        first_name = self.user.get("first_name")
        selected_theme = self.user.get("selected_theme")
        class_name = self.user.get("class_name")

        self.layout = QVBoxLayout()

        self.user_layout = QHBoxLayout()
        text = f"Пользователь: {last_name} {first_name}"
        self.name_label = QLabel(text, self)
        self.name_label.setFont(FONT)
        self.user_layout.addWidget(self.name_label)
        text = f"Количество процентов: {self.round_score}"
        text = f"Количество процентов: {self.round_score}"
        self.score_label = QLabel(text, self)
        self.score_label.setFont(FONT)
        self.user_layout.addWidget(self.score_label)
        self.layout.addLayout(self.user_layout)

        self.test_layout = QHBoxLayout()
        text = f"Тема теста: {selected_theme}"
        self.test_label = QLabel(text, self)
        self.test_label.setFont(FONT)
        self.test_layout.addWidget(self.test_label)
        text = f"Верных ответов: {self.score}"
        self.score_label = QLabel(text, self)
        self.score_label.setFont(FONT)
        self.test_layout.addWidget(self.score_label)
        self.layout.addLayout(self.test_layout)

        self.score_layout = QHBoxLayout()
        text = f"Класс: {class_name}"
        self.class_label = QLabel(text, self)
        self.class_label.setFont(FONT)
        self.score_layout.addWidget(self.class_label)
        text = f"Задано вопросов: {self.count}"
        self.count_label = QLabel(text, self)
        self.count_label.setFont(FONT)
        self.score_layout.addWidget(self.count_label)
        self.layout.addLayout(self.score_layout)

        self.pic_label = QLabel(self)
        self.pic_label.setPixmap(self.get_pixmap())
        self.layout.addWidget(self.pic_label)

        self.close_button = QPushButton("Закрыть", self)
        self.close_button.setFont(FONT)
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

    def calc_score(self):
        uuid_dct = behoof.load_json("user", f"{self.uuid}.json")
        score = 0
        count = 0
        for key, value in uuid_dct.items():
            name, char, test_value = key.split("|")
            for mashup in self.mashup:
                if mashup["theme"] != name:
                    continue
                if mashup["char"] != char:
                    continue
                count += 1
                if value == test_value.split(":")[0]:
                    score += int(test_value.split(":")[1])
        return score, count

    def get_pixmap(self):
        width, height = 800, 800
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        try:
            fnt = os.path.join("fonts", "Krasnoyarsk.otf")
            font = ImageFont.truetype(fnt, 200)
            font = ImageFont.truetype(fnt, 200)
        except IOError:
            font = ImageFont.load_default()
        text = str(self.round_score) + '%'
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        draw.text((x, y), text, fill="black", font=font)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        pixmap = QPixmap()
        pixmap.loadFromData(buffered.getvalue())
        return pixmap


class AuthorizationDialog(QDialog):
    def __init__(self, parent=None, title_lst=list()):
        super().__init__(parent)
        self.setWindowTitle("Авторизация")
        self.layout = QFormLayout()
        self.last_name_input = QLineEdit()
        self.layout.addRow("Фамилия:", self.last_name_input)
        self.first_name_input = QLineEdit()
        self.layout.addRow("Имя:", self.first_name_input)
        self.class_input = QLineEdit()
        self.layout.addRow("Класс:", self.class_input)
        self.test_themes_combo = QComboBox()
        self.test_themes_combo.addItems(title_lst)
        self.layout.addRow("Тема теста:", self.test_themes_combo)
        self.submit_button = QPushButton("Отправить")
        self.submit_button.clicked.connect(self.validate_and_accept)
        self.layout.addRow(self.submit_button)
        self.setLayout(self.layout)

    def validate_and_accept(self):
        is_valid = True
        last_name = self.last_name_input.text().strip()
        first_name = self.first_name_input.text().strip()
        class_name = self.class_input.text().strip()
        if not class_name:
            is_valid = False
        elif len(class_name) not in [2, 3]:
            is_valid = False
        elif class_name[-1].lower() not in behoof.rus_alphabet:
            is_valid = False
        elif not class_name[:-1].isdigit():
            is_valid = False
        elif not last_name:
            is_valid = False
        elif len(last_name) < 2:
            is_valid = False
        elif set(last_name.lower()) - set(behoof.rus_alphabet):
            is_valid = False
        elif not first_name:
            is_valid = False
        elif len(first_name) < 2:
            is_valid = False
        elif set(first_name.lower()) - set(behoof.rus_alphabet):
            is_valid = False
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", "Такие данные не допустимы.")
            return
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())