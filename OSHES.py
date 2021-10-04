import sqlite3
import json
import numpy as np
import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine

###connecting to SQL###
#db = create_engine('sqlite:///oshes.db')
conn = sqlite3.connect('OSHE') 
c = conn.cursor()
sql = open('oshe.sql', 'r')
sqlfile = sql.read()
sql.close()
sqlQueries = sqlfile.split(';')
for query in sqlQueries:
    c.execute(query)

#sample code#
#c.execute('UPDATE items SET Category = "Lights" WHERE ItemID = 1001') #update table
#print(pd.read_sql_query('SELECT Category FROM items WHERE ItemID == 1001',OSHE)) #prints output in idle

###connecting to MongoDB###
mongodb = MongoClient('localhost', 27017)
db = mongodb.OSHES #db is oshes

##create Items table##
collection = db.Items
items = open('items.json', 'r')
items_details = items.read()
items_json = json.loads(items_details)
Q = pd.DataFrame(np.array(items_json))
docs = json.loads(Q.T.to_json()).values()
collection.insert_many(docs)
##create Products table##
collection = db.Products
products = open('products.json', 'r')
products_details = products.read()
products_json = json.loads(products_details)
Q = pd.DataFrame(np.array(products_json))
docs = json.loads(Q.T.to_json()).values()
collection.insert_many(docs)

def addAdmin(ID, name, gender, number, pw):
    val = (ID, name, gender, number, pw)
    sql = "INSERT INTO Administrator (AdministratorID, AdminName, Gender, PhoneNumber, Password) VALUES " + str(val) + ";"
    c.execute(sql)
    return "done"

#def addCustomer()
def addCustomer(ID, name, address, gender, email, number, pw):
    val = (ID, name, address, gender, email, number, pw)
    sql = "INSERT INTO Customers(CustomerID, CustomerName, Address, Gender, EmailAddress, PhoneNumber, Password) VALUES" + str(val) + ";" 
    c.execute(sql)
    return "done"

#def customerPurchaseItem() #mg
def customerPurchaseItem(CustomerID, ItemID, PurchaseDate, PurchaseStatus):
    sql = "UPDATE Item SET CustomerID = ?, PurchaseDate = ?, PurchaseStatus = ? WHERE ItemID = ?"
    data = (CustomerID, PurchaseDate, PurchaseStatus, ItemID,)
    c.execute(sql, data)
    conn.commit()

    myquery = { "0.ItemID": ItemID }
    newvalues = { "$set": { "0.PurchaseStatus": PurchaseStatus } }
    db.Items.update_one({}, newvalues)

    return "done"

#def customerRequestService() #mg

#def customerPayService() #mg

#def adminAdministerService() #mg

#def customerSearch()

#def adminSearch()

