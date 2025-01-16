import re
import os
import sys
import time
import uuid
import string
import behoof
import random
import datetime
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
import style

FONT = QFont(None, 16, QFont.Weight.Bold)


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

        self.user = {
            "last_name": "Воробей",
            "first_name": "Джек",
            "class_name": "11Ж",
            "selected_theme": "Это название теста",
            "tests": [],
            "date": "2025-01-17T01:13:11.903253",
            "uuid": "238dc614-e096-4d20-b1e2-d489a92b1cdc",
        }

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
        # self.final_button.setDisabled(True)
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
        self.tab_widget.setStyleSheet(style.style_sheet)

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


    def on_tab_change(self, index):
        self.key = self.tab_widget.currentWidget().name
        name, char, value = self.key.split("|")
        self.test_name = name
        self.test_char = char
        self.test_value = value

        self.input_field.clear()
        uuid_dct = behoof.load_json("user", f"{self.uuid}.json")
        self.input_field.setText(uuid_dct.get(self.key, str()))
        

    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.current_time_label.setText(f"Текущее время: {current_time}")
        app_time = int(time.time() - self.start_time)
        self.app_time_label.setText(f"Время работы приложения: {app_time} секунд")

    def on_final(self):
        print(f"Пользователь зафиналил")

    def on_submit(self):
        user_input = self.input_field.text()
        print(
            f"Ответ пользователя: {user_input} {self.test_name} {self.test_char} {self.test_value}"
        )
        for test_value in self.test_value.split("?"):
            q, a = test_value.split(":")
            if q == user_input:
                print(f"Правильно")
        # self.input_field.clear()
        # import ipdb; ipdb.sset_trace()
        uuid_dct = behoof.load_json("user", f"{self.uuid}.json")
        uuid_dct[self.key] = user_input
        behoof.save_json("user", f"{self.uuid}.json", uuid_dct)


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
        last_name = self.last_name_input.text()
        first_name = self.first_name_input.text()
        class_name = self.class_input.text()
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
        elif len(last_name) < 4:
            is_valid = False
        elif set(last_name.lower()) - set(behoof.rus_alphabet):
            is_valid = False
        elif not first_name:
            is_valid = False
        elif len(first_name) < 4:
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
