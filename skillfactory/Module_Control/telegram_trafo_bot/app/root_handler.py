from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Filter

import mysql.connector

from app.config import host, port, user, password

from app.keyboard import root_keyboard  # доступ к кнопке Back

import app.keyboard as kb

root_router = Router()

conn = None  # определение первоначального состояния подключения к БД

db_name = None  # для использования в других функциях

# Словари
chat_data = {}
user_states = {}

# ********************* ID'S
# Список Root Group
root_id = [1035107072,  # Daniel
           103200201    # Dima
          ]

# Список Maintenance Group
maintenance_id = [1035107072, # Daniel
                  103200201   # Dima
                 ]

# ---------------------------

#                        ROOT                          #
#  **************************************************  #

class Root(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in root_id

@root_router.message(Root(), F.text == 'Root')
async def root(message: Message):
    print(f"{message.from_user.id} entered to Root")
    await message.answer('Root Status :: [OK]', reply_markup=kb.root)

    # Устанавливаем соединение с базой данных MySQL
    try:
        global conn
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
        )
        await message.answer("Connection to MySQL was successful.")
        print(f"{message.from_user.id} connection to MySQL was successful.")
    except mysql.connector.Error as ex:
        await message.answer(f"Connection to MySQL is not established: {ex}")

# -------------- DATABASE MENU --------------

@root_router.message(F.text == 'Database Menu')
async def db_menu(message: Message):
    print(f"{message.from_user.id} Database Menu Open")

    # Вызываем функцию db_list для вывода списка доступных баз данных
    await db_list(message)

    # Ожидание ввода имени базы данных
    await message.answer("Введите имя БД для подключения\n Или 'exit' для выхода.")

    # Сохраняем состояние пользователя - ожидание ввода имени базы данных
    user_states[message.from_user.id] = "waiting_for_db_name"


@root_router.message(lambda message: message.from_user.id in user_states and user_states[
    message.from_user.id] == "waiting_for_db_name")
async def db_choose(message: Message):
    db_name = message.text.strip()

    # Проверка на ввод 'exit'
    if db_name.lower() == 'exit':
        # Устанавливаем состояние пользователя
        user_states.pop(message.from_user.id, None)
        await message.answer("Выход из режима ввода.")
        return

    try:
        # Подключение к ранее установленному соединению с базой данных MySQL
        conn.database = db_name

        # Вывод сообщения об успешном подключении
        await message.answer(f"Connection to the << {db_name} >> was successful.")
        print(f"{message.from_user.id} connection to the << {db_name} >> was successful.")

        # Устанавливаем дальнейшее состояние пользователя
        user_states[message.from_user.id] = "connected_to_db"

        # Выводим дальнейшее меню
        await message.answer("...", reply_markup=kb.database_menu)

    except mysql.connector.Error as ex:
        # Обработка ошибки подключения
        await message.answer(f"Connection is not established: {ex}")

# -------------- Database --------------
@root_router.message(F.text == 'Database')
async def database(message: Message):
    print(f"{message.from_user.id} entered to Database")
    await message.answer("...", reply_markup=kb.database)

# -------------- D.Add
@root_router.message(F.text == 'D.Add')
async def db_add(message: Message):
    print(f"{message.from_user.id} Database Add")
    await message.answer("Введите Имя БД Для Добавления: ")

    # Сохраняем состояние пользователя - ожидание ввода имени базы данных
    user_states[message.from_user.id] = "waiting_for_db_name_add"

# Middleware для обработки ввода от пользователя
@root_router.message(lambda message: message.from_user.id in user_states and user_states[
    message.from_user.id] == "waiting_for_db_name_add")
async def db_name_input(message: Message):
    global db_name
    db_name = message.text.strip()

    if conn is not None:
        try:
            # Создаем курсор для выполнения SQL-запросов
            with conn.cursor() as curs:
                # Проверяем, существует ли уже такая база данных
                curs.execute(f"SHOW DATABASES LIKE '{db_name}'")
                result = curs.fetchone()

                if result:
                    await message.answer(f"БД {db_name} уже существует, введите другое имя.")
                else:
                    # База данных не существует, выполним добавление
                    curs.execute(f"CREATE DATABASE {db_name}")

                    # После завершения обработки, очистите состояние пользователя
                    user_states.pop(message.from_user.id, None)

                    await message.answer(f"БД << {db_name} >> добавлена.")
                    print(f"{message.from_user.id}: БД << {db_name} >> добавлена.")

        except mysql.connector.Error as ex:
            print(f"Error in db_name_input:\n {ex}")
            await message.answer(f"Error in db_name_input\n {ex}")

# -------------- D.Remove
@root_router.message(F.text == 'D.Remove')
async def db_remove(message: Message):
    print(f"{message.from_user.id} Remove")
    await message.answer("Введите Имя БД для Удаления: ")

    # Сохраняем состояние пользователя - ожидание ввода имени базы данных
    user_states[message.from_user.id] = "waiting_for_db_name"

