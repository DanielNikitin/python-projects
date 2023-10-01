from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Filter

import psycopg2

from app.config import host, port, user, password

import app.keyboard as kb

maint_router = Router()

conn = None

# Словари
chat_data = {}
user_states = {}

# Список Maintenance Group
maintenance_id = [1035107072, # Daniel
                  103200201   # Dima
                 ]

#                     MAINTENANCE                      #
#  **************************************************  #

class Maintenance(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in maintenance_id

@maint_router.message(Maintenance(), F.text == 'Maintenance')
async def maint_menu(message: Message):
    await message.answer('Maintenance Status :: [OK]')

    db_name = "trafo_db"  # Имя базы данных
    global conn

    await message.answer(f"Connecting to << {db_name} >>")
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
        conn.set_isolation_level(0)  # Устанавливаем уровень изоляции / без него нет доступа к бд

        await message.answer("Connection to the database was successful.")
        print(f"{message.from_user.id} connection to the database was successful.")

        await message.answer("...", reply_markup=kb.maintenance)

    except Exception as ex:
        print(f"Error: {ex}")

# -------------- Jig Calibration

@maint_router.message(F.text == 'Jig Calibration')
async def jig_calib(message: Message):
    await message.answer("...", reply_markup=kb.jig)

# -------- Ввести модель JIG

@maint_router.message(F.text == 'Ввести Модель Шаблона')
async def input_jig(message: Message):
    print(f"{message.from_user.id} Input JIG name")
    await message.answer(":: Введите Модель Шаблона или отправьте 'exit' для выхода: ")

    # Сохраняем состояние пользователя - ожидание ввода имени шаблона
    user_states[message.from_user.id] = "waiting_for_input_jig_name"

# Middleware для обработки ввода от пользователя
@maint_router.message(lambda message: message.from_user.id in user_states and user_states[message.from_user.id] == "waiting_for_input_jig_name")
async def db_jig_name(message: Message):
    jig_name = message.text.strip()

    # Если пользователь ввел "exit", завершаем состояние и выходим из функции
    if jig_name.lower() == 'exit':
        await message.answer(":: Вы вышли из режима Ввода.")
        user_states.pop(message.from_user.id, None)
        return

    # Создаем курсор для выполнения SQL-запросов
    with conn.cursor() as curs:
        # Выполняем SQL-запрос для проверки наличия имени "jig" в таблице
        curs.execute("SELECT COUNT(*) FROM jigs WHERE name = %s", (jig_name,))
        count = curs.fetchone()[0]

        if count > 0:
            await message.answer(f":: {jig_name} существует.")
        else:
            await message.answer(f":: {jig_name} не существует в базе данных.")

# -------- Список рабочих мест

@maint_router.message(F.text == 'Список Рабочих Мест')
async def list_places(message: Message):
    table_name = "wps"

    # Создаем курсор для выполнения SQL-запросов
    with conn.cursor() as curs:
        # Выводим список всех рабочих мест в таблице
        curs.execute(f"SELECT id, name FROM {table_name}")
        all_details = curs.fetchall()

        if all_details:
            wps_list_message = ":: Список Рабочих мест:\n"
            for detail in all_details:
                detail_id, detail_name = detail[0], detail[1]
                wps_list_message += f":: {detail_name}\n"

            # Определяем количество рабочих мест
            num_places = len(all_details)

            # Добавляем информацию о количестве рабочих мест в сообщение
            wps_list_message += f"\n:: Количество рабочих мест: {num_places}"

            # Отправляем список рабочих мест в чат
            await message.answer(wps_list_message)
        else:
            await message.answer(":: В базе данных нет рабочих мест.")

# -------- Список JIG

@maint_router.message(F.text == 'Список Шаблонов')
async def jig_list(message: Message):
    table_name = "jigs"

    # Создаем курсор для выполнения SQL-запросов
    with conn.cursor() as curs:
        # Выводим список всех деталей в таблице
        curs.execute(f"SELECT id, name FROM {table_name}")
        all_details = curs.fetchall()

        if all_details:
            jig_list_message = ":: Список Шаблонов:\n"
            for jig in all_details:
                jig_id, jig_name = jig[0], jig[1]
                jig_list_message += f":: {jig_name}\n"

            # Определяем количество рабочих мест
            num_jigs = len(all_details)

            # Добавляем информацию о количестве рабочих мест в сообщение
            jig_list_message += f"\n:: Количество шаблонов: {num_jigs}"

            # Отправляем список JIGs в чат
            await message.answer(jig_list_message)
        else:
            await message.answer(":: В БД нет такого шаблона.")

# -------- Чертежи

@maint_router.message(F.text == 'Чертежи')
async def jig_blueprint(message: Message):
    await message.answer("Чертежи")

# -------- Инструкция

@maint_router.message(F.text == 'Инструкция')
async def show_instruction(message: Message):

    message_instr = (
        '** Руководство По Использованию **\n'
        '👉🏻 Т\n'
        '👉🏻 Ы\n'
        '👉🏻 П\n'
        '👉🏻 Е\n'
        '👉🏻 Т\n'
        '👉🏻 У\n'
        '👉🏻 Х'
    )
    await message.answer(message_instr)