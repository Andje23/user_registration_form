import sqlite3
from PyQt5 import QtCore
from loguru import logger

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")


def _user_existence_check(cursor: sqlite3.Connection.cursor, login: str):
    cursor.execute(f"SELECT * FROM users WHERE name='{login}';")
    value = cursor.fetchall()
    return value


def login(login: str, password: str, signal: QtCore.pyqtSignal) -> None:
    """
    User login.
    :param login: str. New user login
    :param password: str. New user password
    :param signal: QtCore.pyqtSignal. To display a process status message.
    :return: None
    """
    connection = sqlite3.connect('handler/users')
    cursor = connection.cursor()

    # Проверка на наличие пользователя
    value = _user_existence_check(cursor=cursor, login=login)

    if value != [] and value[0][2] == password:
        signal.emit("Успешная авторизация!")
    else:
        signal.emit("Проверьте правильность ввода данных!")

    cursor.close()
    connection.close()


def register(login: str, password: str, signal: QtCore.pyqtSignal) -> None:
    """
        Adding new users to the database.
        :param login: str. New user login
        :param password: str. New user password
        :param signal: QtCore.pyqtSignal. To display a process status message.
        :return: None
        """

    connection = sqlite3.connect('handler/users')
    cursor = connection.cursor()

    # Проверка на наличие пользователя
    value = _user_existence_check(cursor=cursor, login=login)

    if value:
        signal.emit("Такой ник уже используется!")

    elif not value:
        cursor.execute(f"INSERT INTO users (name, password) VALUES ('{login}', '{password}')")
        signal.emit("Вы успешно зарегистрированы!")
        connection.close()

    cursor.close()
    connection.close()

