import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import json
import numpy as np
import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine
#Inventory table
from custTable import *
from request import *
from adminFunc import *
from oshes import *
import datetime

def simSearchTable(username, price, category, model, color, factory, powersupply, productionyear):
    #initializing screen
    root = Tk()
    root.title('Your Search Results')
    root.geometry("1000x500")

    conn = sqlite3.connect('OSHE')
    mongodb = MongoClient('localhost', 27017)
    db = mongodb.OSH 

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
    background="#D3D3D3",
    foreground="black",
    rowheight=25,
    fieldbackground="#D3D3D3")
    style.map('Treeview',
    background=[('selected', "#347083")])

    #creating tree view
    tree_frame = Frame(root)
    tree_frame.pack(pady=10)

    # Create a Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()

    # Configure the Scrollbar
    tree_scroll.config(command=my_tree.yview)

    # Define Our Columns
    my_tree['columns'] = ("ItemID", "Category", "Model")

    # Format Our Columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ItemID", anchor=W, width=50)
    my_tree.column("Category", anchor=CENTER, width=90)
    my_tree.column("Model", anchor=CENTER, width=90)


    # Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("ItemID",text="ItemID", anchor=W)
    my_tree.heading("Category",text="Category", anchor=CENTER)
    my_tree.heading("Model", text="Model", anchor=CENTER)

    # Create Striped Row Tags
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")
    
    global count
    count = 0

    allpdt = []
    returnedresults = []
    if category == "None":
        category = db.Items.distinct("0.Category")
    else:
        category = [category]
    if model == "None":
        model = db.Items.distinct("0.Model")
    else:
        model = [model]
    for x in category:
        for y in model:
            item = (db.Items.find_one({"0.Category": str(x), "0.Model": str(y), "0.PurchaseStatus": "Unsold"}))
            print(item)
            if item:
                if count % 2 == 0:
                    my_tree.insert(parent='', index='end',iid=count,text='',values=(item['0']['ItemID'],item['0']['Category'],item['0']['Model']), tags=('evenrow',))
                else:
                    my_tree.insert(parent='', index='end',iid=count,text='',values=(item['0']['ItemID'],item['0']['Category'],item['0']['Model']), tags=('oddrow',))
                count += 1
    
    data_frame = LabelFrame(root, text="Purchase Information")
    data_frame.pack(fill="x", expand="yes", padx=10)
    itemId_label = Label(data_frame, text="ItemID")
    itemId_label.grid(row=0, column=2, padx=10, pady=10)
    itemId_entry = Entry(data_frame)
    itemId_entry.grid(row=0, column=3, padx=10, pady=10)

    model_label = Label(data_frame, text="Model")
    model_label.grid(row=0, column=4, padx=10, pady=10)
    model_entry = Entry(data_frame)
    model_entry.grid(row=0, column=5, padx=10, pady=10)

    def select_record(e):
        # Clear entry boxes
        itemId_entry.delete(0, END)
        model_entry.delete(0, END)

        # Grab record Number
        selected = my_tree.focus()
        # Grab record values
        values = my_tree.item(selected, 'values')

        itemId = values[0]
        
        # outpus to entry boxes
        itemId_entry.insert(0, values[0])
        model_entry.insert(0, values[2])

    def clear_entries():
        # Clear entry boxes
        itemId_entry.delete(0, END)
        model_entry .delete(0, END)
        
    def customerPurchaseItem(ItemID, CustomerID):
        conn = sqlite3.connect('OSHE')
        c = conn.cursor()
        # MySQL update
        # sql1 = "SELECT * FROM Item WHERE ItemID = " + str(ItemID) + ";"
        # c.execute(sql1)
        # if c.fetchall != None:
        #     messagebox.showerror(title="FAILED",message="Item has already been purchased. Please choose a different product")
        # else:
        if ItemID == "":
            messagebox.showerror(title="FAILED",message="Please choose an item!")
        else:
            val = (str(ItemID), CustomerID, datetime.date.today().strftime('%Y-%m-%d'))
            sql = "INSERT INTO Item (ItemID, CustomerID, PurchaseDate) VALUES " + str(val) + ";"
            c.execute(sql)
            messagebox.showerror(title="SUCCESS",message="Item purchased!")
            myquery = { "0.ItemID": ItemID }
            newvalues = {"$set": {"0.PurchaseStatus": "Sold"} }
            db.Items.update_one(myquery, newvalues)

        # Use to check if data has been inserted into MySQL.
        c.execute("SELECT * FROM Item;")
        print(c.fetchall())
        conn.commit()
        conn.close()
        

    #buttons
    button_frame = LabelFrame(root, text="")
    button_frame.pack(fill="x", expand="yes", padx=20)

    buy_button = Button(button_frame, text="Purchase Product",command = lambda: customerPurchaseItem(itemId_entry.get(), username.get()))
    buy_button.grid(row=0, column=0, padx=10, pady=10)

    select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
    select_record_button.grid(row=0, column=7, padx=10, pady=10)
    
    # Bind the treeview
    my_tree.bind("<ButtonRelease-1>",select_record)

    