# Middleware для обработки ввода от пользователя
@root_router.message(lambda message: message.from_user.id in user_states and user_states[
    message.from_user.id] == "waiting_for_db_name")
async def db_remove_name(message: Message):
    global db_name
    db_name = message.text.strip()

    if conn is not None:
        try:
            # Создаем курсор для выполнения SQL-запросов
            with conn.cursor() as curs:
                # Проверяем, существует ли такая база данных
                curs.execute(f"SHOW DATABASES LIKE '{db_name}'")
                result = curs.fetchone()

                if result:
                    # База данных существует, выполним удаление
                    curs.execute(f"DROP DATABASE {db_name}")

                    # После завершения обработки, очистите состояние пользователя
                    user_states.pop(message.from_user.id, None)

                    await message.answer(f"БД << {db_name} >> была удалена.")
                    print(f"{message.from_user.id}: БД << {db_name} >> удалена.")
                else:
                    await message.answer(f"БД << {db_name} >> не существует, попробуйте заново.")

        except mysql.connector.Error as ex:
                    print(f"Error in db_list: {ex}")
                    await message.answer(f"Error in db_remove\n {ex}")

# -------------- D.List
@root_router.message(F.text == 'D.List')
async def db_list(message: Message):
    print(f"{message.from_user.id} List")

    if conn is not None:
        try:
            with conn.cursor() as curs:
                curs.execute("SHOW DATABASES")
                databases = curs.fetchall()
                for db in databases:
                    print(db[0])
                await message.answer("List of Databases:\n" + "\n".join(db[0] for db in databases))
        except mysql.connector.Error as ex:
            print(f"Error in db_list: {ex}")
            await message.answer(f"Error in db_list\n {ex}")

# -------------- TABLE --------------

@root_router.message(F.text == 'Table')
async def db_table(message: Message):
    print(f"{message.from_user.id} entered to Table")
    await message.answer("...", reply_markup=kb.table)

# -------------- T.Add
@root_router.message(F.text == 'T.Add')
async def tb_add(message: Message):

    print(f"{message.from_user.id} Table Add")
    await message.answer(f"Вы в режиме добавления Таблиц в БД << {db_name} >>\n"
                         f"Ввод буквенный, формат 'test_tb'\n"
                         f"Чтобы закончить введите 'exit'")

    # Сохраняем состояние пользователя - ожидание ввода имени таблицы
    user_states[message.from_user.id] = "waiting_for_tb_name_add"

# Middleware для обработки ввода от пользователя
@root_router.message(lambda message: message.from_user.id in user_states and user_states[
    message.from_user.id] == "waiting_for_tb_name_add")
async def tb_name_input(message: Message):
    new_table_name = message.text.strip()

    if new_table_name.lower() == 'exit':
        # Если пользователь ввел "exit", очищаем состояние и сообщаем о выходе
        user_states.pop(message.from_user.id, None)
        await message.answer("Выход из режима ввода.")

    else:
        if conn is not None:
            try:
                # Создаем курсор для выполнения SQL-запросов
                with conn.cursor() as curs:
                    # Проверяем, существует ли таблица с таким именем
                    curs.execute(f"SHOW TABLES LIKE '{new_table_name}'")
                    table_exists = curs.fetchone()  # состояние таблицы

                    if table_exists:
                        await message.answer(f"Таблица с именем << {new_table_name} >> уже существует.\n"
                                             f"Введите другое Имя Таблицы.")
                    else:
                        # Таблица не существует, выполняем создание
                        create_table_query = f"""
                        CREATE TABLE {new_table_name} 
                        (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(255) NOT NULL
                        )
                        """
                        # Выполняем создание таблицы
                        curs.execute(create_table_query)
                        # Подтверждаем изменения в базе данных
                        conn.commit()
                        await message.answer(f"Таблица {new_table_name} создана.\n"
                                             f"Выйти из режима ввода 'exit'")

            except mysql.connector.Error as ex:
                print(f"Error in tb_list: {ex}")
        else:
            await message.answer(f"Error in tb_name_input\n {ex}")

# -------------- T.List
@root_router.message(F.text == 'T.List')
async def tb_list(message: Message):

    if conn is not None:
        try:
            with conn.cursor() as curs:
                curs.execute("SHOW TABLES")

                # Получаем результаты запроса
                tables = curs.fetchall()

                # Собираем все названия таблиц в одну строку
                table_names = "\n".join(tb[0] for tb in tables)

                # Отправляем список таблиц как одно сообщение
                await message.answer(f"List of Tables:\n{table_names}")

        except mysql.connector.Error as ex:
            print(f"Error in tb_list: {ex}")
    else:
        await message.answer(f"Error in tb_list\n {ex}")

