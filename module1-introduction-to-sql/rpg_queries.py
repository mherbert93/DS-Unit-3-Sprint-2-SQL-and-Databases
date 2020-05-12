import os
import sqlite3

DB_FILEPATH = "rpg_db.sqlite3"

connection = sqlite3.connect(DB_FILEPATH)

cursor = connection.cursor()

##test queries
#Add all query results to dictionary
query = """SELECT 
	count(distinct charactercreator_character.character_id) as total_characters, 
	count(distinct charactercreator_mage.character_ptr_id) as class_mage, 
	count(distinct charactercreator_thief.character_ptr_id) as class_thief, 
	count(distinct charactercreator_cleric.character_ptr_id) as class_cleric,
	count(distinct charactercreator_fighter.character_ptr_id) as class_fighter
FROM charactercreator_character
LEFT JOIN charactercreator_mage ON charactercreator_character.character_id = charactercreator_mage.character_ptr_id
LEFT JOIN charactercreator_fighter ON charactercreator_character.character_id = charactercreator_fighter.character_ptr_id
LEFT JOIN charactercreator_cleric ON charactercreator_character.character_id = charactercreator_cleric.character_ptr_id
LEFT JOIN charactercreator_thief ON charactercreator_character.character_id = charactercreator_thief.character_ptr_id"""

result = cursor.execute(query).fetchall()

queries = {"Total characters: ": result[0][0], "Total thieves: ": result[0][1], "Total clerics: ": result[0][2],
           "Total fighters: ": result[0][3], "Total mages: ": result[0][4]}

query = """SELECT 
count(distinct armory_item.item_id) as total_items,
count(distinct armory_weapon.item_ptr_id) as total_weapons,
(count(distinct armory_item.item_id) - count(distinct armory_weapon.item_ptr_id)) as not_weapons
from armory_item
LEFT JOIN armory_weapon on armory_item.item_id = item_ptr_id
"""

result = cursor.execute(query).fetchall()

queries.update({"--------------------\nTotal items ": result[0][0], "Total weapons: ": result[0][1],
               "Not weapons: ": result[0][2]})

query = """
SELECT
	count(distinct charactercreator_character_inventory.item_id) as total_items,
	count(distinct armory_weapon.item_ptr_id) as total_weapons
FROM charactercreator_character_inventory
LEFT JOIN armory_item on charactercreator_character_inventory.item_id = armory_item.item_id
LEFT JOIN armory_weapon on armory_item.item_id = armory_weapon.item_ptr_id
GROUP BY charactercreator_character_inventory.character_id
limit 20"""

character_items = cursor.execute(query).fetchall()

queries.update({"--------------------\n": "Character_Items, Character_Weapons"})

query = """
SELECT
	avg(total_items),
	avg(total_weapons)
FROM(
SELECT
	count(distinct charactercreator_character_inventory.item_id) as total_items,
	count(distinct armory_weapon.item_ptr_id) as total_weapons
FROM charactercreator_character_inventory
LEFT JOIN armory_item on charactercreator_character_inventory.item_id = armory_item.item_id
LEFT JOIN armory_weapon on armory_item.item_id = armory_weapon.item_ptr_id
GROUP BY charactercreator_character_inventory.character_id)"""

result = cursor.execute(query).fetchall()

queries.update({"--------------------\nAverage total items ": result[0][0], "Average total weapons: ": result[0][1]})

for key, value in queries.items(): #print query results, with key being the description text, and value being the result
    print(key, value) #For this query we print values side by side, so description text is split between the key and value
    if key == "--------------------\n":
        for row in character_items: #The actual values we must pull out of the list(not our created dictionary)
            print(row)