def advSearchTable(username, price, category, model, color, factory, powersupply, productionyear, itemID):
    #initializing screen
    root = Tk()
    root.title('Your Search Results')
    root.geometry("1000x500")


    conn = sqlite3.connect('OSHE')
    c = conn.cursor()
    mongodb = MongoClient('localhost', 27017)
    db = mongodb.OSH 

    global count
    count = 0

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
    background="#D3D3D3",
    foreground="black",
    rowheight=25,
    fieldbackground="#D3D3D3")
    style.map('Treeview',
    background=[('selected', "#347083")])

    #creating tree view
    tree_frame = Frame(root)
    tree_frame.pack(pady=10)

    # Create a Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()

    # Configure the Scrollbar
    tree_scroll.config(command=my_tree.yview)

    # Define Our Columns
    my_tree['columns'] = ("ItemID", "Category", "Model", "Price", "Colour", "Factory",
                        "PowerSupply","Production Year")

    # Format Our Columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ItemID", anchor=W, width=50)
    my_tree.column("Category", anchor=CENTER, width=90)
    my_tree.column("Model", anchor=CENTER, width=90)
    my_tree.column("Price", anchor=CENTER, width=70)
    my_tree.column("Colour", anchor=CENTER, width=90)
    my_tree.column("Factory", anchor=CENTER, width=100)
    my_tree.column("PowerSupply", anchor=CENTER, width=90)
    my_tree.column("Production Year", anchor=CENTER, width=100)


    # Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("ItemID",text="ItemID", anchor=W)
    my_tree.heading("Category",text="Category", anchor=CENTER)
    my_tree.heading("Model", text="Model", anchor=CENTER)
    my_tree.heading("Price", text="Price",anchor=CENTER)
    my_tree.heading("Colour", text ="Colour", anchor=CENTER)
    my_tree.heading("Factory", text="Factory", anchor=CENTER)
    my_tree.heading("PowerSupply",text="PowerSupply", anchor=CENTER)
    my_tree.heading("Production Year", text="Production Year", anchor=CENTER)

    # Create Striped Row Tags
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")

    # Create Striped Row Tags
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")
    
    if category == "None":
        category = db.Items.distinct("0.Category")
    else:
        category = [category]
    if model == "None":
        model = db.Items.distinct("0.Model")
    else:
        model = [model]
    if color == "None":
        color = db.Items.distinct("0.Color")
    else:
        color = [color]
    if factory == "None":
        factory = db.Items.distinct("0.Factory")
    else:
        factory = [factory]
    if powersupply == "None":
        powersupply = db.Items.distinct("0.PowerSupply")
    else:
        powersupply = [powersupply]
    if productionyear == "None":
        productionyear = db.Items.distinct("0.ProductionYear")
    else:
        productionyear = [productionyear]
    
    item = db.Items.find_one({'0.Category': {'$in': category}, '0.Model': {'$in':model}, '0.Color': {'$in':color}, '0.Factory': {'$in':factory}, '0.PowerSupply': {'$in':powersupply}, '0.ProductionYear':{'$in':productionyear}})
    my_tree.insert(parent='', index='end',iid=count,text='',values=(item['0']['ItemID'],item['0']['Category'],item['0']['Model'],0,item['0']['Color'],item['0']['Factory'],item['0']['PowerSupply'],item['0']['ProductionYear']), tags=('evenrow',))
    
    data_frame = LabelFrame(root, text="Purchase Information")
    data_frame.pack(fill="x", expand="yes", padx=10)
    itemId_label = Label(data_frame, text="ItemID")
    itemId_label.grid(row=0, column=2, padx=10, pady=10)
    itemId_entry = Entry(data_frame)
    itemId_entry.grid(row=0, column=3, padx=10, pady=10)

    model_label = Label(data_frame, text="Model")
    model_label.grid(row=0, column=4, padx=10, pady=10)
    model_entry = Entry(data_frame)
    model_entry.grid(row=0, column=5, padx=10, pady=10)
        
    def select_record(e):
        # Clear entry boxes
        itemId_entry.delete(0, END)
        model_entry.delete(0, END)

        # Grab record Number
        selected = my_tree.focus()
        # Grab record values
        values = my_tree.item(selected, 'values')

        itemId = values[0]
        
        # outpus to entry boxes
        itemId_entry.insert(0, values[0])
        model_entry.insert(0, values[2])

    def clear_entries():
        # Clear entry boxes
        itemId_entry.delete(0, END)
        model_entry .delete(0, END)
        
    def customerPurchaseItem(ItemID, CustomerID):
        conn = sqlite3.connect('OSHE')
        c = conn.cursor()
        # MySQL update
        # sql1 = "SELECT * FROM Item WHERE ItemID = " + str(ItemID) + ";"
        # c.execute(sql1)
        # if c.fetchall != None:
        #     messagebox.showerror(title="FAILED",message="Item has already been purchased. Please choose a different product")
        # else:
        if ItemID == "":
            messagebox.showerror(title="FAILED",message="Please choose an item!")
        else:
            val = (str(ItemID), CustomerID, datetime.date.today().strftime('%Y-%m-%d'))
            sql = "INSERT INTO Item (ItemID, CustomerID, PurchaseDate) VALUES " + str(val) + ";"
            c.execute(sql)
            messagebox.showerror(title="SUCCESS",message="Item purchased!")
            myquery = { "0.ItemID": ItemID }
            newvalues = {"$set": {"0.PurchaseStatus": "Sold"} }
            db.Items.update_one(myquery, newvalues)

        # Use to check if data has been inserted into MySQL.
        c.execute("SELECT * FROM Item;")
        print(c.fetchall())
        conn.commit()
        conn.close()
        

    #buttons
    button_frame = LabelFrame(root, text="")
    button_frame.pack(fill="x", expand="yes", padx=20)

    buy_button = Button(button_frame, text="Purchase Product",command = lambda: customerPurchaseItem(itemId_entry.get(), username.get()))
    buy_button.grid(row=0, column=0, padx=10, pady=10)

    select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
    select_record_button.grid(row=0, column=7, padx=10, pady=10)
    
    # Bind the treeview
    my_tree.bind("<ButtonRelease-1>",select_record)


