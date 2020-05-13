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

sl_conn = sqlite3.connect('rpg_db.sqlite3')
sl_curs = sl_conn.cursor()

###characters
get_characters = 'SELECT * FROM charactercreator_character'
characters = sl_curs.execute(get_characters).fetchall()

create_character_table = """
CREATE TABLE charactercreator_character (
  character_id SERIAL PRIMARY KEY,
  name VARCHAR(30),
  level INT,
  exp INT,
  hp INT,
  strength INT,
  intelligence INT,
  dexterity INT,
  wisdom INT
);
"""

pg_curs.execute(create_character_table)
pg_conn.commit()

for character in characters:
    insert_character = """
    INSERT INTO charactercreator_character
    (name, level, exp, hp, strength, intelligence, dexterity, wisdom)
    VALUES """ + str(character[1:]) + ";"
    pg_curs.execute(insert_character)
pg_conn.commit()


###items
get_items = 'SELECT * FROM armory_item'
items = sl_curs.execute(get_items).fetchall()

create_item_table = """
CREATE TABLE armory_item (
    item_id SERIAL PRIMARY KEY,
    name VARCHAR(30),
    value INT,
    weight INT
);"""

pg_curs.execute(create_item_table)
pg_conn.commit()

for item in items:
    insert_item = """
    INSERT INTO armory_item
    (name, value, weight)
    VALUES """ + str(item[1:]) + ";"
    pg_curs.execute(insert_item)
pg_conn.commit()