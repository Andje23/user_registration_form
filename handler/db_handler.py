import sqlite3
from PyQt5 import QtCore


def login(login: str, password: str, signal: QtCore.pyqtSignal) -> None:
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
    cursor.execute(f"SELECT * FROM users WHERE name='{login}';")
    value = cursor.fetchall()

    if value != [] and value[0][2] == password:
        signal.emit("Успешная авторизация!")
    else:
        signal.emit("Проверьте правильность ввода данных!")

    cursor.close()
    connection.close()