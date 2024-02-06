from os import getenv
from dotenv import load_dotenv
import psycopg2

load_dotenv()

HOST = getenv('host')
DATABASE = getenv('database')
USER = getenv('user')
PASSWORD = getenv('password')

connection = psycopg2.connect(
    host = HOST,
    database = DATABASE,
    user = USER,
    password = PASSWORD
)

cursor = connection.cursor()

def update_crm(dataframe):

    cursor.execute("DELETE FROM crm;")

    create_table_query = f"CREATE TABLE IF NOT EXISTS crm ("
    for coluna in dataframe.columns:
        create_table_query += f"{coluna.replace(' ', '_')} TEXT,"
    create_table_query = create_table_query[:-1] + ");"

    cursor.execute(create_table_query)

    for _indice, linha in dataframe.iterrows():
        cursor.execute(f"INSERT INTO crm VALUES (%s);" % ','.join("'" + str(x) + "'" for x in linha))

    connection.commit()

    cursor.close()
