import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from check_db import *
from des import *
from loguru import logger

logger.add("main.log", format="{time} {level} {message}", level="DEBUG",
           rotation="1 week", compression="zip")


@logger.catch
class Interface(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.reg)
        self.ui.pushButton.clicked.connect(self.auth)
        self.base_line_edit = [self.ui.lineEdit, self.ui.lineEdit_2]

        self.check_db = CheckThread()
        self.check_db.my_signal.connect(self.signal_handler)

    def check_input(function):
        def wrapper(self):
            for line_edit in self.base_line_edit:
                if len(line_edit.next()) == 0:
                    return
            function(self)
        return wrapper

    def signal_handler(self, value: str):
        QtWidgets.QMessageBox.about(self, 'оповещение', value)