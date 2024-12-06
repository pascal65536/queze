import sys

from PyQt6 import uic

from PyQt6.QtWidgets import QApplication, QWidget


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("1_experiment.ui", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Calculator()
    ex.show()
    sys.exit(app.exec())
