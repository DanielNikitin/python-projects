# ALTER USER 'root'@'localhost' IDENTIFIED WITH 'mysql_native_password' BY '123456';  # ПУСТОЙ ПАРОЛЬ
# mysql -u root -p

import mysql.connector
#from config import *

conn = None

db_name = input("Введите имя БД: ")

# Устанавливаем соединение с базой данных
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database=f'{db_name}'
    )
    print(f"Соединение с << {db_name} >> установлено.")

    # -------------------------------- USER
    def input_jig():
        jig_name = input("Введите имя jig: ")
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM jigs WHERE name = %s", (jig_name,))
                count = cursor.fetchone()[0]

                if count > 0:
                    print(f"{jig_name} существует.")
                else:
                    print(f"{jig_name} не существует в базе данных.")
        except mysql.connector.Error as ex:
            print(f"Ошибка: {ex}")

    #input_jig()

    # -------------------------------- SCHEME
    def db_scheme():
        try:
            with conn.cursor() as cursor:
                cursor.execute("SHOW SCHEMAS")
                schemas = cursor.fetchall()

                print("Список схем в базе данных:")
                for schema in schemas:
                    print(schema[0])
        except mysql.connector.Error as ex:
            print(f"Ошибка: {ex}")

    #db_scheme()

    # --------------------------------  PARTS
    def db_add_part():
        table_name = input("Введите имя таблицы: ")
        while True:
            detail_name = input("Введите имя детали (или 'exit' для выхода): ")

            if detail_name.lower() == 'exit':
                break

            try:
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE name = %s", (detail_name,))
                    count = cursor.fetchone()[0]

                    if count > 0:
                        print(f"Деталь '{detail_name}' уже имеется в таблице '{table_name}'.")
                    else:
                        cursor.execute(f"INSERT INTO {table_name} (name) VALUES (%s) RETURNING id", (detail_name,))
                        detail_id = cursor.fetchone()[0]
                        conn.commit()
                        print(
                            f"Деталь '{detail_name}' была успешно добавлена в таблицу '{table_name}' с id = {detail_id}.")

                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT name FROM {table_name}")
                    all_details = cursor.fetchall()

                    if all_details:
                        print("Список всех деталей в таблице:")
                        for detail in all_details:
                            print(detail[0])

            except mysql.connector.Error as ex:
                print(f"Ошибка: {ex}")

    db_add_part()

    def db_list_parts():
        table_name = input("Введите имя таблицы: ")
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT id, name FROM {table_name}")
                all_details = cursor.fetchall()
                if all_details:
                    print(f"Список всех деталей в таблице {table_name}:")
                    for detail in all_details:
                        detail_id, detail_name = detail[0], detail[1]
                        print(f"ID: {detail_id}, Имя: {detail_name}")
        except mysql.connector.Error as ex:
            print(f"Ошибка: {ex}")

    #db_list_parts()

    # -------------------------------- TABLE
    def db_list_table():
        try:
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()

                print(f"Список таблиц в {db_name}:")
                for table in tables:
                    print(table[0])
        except mysql.connector.Error as ex:
            print(f"Ошибка: {ex}")

    #db_list_table()

    # -------------------------------- DATABASE
    def db_add():
        new_db_name = input("Введите имя новой базы данных: ")
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE {new_db_name}")
                print(f"База данных '{new_db_name}' успешно создана.")
        except mysql.connector.Error as ex:
            print(f"Ошибка: {ex}")

    #db_add()

    def db_delete():
        db_to_delete = input("Введите имя базы данных для удаления: ")
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"DROP DATABASE IF EXISTS {db_to_delete}")
                print(f"База данных {db_to_delete} была успешно удалена.")
        except mysql.connector.Error as ex:
            print(f"Ошибка: {ex}")

    #db_delete()

    def db_list():
        try:
            with conn.cursor() as cursor:
                cursor.execute("SHOW DATABASES")
                databases = cursor.fetchall()

                print("Список всех баз данных:")
                for db in databases:
                    print(db[0])
        except mysql.connector.Error as ex:
            print(f"Ошибка: {ex}")

    #db_list()

except Exception as ex:
    print(f"Ошибка при подключении к базе данных: {ex}")