def adminAdvSearchTable(username, price, cost, category, model, color, factory, powersupply, productionyear, itemID):
    #initializing screen
    root = Tk()
    root.title('Your Search Results')
    root.geometry("1000x500")


    conn = sqlite3.connect('OSHE')
    c = conn.cursor()
    mongodb = MongoClient('localhost', 27017)
    db = mongodb.OSH 

    global count    
    count = 0

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
    background="#D3D3D3",
    foreground="black",
    rowheight=25,
    fieldbackground="#D3D3D3")
    style.map('Treeview',
    background=[('selected', "#347083")])

    #creating tree view
    tree_frame = Frame(root)
    tree_frame.pack(pady=10)

    # Create a Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()

    # Configure the Scrollbar
    tree_scroll.config(command=my_tree.yview)

    # Define Our Columns
    my_tree['columns'] = ("ItemID", "Category", "Model", "Cost","Price", "Colour", "Factory",
                        "PowerSupply","Production Year", "Stock Level", "Purchase Status", 
                        "Service Status", "Warranty", "ProductID")

    # Format Our Columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ItemID", anchor=W, width=50)
    my_tree.column("Category", anchor=CENTER, width=90)
    my_tree.column("Model", anchor=CENTER, width=90)
    my_tree.column("Cost", anchor=CENTER, width=90)
    my_tree.column("Price", anchor=CENTER, width=70)
    my_tree.column("Colour", anchor=CENTER, width=90)
    my_tree.column("Factory", anchor=CENTER, width=100)
    my_tree.column("PowerSupply", anchor=CENTER, width=90)
    my_tree.column("Production Year", anchor=CENTER, width=100)
    #newattributes
    my_tree.column("Stock Level", anchor=CENTER, width=100)
    my_tree.column("Purchase Status", anchor=CENTER, width=100)
    my_tree.column("Service Status", anchor=CENTER, width=100)
    my_tree.column("Warranty", anchor=CENTER, width=100)
    my_tree.column("ProductID", anchor=CENTER, width=100)

    # Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("ItemID",text="ItemID", anchor=W)
    my_tree.heading("Category",text="Category", anchor=CENTER)
    my_tree.heading("Model", text="Model", anchor=CENTER)
    my_tree.heading("Cost", text="Cost ($)", anchor=CENTER)
    my_tree.heading("Price", text="Price ($)",anchor=CENTER)
    my_tree.heading("Colour", text ="Colour", anchor=CENTER)
    my_tree.heading("Factory", text="Factory", anchor=CENTER)
    my_tree.heading("PowerSupply",text="Power Supply", anchor=CENTER)
    my_tree.heading("Production Year", text="Production Year", anchor=CENTER)
    my_tree.heading("Stock Level", text="Stock Level", anchor=CENTER)
    #newattributes
    my_tree.heading("Stock Level", text="Stock Level", anchor=CENTER)
    my_tree.heading("Purchase Status", text="Purchase Status", anchor=CENTER)
    my_tree.heading("Service Status", text="Service Status", anchor=CENTER)
    my_tree.heading("Warranty", text="Warranty (Months)", anchor=CENTER)
    my_tree.heading("ProductID", text="ProductID", anchor=CENTER)

    # Create Striped Row Tags
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")

    # Create Striped Row Tags
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")
    
    if category == "None":
        category_n = "-"
        category = db.Items.distinct("0.Category")
    else:
        category_n = category
        category = [category]
    if model == "None":
        model_n = "-"
        model = db.Items.distinct("0.Model")    
    else:
        model_n = model
        model = [model]
    if cost == "None":
        cost_n = "-"
        cost = db.Products.distinct("0.Cost")
    else:
        cost_n = cost
        modelitem = db.Products.find({'0.Cost':cost})[0]['0']['Model']
        model = [modelitem]
    if color == "None":
        color_n = "-"
        color = db.Items.distinct("0.Color")
    else:
        color_n = color
        color = [color]
    if factory == "None":
        factory_n = "-"
        factory = db.Items.distinct("0.Factory")
    else:
        factory_n = factory
        factory = [factory]
    if powersupply == "None":
        ps_n = "-"
        powersupply = db.Items.distinct("0.PowerSupply")
    else:
        ps_n = powersupply
        powersupply = [powersupply]
    if productionyear == "None":
        py_n = "-"
        productionyear = db.Items.distinct("0.ProductionYear")
    else:
        py_n = productionyear
        productionyear = [productionyear]
    if itemID == "":
        if len(model) > 1:
            price_n = "-"
        else:
            price_n = str(db.Products.find({"0.Model": model[0]})[0]['0']['Price ($)'])
        itemID_n = "-"
        itemID = db.Items.distinct("0.ItemID")
        purchasestatus_n = "-"
        servicestatus_n = "-"
        warranty_n = "-"
        productid_n = "-"
        allitems = db.Items.find({'0.ItemID': {'$in': itemID}, '0.Category': {'$in': category}, '0.Model': {'$in':model}, '0.Color': {'$in':color}, '0.Factory': {'$in':factory}, '0.PowerSupply': {'$in':powersupply}, '0.ProductionYear':{'$in':productionyear}}).count()
        item = db.Items.find_one({'0.ItemID': {'$in': itemID}, '0.Category': {'$in': category}, '0.Model': {'$in':model}, '0.Color': {'$in':color}, '0.Factory': {'$in':factory}, '0.PowerSupply': {'$in':powersupply}, '0.ProductionYear':{'$in':productionyear}})
        my_tree.insert(parent='', index='end',iid=count,text='',values=(itemID_n,category_n,model_n,cost_n,price_n,color_n,factory_n,ps_n,py_n, allitems, purchasestatus_n, servicestatus_n, warranty_n, productid_n), tags=('evenrow',))
    

    else:
        itemID_n = itemID
        modeltype = db.Items.find({'0.ItemID': itemID})[0]['0']['Model']
        purchasestatus_n = db.Items.find({'0.ItemID': itemID})[0]['0']['PurchaseStatus']
        servicestatus_n = db.Items.find({'0.ItemID': itemID})[0]['0']['ServiceStatus']
        if servicestatus_n == "":
            servicestatus_n = "-"
        warranty_n = db.Products.find({'0.Model': modeltype})[0]['0']['Warranty (months)']
        productid_n = db.Products.find({'0.Model': modeltype})[0]['0']['ProductID']
        price_n = db.Products.find({'0.Model': modeltype})[0]['0']['Price ($)']
        cost_n = db.Products.find({'0.Model': modeltype})[0]['0']['Cost ($)']
        s = db.Items.find({'0.ItemID': itemID})[0]['0']
        my_tree.insert(parent='', index='end',iid=count,text='',values=(itemID_n,s['Category'],s['Model'],cost_n, price_n,s['Color'],s['Factory'],s['PowerSupply'],s['ProductionYear'],'1', purchasestatus_n, servicestatus_n, warranty_n, productid_n), tags=('evenrow',))
    
    data_frame = LabelFrame(root, text="Purchase Information")
    data_frame.pack(fill="x", expand="yes", padx=10)
    itemId_label = Label(data_frame, text="ItemID")
    itemId_label.grid(row=0, column=2, padx=10, pady=10)
    itemId_entry = Entry(data_frame)
    itemId_entry.grid(row=0, column=3, padx=10, pady=10)

    model_label = Label(data_frame, text="Model")
    model_label.grid(row=0, column=4, padx=10, pady=10)
    model_entry = Entry(data_frame)
    model_entry.grid(row=0, column=5, padx=10, pady=10)
        
    def select_record(e):
        # Clear entry boxes
        itemId_entry.delete(0, END)
        model_entry.delete(0, END)

        # Grab record Number
        selected = my_tree.focus()
        # Grab record values
        values = my_tree.item(selected, 'values')

        itemId = values[0]
        
        # outpus to entry boxes
        itemId_entry.insert(0, values[0])
        model_entry.insert(0, values[2])

    def clear_entries():
        # Clear entry boxes
        itemId_entry.delete(0, END)
        model_entry .delete(0, END)
        
    def customerPurchaseItem(ItemID, CustomerID):
        conn = sqlite3.connect('OSHE')
        c = conn.cursor()
        # MySQL update
        # sql1 = "SELECT * FROM Item WHERE ItemID = " + str(ItemID) + ";"
        # c.execute(sql1)
        # if c.fetchall != None:
        #     messagebox.showerror(title="FAILED",message="Item has already been purchased. Please choose a different product")
        # else:
        if ItemID == "":
            messagebox.showerror(title="FAILED",message="Please choose an item!")
        else:
            val = (str(ItemID), CustomerID, datetime.date.today().strftime('%Y-%m-%d'))
            sql = "INSERT INTO Item (ItemID, CustomerID, PurchaseDate) VALUES " + str(val) + ";"
            c.execute(sql)
            messagebox.showerror(title="SUCCESS",message="Item purchased!")
            myquery = { "0.ItemID": ItemID }
            newvalues = {"$set": {"0.PurchaseStatus": "Sold"} }
            db.Items.update_one(myquery, newvalues)

        # Use to check if data has been inserted into MySQL.
        c.execute("SELECT * FROM Item;")
        print(c.fetchall())
        conn.commit()
        conn.close()
        

