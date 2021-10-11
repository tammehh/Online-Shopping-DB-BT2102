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

    
def advSearchTable(username, price, category, model, color, factory, powersupply, productionyear):
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
    
    item = db.Items.find_one({'0.Category': {'$in': category}, '0.Model': {'$in':model}, '0.Factory': {'$in':factory}, '0.PowerSupply': {'$in':powersupply}, '0.ProductionYear':{'$in':productionyear}})
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
        val = (str(ItemID), str(CustomerID), datetime.date.today().strftime('%Y-%m-%d'))
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

#buttons
    button_frame = LabelFrame(root, text="")
    button_frame.pack(fill="x", expand="yes", padx=20)

    buy_button = Button(button_frame, text="Purchase Product",command = lambda: customerPurchaseItem(itemId_entry.get(), username))
    buy_button.grid(row=0, column=0, padx=10, pady=10)

    select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
    select_record_button.grid(row=0, column=7, padx=10, pady=10)
    
    # Bind the treeview
    my_tree.bind("<ButtonRelease-1>",select_record)
