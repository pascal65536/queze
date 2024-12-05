import sys
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QApplication,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QUrl
from markdown2 import markdown


class MarkdownViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Markdown Viewer")
        layout = QHBoxLayout()
        self.markdown_input = QTextEdit(self)
        self.markdown_input.setPlaceholderText("Введите ваш Markdown код здесь...")
        self.markdown_input.setFixedWidth(500)
        layout.addWidget(self.markdown_input)
        self.markdown_input.textChanged.connect(self.update_output)
        self.setLayout(layout)

    def update_output(self):
        markdown_text = self.markdown_input.toPlainText()
        html_text = markdown(markdown_text)
        html = f"<!DOCTYPE html><html>{html_text}</html>"
        html1 = """
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
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = MarkdownViewer()
    viewer.show()
    sys.exit(app.exec())
