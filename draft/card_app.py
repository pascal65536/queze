import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, 
    QTreeView, QTextEdit, QPushButton, QLabel, QFileDialog
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import markdown2





class CardApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Card Test Application")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Tree View for cards
        self.tree_view = QTreeView()
        self.card_model = QStandardItemModel()
        self.card_model.setHorizontalHeaderLabels(["Cards"])
        self.tree_view.setModel(self.card_model)

        # Text Editor for Markdown
        self.text_edit = QTextEdit()
        self.text_edit.textChanged.connect(self.update_preview)

        # Preview Label for rendered Markdown
        self.preview_label = QLabel()
        self.preview_label.setWordWrap(True)

        # Button to load images
        self.load_image_button = QPushButton("Load Image")
        self.load_image_button.clicked.connect(self.load_image)

        # Add widgets to layout
        self.layout.addWidget(self.tree_view)
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.load_image_button)
        self.layout.addWidget(self.preview_label)

        # Sample data
        self.populate_tree()

    def populate_tree(self):
        # Sample cards
        card1 = QStandardItem("Card 1")
        card2 = QStandardItem("Card 2")
        
        self.card_model.appendRow(card1)
        self.card_model.appendRow(card2)

    def update_preview(self):
        markdown_text = self.text_edit.toPlainText()
        html = markdown2.markdown(markdown_text)
        self.preview_label.setText(html)


    def load_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "Images (*.png *.xpm *.jpg *.jpeg);;All Files (*)", options=options)
        
        if file_path:
            image_tag = f"![Image]({file_path})"
            current_text = self.text_edit.toPlainText()
            new_text = f"{current_text}n{image_tag}n"
            self.text_edit.setPlainText(new_text)
            self.update_preview()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CardApp()
    window.show()
    sys.exit(app.exec())
