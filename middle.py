import re
import os
import sys
import time
import string
import behoof
import random
from PyQt6.QtWidgets import QFormLayout, QMessageBox, QComboBox, QTabWidget, QDialog, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer, QTime, Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.data_lst = behoof.load_json('data', 'content.json')
        self.theme = None
        self.title = None
        self.mashup = list()
        self.user = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Локальная тестирующая система')

        if self.user is None:
            title = list()
            for dl in self.data_lst:
                title.append(dl['title'])
            self.show_modal_window(title)
            return

        selected_theme = self.user.get('selected_theme')
        for dl in self.data_lst:
            if dl.get('title') == selected_theme:
                self.theme = dl
                self.title = dl['title']
                for mashup in dl['mashup']:
                    for k, v in mashup.items():
                        mashup_lst = dl.get('tests', dict()).get(k, list())
                        random.shuffle(mashup_lst)
                        self.mashup.extend(mashup_lst[:v])
                random.shuffle(self.mashup)
                break
        
        self.layout = QVBoxLayout()
        self.username_label = QLabel('Имя пользователя: Guest')
        self.layout.addWidget(self.username_label)
        self.time_layout = QHBoxLayout()
        self.current_time_label = QLabel('Текущее время: ')
        self.time_layout.addWidget(self.current_time_label)
        self.start_time = time.time()
        self.app_time_label = QLabel('Время работы приложения: 0 секунд')
        self.time_layout.addWidget(self.app_time_label)
        self.layout.addLayout(self.time_layout)
        self.tab_layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        self.tab_layout.addWidget(self.tab_widget)
        for idx, data in enumerate(self.mashup):
            tab = QWidget()
            self.tab_widget.addTab(tab, f'Вкладка {idx + 1}')
            self.load_content_to_tab(tab, data)
        self.input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('Введите ваш ответ здесь...')
        self.input_layout.addWidget(self.input_field)
        self.submit_button = QPushButton('Отправить')
        self.submit_button.clicked.connect(self.on_submit)
        self.input_layout.addWidget(self.submit_button)
        self.tab_layout.addLayout(self.input_layout) 
        self.layout.addLayout(self.tab_layout)
        self.setLayout(self.layout)    
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        current_time = QTime.currentTime().toString('hh:mm:ss')
        self.current_time_label.setText(f'Текущее время: {current_time}')
        app_time = int(time.time() - self.start_time)
        self.app_time_label.setText(f'Время работы приложения: {app_time} секунд')

    def on_alphabet_click(self, letter):
        self.question = string.ascii_uppercase.index(letter)
        self.load_content_from_json()

    def on_submit(self):
        user_input = self.input_field.text()
        print(f'Ответ пользователя: {user_input}')
        self.input_field.clear()

    def load_content_to_tab(self, tab, data):
        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(data['text'])
        layout.addWidget(text_edit)
        dip = data['image_path']
        if dip:
            image_label = QLabel()
            image_path = os.path.join('data', dip)
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                image_label.setPixmap(pixmap)
                image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(image_label)
        tab.setLayout(layout)

    def show_modal_window(self, title_lst):
        dialog = AuthorizationDialog(self, title_lst=title_lst)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.user = {
                'last_name': dialog.last_name_input.text(),
                'first_name': dialog.first_name_input.text(),
                'class_name': dialog.class_input.text(),
                'selected_theme': dialog.test_themes_combo.currentText()
            }
            self.initUI()  # Повторно инициализируем UI после авторизации


class AuthorizationDialog(QDialog):
    def __init__(self, parent=None, title_lst=list()):
        super().__init__(parent)
        self.setWindowTitle('Авторизация')
        self.layout = QFormLayout()
        self.last_name_input = QLineEdit()
        self.layout.addRow('Фамилия:', self.last_name_input)
        self.first_name_input = QLineEdit()
        self.layout.addRow('Имя:', self.first_name_input)
        self.class_input = QLineEdit()
        self.layout.addRow('Класс:', self.class_input)
        self.test_themes_combo = QComboBox()
        self.test_themes_combo.addItems(title_lst)
        self.layout.addRow('Тема теста:', self.test_themes_combo)
        self.submit_button = QPushButton('Отправить')
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
            QMessageBox.warning(self, 'Ошибка', 'Такие данные не допустимы.')
            return
        self.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
