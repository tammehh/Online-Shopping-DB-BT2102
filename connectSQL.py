import sqlite3
import json
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

db = create_engine('sqlite:///oshes.db')
db.execute('DROP TABLE IF EXISTS items;')
itemsjson = pd.read_json('items.json')
itemsjson.to_sql('items', db)
#pd.read_sql_query('UPDATE items SET Category = "lighty" WHERE ItemID = 1001', db) #update database in sql
db.execute('UPDATE items SET Category = "lighty" WHERE ItemID = 1001')
print(pd.read_sql_query('SELECT Category FROM items WHERE ItemID == 1001', db)) #prints output in idle
