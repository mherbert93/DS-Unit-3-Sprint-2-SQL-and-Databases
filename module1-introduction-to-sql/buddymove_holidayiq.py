import pandas as pd
import sqlite3

df = pd.read_csv('buddymove_holidayiq.csv')

df.rename({'User Id': 'User_Id'}, axis='columns', inplace=True)
df.set_index('User_Id', inplace=True)

DB_FILEPATH = "buddymove_holidayiq.sqlite3"
connection = sqlite3.connect(DB_FILEPATH)

cursor = connection.cursor()

df.to_sql('review', con=connection)

##test queries
#Add all query results to dictionary

query = "SELECT count(*) FROM review"
result = cursor.execute(query).fetchall()

queries = {"Total rows: ": result[0][0]}

query = "SELECT count(distinct User_Id) FROM review WHERE Nature >= 100 and Shopping >= 100"
result = cursor.execute(query).fetchall()

queries.update({"--------------------\nTotal users with at least 100 nature and at least 100 shopping: ": result[0][0]})

query = "SELECT avg(Sports), avg(Religious), avg(Nature), avg(Theatre), avg(Shopping), avg(Picnic) FROM review"
result = cursor.execute(query).fetchall()

queries.update({"--------------------\nAverage Sports: ": result[0][0], "Average Religious: ": result[0][1],
                "Average Nature: ": result[0][2], "Average Theatre: ": result[0][3], "Average Shopping: ": result[0][4],
                "Average Picnic": result[0][5]})

for key, value in queries.items(): #print query results, with key being the description text, and value being the result
    print(key, value)