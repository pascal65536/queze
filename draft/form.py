import sys
from PyQt6.QtWidgets import QApplication, QWidget, QFormLayout, QLineEdit, QPushButton, QComboBox
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Авторизация')

        self.layout = QFormLayout()

        # Фамилия
        self.last_name_input = QLineEdit()
        self.layout.addRow('Фамилия:', self.last_name_input)

        # Имя
        self.first_name_input = QLineEdit()
        self.layout.addRow('Имя:', self.first_name_input)

        # Класс
        self.class_input = QLineEdit()
        self.layout.addRow('Класс:', self.class_input)

        # Выпадающий список с темами тестов
        self.test_themes_combo = QComboBox()
        self.test_themes_combo.addItems(['Математика', 'Физика', 'Химия', 'Биология', 'История', 'География'])
        self.layout.addRow('Тема теста:', self.test_themes_combo)

        # Кнопка "Отправить"
        self.submit_button = QPushButton('Отправить')
        self.submit_button.clicked.connect(self.on_submit)
        self.layout.addRow(self.submit_button)

        self.setLayout(self.layout)

    def on_submit(self):
        last_name = self.last_name_input.text()
        first_name = self.first_name_input.text()
        class_name = self.class_input.text()
        selected_theme = self.test_themes_combo.currentText()

        print(f'Фамилия: {last_name}')
        print(f'Имя: {first_name}')
        print(f'Класс: {class_name}')
        print(f'Тема теста: {selected_theme}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())