from PyQt5 import QtCore
from handler.db_handler import *
from loguru import logger

logger.add("db_check.log", format="{time} {level} {message}", level="DEBUG",
           rotation="1 week", compression="zip")


@logger.catch
class CheckThread(QtCore.QThread):
    my_signal = QtCore.pyqtSignal(str)

    def thread_login(self, name: str, password: str):
        login(name, password, self.mysignal)

    def thread_register(self, name: str, password: str):
        register(name, password, self.mysignal)
