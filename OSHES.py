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
#db.Items.find_one({"0.ItemID": "1073"}) #prints a document from MongoDB Items collection


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

def advancedSearch(category, model, color, factory, powersupply, productionyear):
    if category == "none":
        category = db.Items.distinct("0.Category")
    else:
        category = [category]
    if model == "none":
        model = db.Items.distinct("0.Model")
    else:
        model = [model]
    if color == "none":
        color = db.Items.distinct("0.Color")
    else:
        color = [color]
    if factory == "none":
        factory = db.Items.distinct("0.Factory")
    else:
        factory = [factory]
    if powersupply == "none":
        powersupply = db.Items.distinct("0.PowerSupply")
    else:
        powersupply = [powersupply]
    if productionyear == "none":
        productionyear = db.Items.distinct("0.ProductionYear")
    else:
        productionyear = [productionyear]
    return(db.Items.find_one({'0.Category': {'$in': category}, '0.Model': {'$in':model}, '0.Factory': {'$in':factory}, '0.PowerSupply': {'$in':powersupply}, '0.ProductionYear':{'$in':productionyear}})))

def getNumberOfItemsSoldByModel():
    models = ['Light1', 'Light2', 'SmartHome1', 'Safe1', 'Safe2', 'Safe3']
    oshe_db = mongodb["OSHES"]
    items = oshe_db["Items"]

    for model in models:
        counts_sold = items.count_documents({'0.Model': model, '0.PurchaseStatus': "Sold"})
        print(f"{model}: " + str(counts_sold))
        
#still abit buggy for this
def initializeTable():
    models = ['Light1', 'Light2', 'SmartHome1', 'Safe1', 'Safe2', 'Safe3']
    oshe_db = mongodb["OSHES"]
    items = oshe_db["Items"]
    lst = []

    for eachmodel in models:
        counts_sold = items.count_documents({'0.Model': eachmodel, '0.PurchaseStatus': "Sold"})
        counts_unsold = items.count_documents({'0.Model': eachmodel, '0.PurchaseStatus': "Unsold"})
        lst.append([eachmodel, counts_sold, counts_unsold])
        print(tabulate(lst, headers = ["IID", "Sold", "Unsold"]))
        
def customerPayService(RequestID, ItemID):
    sql = "UPDATE Request SET RequestStatus = 'In progress' WHERE RequestID = ?"
    data = (RequestID,)
    c.execute(sql, data)
    conn.commit()

    myquery = { "0.ItemID": ItemID }
    newvalues = { "$set": { "0.ServiceStatus": "Waiting for approval" } }
    db.Items.update_one(myquery, newvalues)

    val =("", RequestID, "Waiting for approval")
    sql = "INSERT INTO Service(AdministratorID, RequestID, ServiceStatus)VALUES" + str(val) + ";"
    c.execute(sql)

    sql = "UPDATE ServiceFee SET SettlementDate = CURRENT_DATE WHERE RequestID = ?"
    data = (RequestID,)
    c.execute(sql, data)
    conn.commit()

    return "done"

def getItemsUnderService():
    sql = "SELECT COUNT(ServiceStatus) FROM Service WHERE ServiceStatus != 'Completed'"
    c.execute(sql)
    result = c.fetchall()[0][0]
    print(result)
    
def allCustomersWithUnpaidServiceFee():
    sql = "SELECT COUNT(DISTINCT CustomerID) FROM Request WHERE RequestStatus == 'Submitted and Waiting for payment'"
    c.execute(sql)
    result = c.fetchall()[0][0]
    print(result)
#def customerRequestService() #mg

#def customerPayService() #mg

#def adminAdministerService() #mg

#def customerSearch()

#def adminSearch()

