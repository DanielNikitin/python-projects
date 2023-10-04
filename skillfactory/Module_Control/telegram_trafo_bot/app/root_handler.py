from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Filter

import psycopg2

from app.config import host, port, user, password

from app.keyboard import root_keyboard  # доступ к кнопке Back

import app.keyboard as kb

root_router = Router()

conn = None  # определение первоначального состояния подключения к БД

global db_name  # для использования в других функциях

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

# -------------- DATABASE

@root_router.message(F.text == 'Database Menu')
async def db_menu(message: Message):

    global db_name
    db_name = "trafo_db"  # Имя базы данных
    global conn

    await message.answer(f"Connecting to << {db_name} >> database")
    print(f"{message.from_user.id} trying connect to <<{db_name}>> database")

    # Подключение к Базе Данных
    try:
        # Connect to the default "postgres" database without starting a new transaction
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=f"{db_name}"
        )

        await message.answer("Connection to the database was successful.")
        print(f"{message.from_user.id} connection to the database was successful.")

        await message.answer("...", reply_markup=kb.database_menu)

    except Exception as ex:
        print(f"Error: {ex}")

# -------------- Database
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

    # Создаем курсор для выполнения SQL-запросов
    with conn.cursor() as curs:
        # Проверяем, существует ли уже такая база данных
        curs.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
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
                curs.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
                result = curs.fetchone()

                if result:
                    # База данных существует, выполним удаление
                    curs.execute(f"DROP DATABASE IF EXISTS {db_name}")

                    # После завершения обработки, очистите состояние пользователя
                    user_states.pop(message.from_user.id, None)

                    await message.answer(f"БД << {db_name} >> была удалена.")
                    print(f"{message.from_user.id}: БД << {db_name} >> удалена.")
                else:
                    await message.answer(f"БД << {db_name} >> не существует, попробуйте заново.")

        except Exception as ex:
                    print(f"Error in db_list: {ex}")
    else:
        await message.answer("Connection to the database is not established.")

# -------------- D.List
@root_router.message(F.text == 'D.List')
async def db_list(message: Message):
    print(f"{message.from_user.id} List")

    if conn is not None:
        try:
            with conn.cursor() as curs:
                curs.execute("SELECT datname FROM pg_database")
                databases = curs.fetchall()
                for db in databases:
                    print(db[0])
                await message.answer("List of Databases:\n" + "\n".join(db[0] for db in databases))
        except Exception as ex:
            print(f"Error in db_list: {ex}")
    else:
        await message.answer("Connection to the database is not established.")

# -------------- TABLE

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
    input_text = message.text.strip()

    if input_text.lower() == 'exit':
        # Если пользователь ввел "exit", очищаем состояние и сообщаем о выходе
        user_states.pop(message.from_user.id, None)
        await message.answer("Выход из режима ввода.")
    else:
        if conn is not None:
            try:
                # Создаем курсор для выполнения SQL-запросов
                with conn.cursor() as curs:
                    # Проверяем, существует ли таблица с таким именем
                    curs.execute("""
                        SELECT table_name FROM information_schema.tables
                        WHERE table_schema = 'public' AND table_name = %s
                    """, (input_text,))
                    table_exists = curs.fetchone()  # состояние таблицы

                    if table_exists:
                        await message.answer(f"Таблица с именем << {input_text} >> уже существует.\n"
                                             f"Введите другое Имя Таблицы.")
                    else:
                        # Таблица не существует, выполняем создание
                        curs.execute(f"""
                            CREATE TABLE IF NOT EXISTS {input_text} (
                                id SERIAL PRIMARY KEY,
                                name VARCHAR(255) NOT NULL
                            )""")

                        # Подтверждаем изменения в базе данных
                        conn.commit()
                        await message.answer(f"Таблица {input_text} создана.\n"
                                             f"Выйти из режима ввода 'exit'")

            except Exception as ex:
                print(f"Error in tb_list: {ex}")
        else:
            await message.answer("Connection to the database is not established.")

# -------------- T.List
@root_router.message(F.text == 'T.List')
async def tb_list(message: Message):

    if conn is not None:
        try:
            with conn.cursor() as curs:
                curs.execute("""
                    SELECT table_name FROM information_schema.tables
                    WHERE table_schema = 'public'
                """)

                # Получаем результаты запроса
                tables = curs.fetchall()

                # Собираем все названия таблиц в одну строку
                table_names = "\n".join(tb[0] for tb in tables)

                # Отправляем список таблиц как одно сообщение
                await message.answer(f"List of Tables:\n{table_names}")

        except Exception as ex:
            print(f"Error in tb_list: {ex}")
    else:
        await message.answer("Connection to the database is not established.")

# -------------- T.Remove
@root_router.message(F.text == 'T.Remove')
async def tb_remove(message: Message):
    print(f"{message.from_user.id} Table Remove")
    await message.answer("Введите Имя Таблицы Для Удаления (или 'exit' для выхода): ")

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
                    curs.execute("""
                        SELECT table_name FROM information_schema.tables
                        WHERE table_schema = 'public' AND table_name = %s
                    """, (tb_name,))
                    table_exists = curs.fetchone()

                    if table_exists:
                        # Таблица существует, выполним её удаление
                        curs.execute(f"DROP TABLE IF EXISTS {tb_name}")

                        # Подтверждаем изменения в базе данных
                        conn.commit()
                        await message.answer(f"Таблица << {tb_name} >> удалена\n"
                                             f"Выйти из режима ввода 'exit'")
                        print(f"{tb_name} удалена")
                    else:
                        await message.answer(f"Таблицы << {tb_name} >> не существует")
        except Exception as ex:
            print(f"Error in tb_remove_name: {ex}")
    else:
        await message.answer("Connection to the database is not established.")


# -------------- PARTS
# нажал клавишу Parts, ввёл имя таблицы, сразу выходит Parts List.
# должно быть так, нажал клавишу Parts, ввёл имя таблицы, и тебя переносит в меню kb_parts.
# В этом меню уже выбираешь что делать дальше.

@root_router.message(F.text == 'Parts')
async def db_parts(message: Message):
    print(f"{message.from_user.id} entered to Parts")
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