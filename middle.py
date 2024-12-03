import sys
import time
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer, QTime, Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt6 Приложение')

        self.layout = QVBoxLayout()

        # Имя пользователя
        self.username_label = QLabel('Имя пользователя: Guest')
        self.layout.addWidget(self.username_label)

        # Текущее время и время работы приложения в одной строке
        self.time_layout = QHBoxLayout()
        self.current_time_label = QLabel('Текущее время: ')
        self.time_layout.addWidget(self.current_time_label)
        self.start_time = time.time()
        self.app_time_label = QLabel('Время работы приложения: 0 секунд')
        self.time_layout.addWidget(self.app_time_label)
        self.layout.addLayout(self.time_layout)

        # 27 кнопок с буквами алфавита
        self.alphabet_layout = QHBoxLayout()
        self.alphabet_buttons = []
        for letter in 'ABCDEFGH':
            button = QPushButton(letter)
            button.clicked.connect(lambda _, l=letter: self.on_alphabet_click(l))
            self.alphabet_buttons.append(button)
            self.alphabet_layout.addWidget(button)
        self.layout.addLayout(self.alphabet_layout)

        # Три абзаца текста и картинка из JSON файла
        self.load_content_from_json('data/content.json')

        # Поле для ввода ответа и кнопка "Отправить" в одной строке
        self.input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('Введите ваш ответ здесь...')
        self.input_layout.addWidget(self.input_field)
        self.submit_button = QPushButton('Отправить')
        self.submit_button.clicked.connect(self.on_submit)
        self.input_layout.addWidget(self.submit_button)
        self.layout.addLayout(self.input_layout)

        self.setLayout(self.layout)

        # Таймер для обновления времени
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Обновлять каждую секунду

    def update_time(self):
        current_time = QTime.currentTime().toString('hh:mm:ss')
        self.current_time_label.setText(f'Текущее время: {current_time}')

        app_time = int(time.time() - self.start_time)
        self.app_time_label.setText(f'Время работы приложения: {app_time} секунд')

    def on_alphabet_click(self, letter):
        print(f'Нажата кнопка с буквой: {letter}')

    def on_submit(self):
        user_input = self.input_field.text()
        print(f'Ответ пользователя: {user_input}')
        self.input_field.clear()

    def load_content_from_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Три абзаца текста
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlainText(data['text'])
        self.layout.addWidget(self.text_edit)

        # Картинка
        self.image_label = QLabel()
        pixmap = QPixmap(data['image_path'])
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())