import psycopg2
from app.config import *

conn = None

db_name = input("Введите имя БД: ")

# Connect to the default "postgres" database without starting a new transaction
conn = psycopg2.connect(
    host=host,
    port="5432",
    user=user,
    password=password,
    database=f"{db_name}"
)
print("Connection to the database was successful.")

try:
# -------------------------------- USER
    def input_jig():
        # Получаем имя "jig" через input
        jig_name = input("Введите имя jig: ")

        # Создаем курсор для выполнения SQL-запросов
        with conn.cursor() as curs:
            # Выполняем SQL-запрос для проверки наличия имени "jig" в таблице
            curs.execute("SELECT COUNT(*) FROM jigs WHERE name = %s", (jig_name,))
            count = curs.fetchone()[0]

            if count > 0:
                print(f"{jig_name} существует.")
            else:
                print(f"{jig_name} не существует в базе данных.")

    #input_jig()
# -------------------------------- SCHEME
    def db_scheme():
        # Создаем курсор для выполнения SQL-запросов
        with conn.cursor() as curs:
            # Выполняем SQL-запрос для получения списка схем
            curs.execute("""
                SELECT schema_name
                FROM information_schema.schemata;
            """)

            # Получаем результаты запроса
            schemas = curs.fetchall()

            # Выводим список схем
            print("Список схем в базе данных:")
            for schema in schemas:
                print(schema[0])

    #db_scheme()
# --------------------------------  PARTS
    def db_list_parts():
        table_name = input("Введите имя таблицы: ")
        # Создаем курсор для выполнения SQL-запросов
        with conn.cursor() as curs:
            # Выводим список всех деталей в таблице
            curs.execute(f"SELECT id, name FROM {table_name}")
            all_details = curs.fetchall()
            if all_details:
                print(f"Список всех деталей в таблице {table_name}:")
                for detail in all_details:
                    detail_id, detail_name = detail[0], detail[1]
                    print(f"ID: {detail_id}, Имя: {detail_name}")

    #db_list_parts()

    def db_add_part():
        # Получаем имя таблицы, в которую нужно добавить деталь, и имя детали через input
        table_name = input("Введите имя таблицы: ")
        while True:
            # Получаем имя детали через input
            detail_name = input("Введите имя детали (или 'exit' для выхода): ")

            if detail_name.lower() == 'exit':
                break  # Выход из цикла при вводе 'exit'

            # Создаем курсор для выполнения SQL-запросов
            with conn.cursor() as curs:
                # Проверяем, есть ли уже такая деталь в таблице
                curs.execute(f"SELECT COUNT(*) FROM {table_name} WHERE name = %s", (detail_name,))
                count = curs.fetchone()[0]

                if count > 0:
                    print(f"Деталь '{detail_name}' уже имеется в таблице '{table_name}'.")
                else:
                    # Если детали нет в таблице, выполняем SQL-запрос для вставки
                    curs.execute(f"INSERT INTO {table_name} (name) VALUES (%s) RETURNING id", (detail_name,))
                    detail_id = curs.fetchone()[0]

                    # Подтверждаем изменения в базе данных
                    conn.commit()
                    print(f"Деталь '{detail_name}' была успешно добавлена в таблицу '{table_name}' с id = {detail_id}.")

            # Выводим список всех деталей в таблице
            with conn.cursor() as curs:
                curs.execute(f"SELECT name FROM {table_name}")
                all_details = curs.fetchall()

                if all_details:
                    print("Список всех деталей в таблице:")
                    for detail in all_details:
                        print(detail[0])

    #db_add_part()

    def db_remove_part():
        db_list_parts()
        # Получаем имя таблицы и ID детали, которую нужно удалить, через input
        table_name = input("Введите имя таблицы: ")
        while True:
            detail_id = input("Введите ID детали для удаления (или 'exit' для выхода): ")

            if detail_id.lower() == 'exit':
                break  # Выход из цикла при вводе 'exit'

            # Создаем курсор для выполнения SQL-запросов
            with conn.cursor() as curs:
                # Проверяем, есть ли деталь с указанным ID в таблице
                curs.execute(f"SELECT COUNT(*) FROM {table_name} WHERE id = %s", (detail_id,))
                count = curs.fetchone()[0]

                if count == 0:
                    print(f"Деталь с ID '{detail_id}' не найдена в таблице '{table_name}'.")
                else:
                    # Если деталь существует, выполняем SQL-запрос для удаления
                    curs.execute(f"DELETE FROM {table_name} WHERE id = %s", (detail_id,))
                    # Подтверждаем изменения в базе данных
                    conn.commit()
                    print(f"Деталь с ID '{detail_id}' была успешно удалена из таблицы '{table_name}'.")

                # Выводим обновленный список всех деталей в таблице
                curs.execute(f"SELECT id, name FROM {table_name}")
                all_details = curs.fetchall()
                if all_details:
                    print("Список всех деталей в таблице после удаления:")
                    for detail in all_details:
                        detail_id, detail_name = detail[0], detail[1]
                        print(f"ID: {detail_id}, Имя: {detail_name}")

    #db_remove_part()
# --------------------------------  TABLE
    def db_list_table():
        # Создаем курсор для выполнения SQL-запросов
        with conn.cursor() as curs:
            # Выполняем SQL-запрос для получения списка таблиц в схеме 'public'
            curs.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """)

            # Получаем результаты запроса
            tables = curs.fetchall()

            # Выводим список таблиц
            print(f"Список таблиц в {db_name}:")
            for table in tables:
                print(table[0])

    #db_list_table()

    def db_add_table():
        # Получаем имя таблицы, которую вы хотите создать, с помощью input
        table_name = input("Введите имя таблицы: ")

        # Создаем курсор для выполнения SQL-запросов
        with conn.cursor() as curs:
            # Выполняем SQL-запрос для создания таблицы с введенным именем
            curs.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                )""")

            # Подтверждаем изменения в базе данных
            conn.commit()
        print(f"Таблица {table_name} была успешно создана.")

    #db_add_table()

    def db_remove_table():
        # Получаем имя таблицы, которую нужно удалить
        table_name = input("Введите имя таблицы для удаления: ")

        # Создаем курсор для выполнения SQL-запросов
        with conn.cursor() as curs:
            # Выполняем SQL-запрос для удаления таблицы
            curs.execute(f"DROP TABLE IF EXISTS {table_name}")

            # Подтверждаем изменения в базе данных
            conn.commit()

        print(f"Таблица {table_name} была успешно удалена.")

    #db_remove_table()
    #db_list_table()
# -------------------------------- DATABASE
    def db_delete():
        # Получаем имя базы данных, которое вы хотите удалить, с помощью input
        db_to_delete = input("Введите имя базы данных для удаления: ")

        # Создаем курсор для выполнения SQL-запросов
        with conn.cursor() as curs:
            # Выполняем SQL-запрос для удаления базы данных
            curs.execute(f"DROP DATABASE IF EXISTS {db_to_delete}")

        print(f"База данных {db_to_delete} была успешно удалена.")

    #db_delete()

    def db_list():
        # Создаем курсор для выполнения SQL-запросов
        with conn.cursor() as curs:
            # Выполняем SQL-запрос для получения списка всех баз данных
            curs.execute("SELECT datname FROM pg_database")

            # Получаем результаты запроса
            databases = curs.fetchall()

            # Выводим список всех баз данных
            for db in databases:
                print(db[0])  # db[0] содержит имя базы данных

    #db_list()

# --------------------------------

except Exception as ex:
    print(f"Error: {ex}")
finally:
    if conn is not None:
        conn.close()