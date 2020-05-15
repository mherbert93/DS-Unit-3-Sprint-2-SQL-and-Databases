import psycopg2
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("DB_NAME", default="OOPS")
DB_USER = os.getenv("DB_USER", default="OOPS")
DB_PW = os.getenv("DB_PW", default="OOPS")
DB_HOST = os.getenv("DB_HOST", default="OOPS")

pg_conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER,
    password=DB_PW, host=DB_HOST
)
pg_curs = pg_conn.cursor()

query = """SELECT 
	SUM(CASE when "Survived" = 0 THEN 1 else 0 END) as total_dead,
	SUM(CASE when "Survived" = 1 THEN 1 else 0 END) as total_alive,
	SUM(CASE when "Pclass" = 1 THEN 1 else 0 END) as FirstClass,
	SUM(CASE when "Pclass" = 2 THEN 1 else 0 END) as SecondClass,
	SUM(CASE when "Pclass" = 3 THEN 1 else 0 END) as ThirdClass
FROM 
	titanic_test"""

pg_curs.execute(query)
result = pg_curs.fetchall()

queries = {"Total dead: ": result[0][0], "Total alive: ": result[0][1], "First class passengers: ": result[0][2],
           "Second class passengers: ": result[0][3], "Third class passengers: ": result[0][4]}

query = '''
SELECT 
	SUM(CASE when "Survived" = 0 THEN 1 else 0 END) as total_dead,
	SUM(CASE when "Survived" = 1 THEN 1 else 0 END) as total_alive
FROM 
	titanic_test
GROUP BY
	"Pclass"
ORDER BY
	"Pclass"'''

pg_curs.execute(query)
result = pg_curs.fetchall()

queries.update({"--------------------\nFirst class dead": result[0][0],
                "Second class dead: ": result[1][0],
                "Third class dead: ": result[2][0],
                "First class alive: ": result[0][1],
                "Second class alive: ": result[1][1],
                "Third class alive: ": result[2][1]})

query = '''SELECT avg("Age"), "Survived" FROM titanic_test GROUP BY "Survived"'''  # included survived column to see where
# the average was mapped to. Including
# to show work.

pg_curs.execute(query)
result = pg_curs.fetchall()

queries.update({"--------------------\nAverage age of dead": result[0][0],
                "Average age of survived: ": result[1][0]})

query = '''SELECT avg("Age"), avg("Fare") FROM titanic_test GROUP BY "Pclass" ORDER BY "Pclass"'''

pg_curs.execute(query)
result = pg_curs.fetchall()

queries.update({"--------------------\nFirst class average age": result[0][0],
                "Second class average age: ": result[1][0], "Third class average age: ": result[2][0],
                "--------------------\nFirst class average fare: ": result[0][1],
                "Second class average fare: ": result[1][1],
                "Third class average fare: ": result[2][1]})

query = '''SELECT avg("Fare") FROM titanic_test GROUP BY "Survived" ORDER BY "Survived"'''

pg_curs.execute(query)
result = pg_curs.fetchall()

queries.update({"Average fare of dead": result[0][0],
                "Average fare of survived: ": result[1][0]})

query = '''
SELECT
	avg("Siblings/Spouses Aboard"),
	avg("Parents/Children Aboard")
FROM
	titanic_test
GROUP BY
	"Pclass"
ORDER BY
	"Pclass"'''

pg_curs.execute(query)
result = pg_curs.fetchall()

queries.update({"--------------------\nFirst class average siblings/spouses aboard": result[0][0],
                "Second class average siblings/spouses aboard: ": result[1][0],
                "Third class average siblings/spouses aboard: ": result[2][0],
                "--------------------\nFirst class average parents/children aboard: ": result[0][1],
                "Second class average parents/children aboard: ": result[1][1],
                "Third class average parents/children aboard: ": result[2][1]})

query = '''
SELECT
	avg("Siblings/Spouses Aboard"),
	avg("Parents/Children Aboard")
FROM
	titanic_test
GROUP BY
	"Survived"
ORDER BY
	"Survived"'''

pg_curs.execute(query)
result = pg_curs.fetchall()

queries.update({"--------------------\nAverage siblings/spouses aboard for passengers who died:": result[0][0],
                "Average siblings/spouses aboard for passengers who lived: ": result[1][0],
                "--------------------\nAverage parents/children aboard for passengers who died: ": result[0][1],
                "Average parents/children aboard for passengers who lived: ": result[1][1]})

query = '''SELECT count(*) - count(distinct "Name") as non_unique_names FROM titanic_test'''

pg_curs.execute(query)
result = pg_curs.fetchall()

queries.update({"--------------------\nNon-Unique names: ": result[0][0]})

for key, value in queries.items():  # print query results, with key being the description text, and value being the result
    print(key,
          value)  # For this query we print values side by side, so description text is split between the key and value

pg_curs.close()
pg_conn.close()
