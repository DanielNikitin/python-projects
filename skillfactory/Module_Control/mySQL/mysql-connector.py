# 5.42.78.98
# XM8HC5etpUZn

# daniel.nikitin@tptlive.ee
# FP@)OFhYa@@C

# ALTER USER 'root'@'localhost' IDENTIFIED WITH 'mysql_native_password' BY '123456';  # ПУСТОЙ ПАРОЛЬ
# mysql -u root -p

# pip install mysql-connector-python

import mysql.connector
#from config import *

conn = None

db_name = "trafo_db"

# Устанавливаем соединение с базой данных
try:
    conn = mysql.connector.connect(
        host='localhost',
        port='3306',
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

    # --------------------------------  PARTS
    def db_add_part():
        table_name = input("Введите имя таблицы, в которую хотите добавить деталь: ")
        detail_name = input("Введите имя детали: ")

        try:
            with conn.cursor() as cursor:
                # Проверяем, существует ли указанная таблица
                cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
                exists = cursor.fetchone()

                if not exists:
                    print(f"Таблицы '{table_name}' не существует.")
                    return

                # Проверяем, есть ли уже такая деталь в таблице
                cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE name = %s", (detail_name,))
                count = cursor.fetchone()[0]

                if count > 0:
                    print(f"Деталь '{detail_name}' уже имеется в таблице '{table_name}'.")
                else:
                    # Если детали нет в таблице, выполняем SQL-запрос для вставки
                    cursor.execute(f"INSERT INTO {table_name} (name) VALUES (%s)", (detail_name,))
                    conn.commit()
                    print(f"Деталь '{detail_name}' успешно добавлена в таблицу '{table_name}'.")

        except mysql.connector.Error as ex:
            print(f"Ошибка: {ex}")

    #db_add_part()

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

    def db_delete_detail():
        table_name = input("Введите имя таблицы, из которой хотите удалить деталь: ")
        detail_name = input("Введите имя детали, которую хотите удалить: ")

        try:
            with conn.cursor() as cursor:
                # Проверяем, существует ли указанная таблица
                cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
                table_exists = cursor.fetchone()

                if not table_exists:
                    print(f"Таблицы '{table_name}' не существует.")
                    return

                # Проверяем, существует ли указанная деталь в таблице
                cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE name = %s", (detail_name,))
                detail_count = cursor.fetchone()[0]

                if detail_count == 0:
                    print(f"Детали '{detail_name}' не существует в таблице '{table_name}'.")
                    return

                # Удаляем деталь из таблицы
                cursor.execute(f"DELETE FROM {table_name} WHERE name = %s", (detail_name,))
                conn.commit()
                print(f"Деталь '{detail_name}' успешно удалена из таблицы '{table_name}'.")

        except mysql.connector.Error as ex:
            print(f"Ошибка: {ex}")

    # db_delete_detail()

    # -------------------------------- TABLE
    def db_add_table():
        new_table_name = input("Введите имя новой таблицы: ")
        try:
            with conn.cursor() as cursor:
                # Проверяем, существует ли уже такая таблица
                cursor.execute(f"SHOW TABLES LIKE '{new_table_name}'")
                exists = cursor.fetchone()

                if exists:
                    print(f"Таблица '{new_table_name}' уже существует.")
                else:
                    # Создаем новую таблицу
                    create_table_query = f"""
                    CREATE TABLE {new_table_name} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL
                    )
                    """
                    cursor.execute(create_table_query)
                    conn.commit()
                    print(f"Таблица '{new_table_name}' создана.")

        except mysql.connector.Error as ex:
            print(f"Ошибка: {ex}")

    #db_add_table()

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

    db_list_table()

    def db_delete_table():
        table_name = input("Введите имя таблицы, которую хотите удалить: ")

        try:
            with conn.cursor() as cursor:
                # Проверяем, существует ли указанная таблица
                cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
                exists = cursor.fetchone()

                if not exists:
                    print(f"Таблицы '{table_name}' не существует.")
                    return

                # Удаляем таблицу
                cursor.execute(f"DROP TABLE {table_name}")
                conn.commit()
                print(f"Таблица '{table_name}' успешно удалена.")

        except mysql.connector.Error as ex:
            print(f"Ошибка: {ex}")

    #db_delete_table()

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
                # Проверяем, существует ли указанная база данных
                cursor.execute(f"SHOW DATABASES LIKE '{db_to_delete}'")
                exists = cursor.fetchone()

                if not exists:
                    print(f"Базы данных '{db_to_delete}' не существует.")
                    return

                # Удаляем базу данных
                cursor.execute(f"DROP DATABASE {db_to_delete}")
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