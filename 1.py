import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Пример QWebEngineView")
        self.setGeometry(100, 100, 800, 600)

        # Создаем виджет для центральной области
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Создаем вертикальный layout
        layout = QVBoxLayout(central_widget)

        # Создаем экземпляр QWebEngineView
        self.web_view = QWebEngineView(self)

        # Загружаем веб-страницу
        url1 = QUrl()
        url1.setUrl("https://kompoblog.ru/")
        self.web_view.setUrl(url1)

        # Добавляем QWebEngineView в layout
        layout.addWidget(self.web_view)

        # Кнопка для обновления страницы
        refresh_button = QPushButton("Обновить страницу", self)
        refresh_button.clicked.connect(self.refresh_page)
        layout.addWidget(refresh_button)

    def refresh_page(self):
        html = '''
<!DOCTYPE html>
<html>
    <head>
        <title>My web page</title>
    </head>
    <body>
        <h1>Hello, world!</h1>
        <p>This is my first web page.</p>
        <p>It contains a 
             <strong>main heading</strong> and <em> paragraph </em>.
        </p>
    </body>
</html>        
        '''
        self.web_view.setHtml(html)
        # self.web_view.reload()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