#buttons
    button_frame = LabelFrame(root, text="")
    button_frame.pack(fill="x", expand="yes", padx=20)

    buy_button = Button(button_frame, text="Purchase Product",command = lambda: customerPurchaseItem(itemId_entry.get(), username.get()))
    buy_button.grid(row=0, column=0, padx=10, pady=10)

    select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
    select_record_button.grid(row=0, column=7, padx=10, pady=10)
    
    # Bind the treeview
    my_tree.bind("<ButtonRelease-1>",select_record)


def adminSimSearchTable(username, price, category, model, color, factory, powersupply, productionyear):
    #initializing screen
    root = Tk()
    root.title('Your Search Results')
    root.geometry("1000x500")

    conn = sqlite3.connect('OSHE')
    mongodb = MongoClient('localhost', 27017)
    db = mongodb.OSH 

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
    background="#D3D3D3",
    foreground="black",
    rowheight=25,
    fieldbackground="#D3D3D3")
    style.map('Treeview',
    background=[('selected', "#347083")])

    #creating tree view
    tree_frame = Frame(root)
    tree_frame.pack(pady=10)

    # Create a Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()

    # Configure the Scrollbar
    tree_scroll.config(command=my_tree.yview)

    # Define Our Columns
    my_tree['columns'] = ("ItemID", "Category", "Model", "Number Sold", "Number Unsold")

    # Format Our Columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ItemID", anchor=W, width=50)
    my_tree.column("Category", anchor=CENTER, width=90)
    my_tree.column("Model", anchor=CENTER, width=90)
    my_tree.column("Number Sold", anchor=CENTER, width=90)
    my_tree.column("Number Unsold", anchor=CENTER, width=90)


    # Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("ItemID",text="ItemID", anchor=W)
    my_tree.heading("Category",text="Category", anchor=CENTER)
    my_tree.heading("Model", text="Model", anchor=CENTER)
    my_tree.heading("Number Sold", text="Number Sold", anchor=CENTER)
    my_tree.heading("Number Unsold", text="Number Unsold", anchor=CENTER)

    # Create Striped Row Tags
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")
    
    global count
    count = 0

    allpdt = []
    returnedresults = []
    if category == "None":
        category = db.Items.distinct("0.Category")
    else:
        category = [category]
    if model == "None":
        model = db.Items.distinct("0.Model")
    else:
        model = [model]
    for x in category:
        for y in model:
            item = (db.Items.find_one({"0.Category": str(x), "0.Model": str(y), "0.PurchaseStatus": "Unsold"}))
            print(item)
            if item:
                allitemsSold = db.Items.find({"0.Category": str(x), "0.Model": str(y), "0.PurchaseStatus": "Sold"}).count()
                allitemsUnsold = db.Items.find({"0.Category": str(x), "0.Model": str(y), "0.PurchaseStatus": "Unsold"}).count()
                if count % 2 == 0:
                    my_tree.insert(parent='', index='end',iid=count,text='',values=(item['0']['ItemID'],item['0']['Category'],item['0']['Model'],allitemsSold,allitemsUnsold), tags=('evenrow',))
                else:
                    my_tree.insert(parent='', index='end',iid=count,text='',values=(item['0']['ItemID'],item['0']['Category'],item['0']['Model'],allitemsSold,allitemsUnsold), tags=('oddrow',))
                count += 1
    
    data_frame = LabelFrame(root, text="Purchase Information")
    data_frame.pack(fill="x", expand="yes", padx=10)
    itemId_label = Label(data_frame, text="ItemID")
    itemId_label.grid(row=0, column=2, padx=10, pady=10)
    itemId_entry = Entry(data_frame)
    itemId_entry.grid(row=0, column=3, padx=10, pady=10)

    model_label = Label(data_frame, text="Model")
    model_label.grid(row=0, column=4, padx=10, pady=10)
    model_entry = Entry(data_frame)
    model_entry.grid(row=0, column=5, padx=10, pady=10)

    def select_record(e):
        # Clear entry boxes
        itemId_entry.delete(0, END)
        model_entry.delete(0, END)

        # Grab record Number
        selected = my_tree.focus()
        # Grab record values
        values = my_tree.item(selected, 'values')

        itemId = values[0]
        
        # outpus to entry boxes
        itemId_entry.insert(0, values[0])
        model_entry.insert(0, values[2])

    def clear_entries():
        # Clear entry boxes
        itemId_entry.delete(0, END)
        model_entry .delete(0, END)
        
    def customerPurchaseItem(ItemID, CustomerID):
        conn = sqlite3.connect('OSHE')
        c = conn.cursor()
        # MySQL update
        # sql1 = "SELECT * FROM Item WHERE ItemID = " + str(ItemID) + ";"
        # c.execute(sql1)
        # if c.fetchall != None:
        #     messagebox.showerror(title="FAILED",message="Item has already been purchased. Please choose a different product")
        # else:
        if ItemID == "":
            messagebox.showerror(title="FAILED",message="Please choose an item!")
        else:
            val = (str(ItemID), CustomerID, datetime.date.today().strftime('%Y-%m-%d'))
            sql = "INSERT INTO Item (ItemID, CustomerID, PurchaseDate) VALUES " + str(val) + ";"
            c.execute(sql)
            messagebox.showerror(title="SUCCESS",message="Item purchased!")
            myquery = { "0.ItemID": ItemID }
            newvalues = {"$set": {"0.PurchaseStatus": "Sold"} }
            db.Items.update_one(myquery, newvalues)

        # Use to check if data has been inserted into MySQL.
        c.execute("SELECT * FROM Item;")
        print(c.fetchall())
        conn.commit()
        conn.close()
        

    #buttons
    button_frame = LabelFrame(root, text="")
    button_frame.pack(fill="x", expand="yes", padx=20)

    buy_button = Button(button_frame, text="Purchase Product",command = lambda: customerPurchaseItem(itemId_entry.get(), username.get()))
    buy_button.grid(row=0, column=0, padx=10, pady=10)

    select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
    select_record_button.grid(row=0, column=7, padx=10, pady=10)
    
    # Bind the treeview
    my_tree.bind("<ButtonRelease-1>",select_record)
