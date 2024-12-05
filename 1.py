import behoof
import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QTextEdit, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt6 Приложение с вкладками')
        self.layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)
        self.data_lst = behoof.load_json('data', 'content.json')
        for idx, data in enumerate(self.data_lst):
            tab = QWidget()
            self.tab_widget.addTab(tab, f'Вкладка {idx + 1}')
            self.load_content_to_tab(tab, data)
        self.setLayout(self.layout)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())