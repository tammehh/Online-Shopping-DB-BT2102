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
    return(db.Items.find_one({'0.Category': {'$in': category}, '0.Model': {'$in':model}, '0.Factory': {'$in':factory}, '0.PowerSupply': {'$in':powersupply}, '0.ProductionYear':{'$in':productionyear}}))

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

def addAdmin(ID, name, gender, number, pw):
    val = (ID, name, gender, number, pw)
    sql = "INSERT INTO Administrator (AdministratorID, AdminName, Gender, PhoneNumber, Password) VALUES " + str(val) + ";"
    c.execute(sql)
    return "done"
# ---------------------------------------------------------------------------------------------------------------------------
def addCustomer(ID, name, address, gender, email, number, pw):
    val = (ID, name, address, gender, email, number, pw)
    sql = "INSERT INTO Customers(CustomerID, CustomerName, Address, Gender, EmailAddress, PhoneNumber, Password) VALUES" + str(val) + ";"
    c.execute(sql)
    return "done"
# ---------------------------------------------------------------------------------------------------------------------------
def customerPurchaseItem(ItemID, CustomerID):
    # MySQL update
    val = (ItemID, CustomerID, datetime.date.today().strftime('%Y-%m-%d'))
    sql = "INSERT INTO Item (ItemID, CustomerID, PurchaseDate) VALUES " + str(val) + ";"
    c.execute(sql)
    messagebox.showerror(title="SUCCESS",message="Item purchased!")

    # Use to check if data has been inserted into MySQL.
    c.execute("SELECT * FROM Item;")
    print(c.fetchone())

    # MongoDB update
    myquery = { "0.ItemID": ItemID }
    newvalues = {"$set": {"0.PurchaseStatus": "Sold"} }
    db.Items.update_one(myquery, newvalues)

    return "done"
# ---------------------------------------------------------------------------------------------------------------------------
def warrantyEffective(ItemID):

    model = db.Items.find_one({"0.ItemID": ItemID})['0']['Model']
    warranty = db.Products.find_one({"0.Model": model})['0']['Warranty (months)']

    sql = "SELECT PurchaseDate FROM Item WHERE ItemID = ?"
    data = (ItemID,)
    c.execute(sql, data)
    purchaseDate_str = c.fetchone()[0]
    purchaseDate_date = datetime.datetime.strptime(purchaseDate_str, "%Y-%m-%d")

    currentDate = datetime.date.today()
    if (currentDate.year - purchaseDate_date.year > 0):
        return (((currentDate.year - purchaseDate_date.year - 1) * 12 + (12 - purchaseDate_date.month + currentDate.month)) < warranty)
    else:
        return (currentDate.month - purchaseDate_date.month < warranty)
# ---------------------------------------------------------------------------------------------------------------------------
requestCount = 1
def customerRequestService(CustomerID, ItemID):
    global requestCount
    if (warrantyEffective(ItemID)):
        val = (requestCount, CustomerID, ItemID, "Submitted", datetime.date.today().strftime('%Y-%m-%d'))
        sql = "INSERT INTO Request(RequestID, CustomerID, ItemID, RequestStatus, RequestDate) VALUES" + str(val) + ";"
        c.execute(sql)
    else:
        val = (requestCount, CustomerID, ItemID, "Submitted and Waiting for payment",
               datetime.date.today().strftime('%Y-%m-%d'))
        sql = "INSERT INTO Request(RequestID, CustomerID, ItemID, RequestStatus, RequestDate) VALUES" + str(val) + ";"
        c.execute(sql)

        # get cost of item
        model = db.Items.find_one({"0.ItemID": ItemID})['0']['Model']
        cost = db.Products.find_one({"0.Model": model})['0']['Cost ($)']
        ServiceFee = 40 + 0.20 * cost

        # insert into ServiceFee table
        val = (CustomerID, requestCount, ServiceFee, None , datetime.date.today())
        sql = "INSERT INTO ServiceFee(CustomerID, RequestID, ServiceFee, SettlementDate, CreationDate) VALUES (?, ?, ?, ?, ?)"
        c.execute(sql, val)

        sql = "SELECT ServiceFee FROM ServiceFee WHERE CustomerID = ?"
        data = (CustomerID,)
        c.execute(sql, data)

        # purchaseDate = c.fetchall()[0][0]

    requestCount += 1
    return "done"
