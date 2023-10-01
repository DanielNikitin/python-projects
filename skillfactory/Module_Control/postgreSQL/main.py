import asyncio
import aiomysql
import pymysql

async def create_table(pool, table_name):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT
            )
            """
            await cur.execute(create_table_query)
            print(f"Таблица '{table_name}' успешно создана")

async def list_tables(pool):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SHOW TABLES")
            tables = await cur.fetchall()
            print("Список таблиц в базе данных:")
            for table in tables:
                print(table[0])

async def create_database(conn, database_name):
    async with conn.cursor() as cur:
        create_database_query = f"CREATE DATABASE IF NOT EXISTS {database_name}"
        await cur.execute(create_database_query)
        print(f"База данных '{database_name}' успешно создана")

async def delete_database(conn, database_name):
    async with conn.cursor() as cur:
        delete_database_query = f"DROP DATABASE IF EXISTS {database_name}"
        await cur.execute(delete_database_query)
        print(f"База данных '{database_name}' успешно удалена")

async def list_databases(conn):
    async with conn.cursor() as cur:
        await cur.execute("SHOW DATABASES")
        databases = await cur.fetchall()
        print("Список баз данных:")
        for database in databases:
            print(database[0])

async def delete_table(conn, table_name):
    async with conn.cursor() as cur:
        delete_table_query = f"DROP TABLE IF EXISTS {table_name}"
        await cur.execute(delete_table_query)
        print(f"Таблица '{table_name}' успешно удалена")

async def select_database(conn, database_name):
    await conn.select_db(database_name)
    print(f"Выбрана база данных '{database_name}'")

async def main():
    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '123321aA!',
        'db': 'trafo_db',
    }

    try:
        conn = await aiomysql.connect(**db_config)
        print("Подключение к базе данных успешно!")

        while True:
            print("Выберите действие:")
            print("1. Создать таблицу")
            print("2. Вывести список таблиц")
            print("3. Создать базу данных")
            print("4. Удалить базу данных")
            print("5. Список Баз Данных")
            print("6. Удалить Таблицу")
            print("7. Выбрать Базу Данных")
            print("8. Выйти")
            choice = input("Введите номер действия: ")

            if choice == '1':
                table_name = input("Введите имя таблицы: ")
                await create_table(conn, table_name)
            elif choice == '2':
                await list_tables(conn)
            elif choice == '3':
                database_name = input("Введите имя базы данных: ")
                await create_database(conn, database_name)
            elif choice == '4':
                database_name = input("Введите имя базы данных для удаления: ")
                await delete_database(conn, database_name)
            elif choice == '5':
                await list_databases(conn)
            elif choice == '6':
                table_name = input("Введите имя таблицы для удаления: ")
                await delete_table(conn, table_name)
            elif choice == '7':
                database_name = input("Введите имя базы данных для выбора: ")
                await select_database(conn, database_name)
            elif choice == '8':
                conn.close()
                await conn.wait_closed()
                break
            else:
                print("Неверный выбор. Пожалуйста, выберите действие 1, 2, 3, 4, 5, 6, 7 или 8.")
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")


if __name__ == '__main__':
    asyncio.run(main())