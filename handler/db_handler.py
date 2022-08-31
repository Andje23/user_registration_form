import sqlite3

from PyQt5 import QtCore
from loguru import logger

logger.add("db_handler.log", format="{time} {level} {message}", level="DEBUG",
           rotation="1 week", compression="zip")


@logger.catch
def _user_existence_check(cursor: sqlite3.Connection.cursor, login: str):
    try:
        cursor.execute(f"SELECT * FROM users WHERE name='{login}';")
    except sqlite3.ProgrammingError as exception_programming_error:
        logger.error("Исключение sqlite3.ProgrammingError возникает из за ошибки программирования, например:\n"
                     "таблица не найдена или уже существует,\n"
                     "синтаксическая ошибка в операторе SQL,\n"
                     "неверное количество указанных параметров и т. д.\n"
                     f"{exception_programming_error}")
    except sqlite3.OperationalError as exception_operation_error:
        logger.error("Исключение sqlite3.OperationalError возникает при ошибках, связанных с работой базы данных и "
                     "не обязательно находятся под контролем программиста, например:\n"
                     "происходит неожиданное отключение,\n"
                     "имя источника данных не найдено,\n"
                     "транзакция не может быть обработана и т. д.\n"
                     f"{exception_operation_error}")
    value = cursor.fetchall()
    return value


@logger.catch
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
        logger.info(f"Успешная авторизация! login: {login} , password: {password}")
    else:
        signal.emit("Проверьте правильность ввода данных!")
        logger.info(f"Проверьте правильность ввода данных! login: {login} , password: {password}")

    cursor.close()
    connection.close()


@logger.catch
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
        logger.info(f"Такой ник уже используется! login: {login} , password: {password}")

    elif not value:
        cursor.execute(f"INSERT INTO users (name, password) VALUES ('{login}', '{password}')")
        signal.emit("Вы успешно зарегистрированы!")
        logger.info(f"Вы успешно зарегистрированы! login: {login} , password: {password}")
        connection.close()

    cursor.close()
    connection.close()