# ---------------------------------------------------------------------------------------------------------------------------
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

    return "paid"
# ---------------------------------------------------------------------------------------------------------------------------
def administratorApprove(RequestID, ItemID):
    sql = "UPDATE Request SET RequestStatus = 'Approved' WHERE RequestID = ?"
    data = (RequestID,)
    c.execute(sql, data)
    conn.commit()
	
    sql = "UPDATE Service SET ServiceStatus = 'In progress' WHERE RequestID = ?"
    data = (RequestID,)
    c.execute(sql, data)
    conn.commit()
    	
    sql = "UPDATE Service SET AdministratorID = ? WHERE RequestID = ?"
    data = (AdministratorID, RequestID,)
    c.execute(sql, data)
    conn.commit()

    myquery = { "0.ItemID": ItemID }
    newvalues = { "$set": { "0.ServiceStatus": "In progress"} }
    db.Items.update_one(myquery, newvalues)
	
    return "done"
# ---------------------------------------------------------------------------------------------------------------------------
def administratorCompleteService(RequestID, ItemID):
    sql = "UPDATE Request SET RequestStatus = 'Completed' WHERE RequestID = ?"
    data = (RequestID,)
    c.execute(sql, data)
    conn.commit()
	
    myquery = { "0.ItemID": ItemID }
    newvalues = { "$set": { "0.ServiceStatus": "Completed"} }
    db.Items.update_one(myquery, newvalues)
	
    return "done"
# ---------------------------------------------------------------------------------------------------------------------------
def getNumberOfItemsSoldByModel():
    models = ['Light1', 'Light2', 'SmartHome1', 'Safe1', 'Safe2', 'Safe3']
    oshe_db = mongodb["OSHES"]
    items = oshe_db["Items"]

    for model in models:
       	counts_sold = items.count_documents({'0.Model': model, '0.PurchaseStatus': "Sold"})
        print(f"{model}: " + str(counts_sold))
# ---------------------------------------------------------------------------------------------------------------------------
def getNumberOfItemsSoldByCategory():
    categories = ['Lights', 'Locks']
    oshe_db = mongodb["OSHES"]
    items = oshe_db["Items"]

    for category in categories:
        counts_sold = items.count_documents({'0.Category': category, '0.PurchaseStatus': "Sold"})
       	print(f"{category}: " + str(counts_sold))
# ---------------------------------------------------------------------------------------------------------------------------
def getItemsUnderService():
    sql = "SELECT COUNT(ServiceStatus) FROM Service WHERE ServiceStatus != 'Completed'"
    c.execute(sql)
    result = c.fetchall()[0][0]
    print(result)
# ---------------------------------------------------------------------------------------------------------------------------
def allCustomersWithUnpaidServiceFee():
    sql = "SELECT COUNT(DISTINCT CustomerID) FROM Request WHERE RequestStatus == 'Submitted and Waiting for payment'"
    c.execute(sql)
    result = c.fetchall()[0][0]
    print(result)
# ---------------------------------------------------------------------------------------------------------------------------
def customerCancelRequest(RequestID):
    sql = "UPDATE Request SET RequestStatus = ‘Cancelled’ WHERE RequestID = ?"
    data = (RequestID,)
    c.execute(sql, data)
    conn.commit()
    return "Request Cancelled."
# ---------------------------------------------------------------------------------------------------------------------------
def cancelAllExpiredRequests():
    sql = "UPDATE Request SET RequestStatus = 'Cancelled' WHERE julianday('now') - julianday(RequestDate) > 10;"
    c.execute(sql)
    conn.commit()
    
    # Use to check if the expired request has been cancelled
    c.execute("SELECT * FROM REQUEST")
    print(c.fetchall())
# ---------------------------------------------------------------------------------------------------------------------------
def initialiseTable():
    models = ['Light1', 'Light2', 'SmartHome1', 'Safe1', 'Safe2', 'Safe3']
    items = db["Items"]
    lst = []

    for model in models:
        counts_sold = items.count_documents({'0.Model': model, '0.PurchaseStatus': "Sold"})
        counts_unsold = items.count_documents({'0.Model': model, '0.PurchaseStatus': "Unsold"})
        lst.append([model, counts_sold, counts_unsold])

    print(tabulate(lst, headers = ["IID", "Sold", "Unsold"]))
