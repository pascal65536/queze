import sys
import io
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QApplication, QComboBox


class FirstForm(QWidget):

    def __init__(self):
        super(FirstForm, self).__init__()
        uic.loadUi("queze/first_widget.ui", self)

        self.tests.addItem("---")
        self.tests.addItem("1")
        self.tests.addItem("2")
        self.tests.addItem("3")

        self.name.editingFinished.connect(self.check_form)
        self.klass.editingFinished.connect(self.check_form)
        self.tests.activated.connect(self.check_form)

    def check_form(self):
        alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяё -."
        if len(self.name.text()) < 3:
            self.send_btn.setEnabled(False)
            return
        if not set(self.name.text().lower()) <= set(alphabet):
            self.send_btn.setEnabled(False)
            return
        if len(self.klass.text()) < 2:
            self.send_btn.setEnabled(False)
            return
        if self.tests.currentText() == "---":
            self.send_btn.setEnabled(False)
            return
        self.send_btn.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = FirstForm()
    form.show()
    sys.exit(app.exec())
