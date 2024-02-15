import pymysql

from config import host, user, password, db_name

conn = None

try:
    conn = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print(f"connect to {db_name} success")
    print("#" * 15)

    def create_table():
        table_name = input("Введите имя БД: ")
        with conn.cursor() as cursor:
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                                id SERIAL PRIMARY KEY,
                                name VARCHAR(255) NOT NULL)""")

        print(f"Таблица {table_name} была успешно создана.")

    #create_table()

    def list_table():
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()

            if tables:
                print(f"Tables in {db_name}:")
                for table in tables:
                    print(table["Tables_in_" + db_name])
            else:
                print(f"No tables found in {db_name}")

    list_table()

    def delete_table():
        delete_name = input("Введите имя таблицы: ")
        with conn.cursor() as cursor:
            drop_table = f"DROP TABLE IF EXISTS {delete_name};"
            cursor.execute(drop_table)

        print(f"Таблица {delete_name} была удалена.")

    delete_table()
    list_table()

except Exception as ex:
    print(ex)
finally:
    if conn is not None:
        print("connection is closed")
        conn.close()
