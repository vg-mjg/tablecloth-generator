# widgets.py - Soon to hold separate widget classes
from PySide6.QtWidgets import QWidget, QMessageBox

class EditionWidget(QWidget):

    def __init__(self):
        super().__init__()


    def closeEvent(self, event):
        close_dialog = QMessageBox(self)
        close_dialog.setWindowTitle("Team Editor")
        close_dialog.setText("Do you wish to close the editor?")
        close_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        response = close_dialog.exec()

        if response == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()