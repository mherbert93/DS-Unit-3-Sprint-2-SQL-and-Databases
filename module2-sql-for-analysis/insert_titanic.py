import psycopg2
import sqlite3
import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PW = os.getenv("DB_PW")
DB_HOST = os.getenv("DB_HOST")
DB_URL = os.getenv("DB_URL")

df = pd.read_csv('titanic.csv')

alchemyEngine = create_engine(DB_URL)

postgreSQLConnection = alchemyEngine.connect()
df.to_sql('titanic_test', postgreSQLConnection, if_exists='fail')

postgreSQLConnection.close()

pg_conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER,
    password=DB_PW, host=DB_HOST
    )
pg_curs = pg_conn.cursor()

query = """SELECT 
	SUM(CASE when "Survived" = 0 THEN 1 else 0 END) as dead,
	SUM(CASE when "Survived" = 1 THEN 1 else 0 END) as alive
FROM 
	titanic_test"""

pg_curs.execute(query)
result = pg_curs.fetchall()

print("Passengers dead: ", result[0][0])
print("Passengers survived: ", result[0][1])

pg_curs.close()
pg_conn.close()