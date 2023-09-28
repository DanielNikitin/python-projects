import psycopg2
from config import *

# pip install psycopg2-binary

try:
    # connect to exist database
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name,
    )

    cur = conn.cursor()
    print("connection ok")



except Exception as err:
    print(err)
finally:
    cur.close()
    conn.close()