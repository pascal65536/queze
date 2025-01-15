import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Styled QTabWidget Example")
        self.setGeometry(100, 100, 400, 300)

        # Создаем QTabWidget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Применяем стиль к QTabBar
        self.apply_styles()

        # Добавляем вкладки
        self.add_tabs()

    def apply_styles(self):
        style_sheet = """
        QTabBar::tab {
            width: 100px;
        }

        QTabBar::tab {
            font-weight: bold; /* Сделать текст жирным (опционально) */
            text-decoration: underline; /* Подчеркнуть текст */
        }  

        /* Подчеркивание текста второй вкладки */
        QTabBar::tab:nth-child(2) {
            font-weight: bold; /* Сделать текст жирным (опционально) */
            text-decoration: underline; /* Подчеркнуть текст */
        }      
        """
        self.tab_widget.setStyleSheet(style_sheet)


    def add_tabs(self):
        # Вкладка 1
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        tab1.setLayout(tab1_layout)
        tab1_layout.addWidget(QLabel("Содержимое вкладки 1"))
        self.tab_widget.addTab(tab1, "Вкладка 1")

        # Вкладка 2
        tab2 = QWidget()
        tab2_layout = QVBoxLayout()
        tab2.setLayout(tab2_layout)
        tab2_layout.addWidget(QLabel("Содержимое вкладки 2"))
        self.tab_widget.addTab(tab2, "Вкладка 2")

        # Вкладка 3
        tab3 = QWidget()
        tab3_layout = QVBoxLayout()
        tab3.setLayout(tab3_layout)
        tab3_layout.addWidget(QLabel("Содержимое вкладки 3"))
        self.tab_widget.addTab(tab3, "Вкладка 3")


style_sheet = """
        QTabBar::tab {
            width: 100px;
        }

        QTabBar::tab {
            font-weight: bold; /* Сделать текст жирным (опционально) */
        }  

        /* Подчеркивание текста второй вкладки */
        QTabBar::tab:nth-child(2) {
            text-decoration: underline; /* Подчеркнуть текст */
        }      
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
