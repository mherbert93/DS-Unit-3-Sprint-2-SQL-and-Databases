import pymongo
import os
from dotenv import load_dotenv
import sqlite3
import pandas as pd

load_dotenv()

DB_URL = os.getenv("DB_URL")

connection_uri = DB_URL
client = pymongo.MongoClient(connection_uri)

sl_conn = sqlite3.connect('rpg_db.sqlite3')  # connect to rpg database
sl_curs = sl_conn.cursor()

queries = [['charactercreator_character', 'SELECT * FROM charactercreator_character'],
           ['armory_item', 'SELECT * FROM armory_item'], ['armory_weapoon', 'SELECT * FROM armory_weapon'],
           ['charactercreator_character_inventory', 'SELECT * FROM charactercreator_character_inventory'],
           ['charactercreator_cleric', 'SELECT * FROM charactercreator_cleric'],
           ['charactercreator_fighter', 'SELECT * FROM charactercreator_fighter'],
           ['charactercreator_mage', 'SELECT * FROM charactercreator_mage'],
           ['charactercreator_necromancer', 'SELECT * FROM charactercreator_necromancer'],
           ['charactercreator_thief', 'SELECT * FROM charactercreator_thief']]

db = client.rpgdata
for query in queries:
    collection_name = query[0]

    get_query = query[1]
    objects = sl_curs.execute(get_query).fetchall()

    df = pd.read_sql(get_query, con=sl_conn)
    df = df.to_dict(orient='records')

    db[collection_name].insert_many(df)

sl_conn.close()

# I enjoyed working with mongodb much more than postgresql. I found really nothing that was harder and everything
# was more simple. The more relaxed rules of mongodb make it easier to work with. However, in a real prod environment,
# I can definitely  see some downsides as well as upsides to mongodb.