# -------------- T.Remove
@root_router.message(F.text == 'T.Remove')
async def tb_remove(message: Message):
    print(f"{message.from_user.id} Table Remove")
    await message.answer("Введите Имя Таблицы Для Удаления\n"
                         " (или 'exit' для выхода): ")

    # Сохраняем состояние пользователя - ожидание ввода
    user_states[message.from_user.id] = "waiting_for_tb_remove_name"

# Middleware для обработки ввода от пользователя
@root_router.message(lambda message: message.from_user.id in user_states and user_states[
    message.from_user.id] == "waiting_for_tb_remove_name")
async def tb_remove_name(message: Message):
    tb_name = message.text.strip()

    if conn is not None:
        try:
            if tb_name.lower() == 'exit':
                # Если пользователь ввел "exit", очищаем состояние и сообщаем о выходе
                user_states.pop(message.from_user.id, None)
                await message.answer("Выход из режима ввода.")

            else:
                # Создаем курсор для выполнения SQL-запросов
                with conn.cursor() as curs:
                    # Проверяем, существует ли таблица с указанным именем
                    curs.execute(f"SHOW TABLES LIKE '{tb_name}'")
                    table_exists = curs.fetchone()

                    if table_exists:
                        # Таблица существует, выполним её удаление
                        curs.execute(f"DROP TABLE {tb_name}")

                        # Подтверждаем изменения в базе данных
                        conn.commit()
                        await message.answer(f"Таблица << {tb_name} >> удалена\n"
                                             f"Выйти из режима ввода 'exit'")
                        print(f"{tb_name} удалена")
                    else:
                        await message.answer(f"Таблицы << {tb_name} >> не существует")
        except mysql.connector.Error as ex:
            print(f"Error in tb_remove_name: {ex}")
    else:
        await message.answer(f"Error in tb_remove_name\n {ex}")


# -------------- PARTS --------------
# нажал клавишу Parts, ввёл имя таблицы, сразу выходит Parts List.
# должно быть так, нажал клавишу Parts, ввёл имя таблицы, и тебя переносит в меню kb_parts.
# В этом меню уже выбираешь что делать дальше.

@root_router.message(F.text == 'Parts')
async def db_parts(message: Message):
    print(f"{message.from_user.id} entered to Parts")

    await tb_list(message)

    await message.answer("Введите Имя Таблицы или введите 'exit' для выхода: ")

    # Сохраняем состояние пользователя - ожидание ввода имени таблицы
    user_states[message.from_user.id] = "waiting_for_db_table_name"


# Middleware для обработки ввода от пользователя
@root_router.message(lambda message: message.from_user.id in user_states and user_states[
    message.from_user.id] == "waiting_for_db_table_name")
async def pts_name_input(message: Message):
    tb_name = message.text.strip()

    if conn is not None:
        try:
            if tb_name.lower() == 'exit':
                # Если пользователь ввел "exit", очищаем состояние и сообщаем о выходе
                user_states.pop(message.from_user.id, None)
                await message.answer("Выход из режима ввода.")
                return

            # Создаем курсор для выполнения SQL-запросов
            with conn.cursor() as curs:
                # Проверяем, существует ли уже такая таблица
                curs.execute("""
                    SELECT EXISTS (
                        SELECT 1 
                        FROM information_schema.tables 
                        WHERE table_name = %s
                    )
                """, (tb_name,))

                table_exists = curs.fetchone()[0]

                if table_exists:
                    # Таблица существует, продолжаем работу
                    curs.execute(f"SELECT id, name FROM {tb_name}")
                    await message.answer(f"Вы открыли данные в таблице << {tb_name} >>", reply_markup=kb.parts)
                    user_states.pop(message.from_user.id, None)
                else:
                    await message.answer(f"Таблицы << {tb_name} >> не существует. Попробуйте снова.")
        except Exception as ex:
            print(f"Error in tb_remove_name: {ex}")
    else:
        await message.answer("Connection to the database is not established.")


@root_router.message(F.text == 'P.Add')
async def pts_add(message: Message):
    await message.answer("Connection to the database is not established.")

# ------
@root_router.message(F.text == 'P.List')
async def pts_list(message: Message):
    await message.answer("Connection to the database is not established.")


# ------
@root_router.message(F.text == 'P.Remove')
async def pts_remove(message: Message):
    await message.answer("Connection to the database is not established.")

# -------------- BACK

@root_router.message(F.text == 'Back')
async def db_back(message: Message):
    user_id = message.from_user.id
    main_kb = root_keyboard(user_id, root_id, maintenance_id)

    global conn

    if conn is not None:
        conn.close()
        conn = None

    print(f"{message.from_user.id} connection is closed.")
    await message.answer("...", reply_markup=main_kb)