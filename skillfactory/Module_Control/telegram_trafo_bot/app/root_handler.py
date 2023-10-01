from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Filter

import psycopg2

from app.config import host, port, user, password

from app.keyboard import root_keyboard  # доступ к кнопке Back

import app.keyboard as kb

root_router = Router()

conn = None

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
        conn.set_isolation_level(0)  # Устанавливаем уровень изоляции

        await message.answer("Connection to the database was successful.")
        print(f"{message.from_user.id} connection to the database was successful.")

        await message.answer("...", reply_markup=kb.database_menu)

    except Exception as ex:
        print(f"Error: {ex}")

# ---------
@root_router.message(F.text == 'Database')
async def database(message: Message):
    print(f"{message.from_user.id} entered to Database")
    await message.answer("...", reply_markup=kb.database)

@root_router.message(F.text == 'Add')
async def db_add(message: Message):
    print(f"{message.from_user.id} Add")
    await message.answer("Введите Имя БД Для Добавления: ")

    # Сохраняем состояние пользователя - ожидание ввода имени базы данных
    user_states[message.from_user.id] = "waiting_for_db_name_add"

# Middleware для обработки ввода от пользователя
@root_router.message(lambda message: message.from_user.id in user_states and user_states[message.from_user.id] == "waiting_for_db_name_add")
async def process_db_name_add(message: Message):
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

#-----
@root_router.message(F.text == 'Remove')
async def db_remove(message: Message):
    print(f"{message.from_user.id} Remove")
    await message.answer("Введите Имя БД для Удаления: ")

    # Сохраняем состояние пользователя - ожидание ввода имени базы данных
    user_states[message.from_user.id] = "waiting_for_db_name"

# Middleware для обработки ввода от пользователя
@root_router.message(lambda message: message.from_user.id in user_states and user_states[message.from_user.id] == "waiting_for_db_name")
async def process_db_name(message: Message):
    db_name = message.text.strip()

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

            await message.answer(f"БД << {db_name} >> была успешно удалена.")
            print(f"{message.from_user.id}: БД << {db_name} >> удалена.")
        else:
            await message.answer(f"БД << {db_name} >> не существует, попробуйте заново.")
#-----

@root_router.message(F.text == 'List')
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
    await message.answer("...", reply_markup=kb.table)

# -------------- PARTS

@root_router.message(F.text == 'Parts')
async def db_parts(message: Message):
    await message.answer("...", reply_markup=kb.parts)

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
