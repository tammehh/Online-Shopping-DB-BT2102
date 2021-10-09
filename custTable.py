from tkinter import *
from tkinter import ttk

import sqlite3
import json
import numpy as np
import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine
#file containing the mongo and sql functions
from oshes import *


def query_database(username,my_tree):
        # Create a database or connect to one that exists
        mongodb = MongoClient('localhost', 27017)
        db = mongodb.OSHES #db is oshes
        conn = sqlite3.connect('OSHE')

        # Create a cursor instance
        c = conn.cursor()
        db = mongodb.OSHES

        c.execute("SELECT ItemID, PurchaseDate FROM Item where CustomerID = ?",(username,))
        records = c.fetchall()
        # Add our data to the screen
        global count
        count = 0
        
	#USed to debug ur queries
        #for record in records:
        	#print(record)

        for record in records:
                ItemID = record[0]
                cat = db.Items.find_one({"0.ItemID": ItemID})['0']['Category']
                model = db.Items.find_one({"0.ItemID": ItemID})['0']['Model']
                price = db.Products.find_one({"0.Model": model})['0']['Price ($)']
                colour = db.Items.find_one({"0.ItemID": ItemID})['0']['Color']
                factory = db.Items.find_one({"0.ItemID": ItemID})['0']['Factory']
                power = db.Items.find_one({"0.ItemID": ItemID})['0']['PowerSupply']
                py = db.Items.find_one({"0.ItemID": ItemID})['0']['ProductionYear']
                war = db.Products.find_one({"0.Model": model})['0']['Warranty (months)']
                ss = db.Items.find_one({"0.ItemID": ItemID})['0']['ServiceStatus']
                if count % 2 == 0:
                        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], cat, model, price, colour, factory, power, py, war,ss,record[1]), tags=('evenrow',))
                else:
                        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], cat, model,price, colour, factory,power, py, war,ss,record[1]), tags=('oddrow',))
                # increment counter
                count += 1


        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()
        requestCount = 1
#need warrantyEffective function code
def customerRequestService(CustomerID, ItemID):
    global requestCount
    pass
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
        # sql = "INSERT INTO ServiceFee(CustomerID, RequestID, ServiceFee, SettlementDate, CreationDate) VALUES" + str(val) + ";"
        sql = "INSERT INTO ServiceFee(CustomerID, RequestID, ServiceFee, SettlementDate, CreationDate) VALUES (?, ?, ?, ?, ?)"
        c.execute(sql, val)

        sql = "SELECT ServiceFee FROM ServiceFee WHERE CustomerID = ?"
        data = (CustomerID,)
        c.execute(sql, data)

    requestCount += 1
    return "done"
def custTable(username):
    #initializing screen
    root = Tk()
    root.title('Past purchases')
    root.geometry("1000x500")

    conn = sqlite3.connect('OSHE')
    
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
                          "PowerSupply","Production Year", "Warranty period","Service Status","Purchase Date")

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
    my_tree.column("Warranty period", anchor=CENTER, width=100)
    my_tree.column("Service Status", anchor=CENTER, width=100)
    my_tree.column("Purchase Date", anchor=CENTER, width=100)


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
    my_tree.heading("Warranty period", text="Warranty period", anchor=CENTER)
    my_tree.heading("Service Status", text="Service Status", anchor=CENTER)
    my_tree.heading("Purchase Date", text="Purchase Date", anchor=CENTER)

    # Create Striped Row Tags
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")
    
    data_frame = LabelFrame(root, text="Item information")
    data_frame.pack(fill="x", expand="yes", padx=10)

    itemId_label = Label(data_frame, text="ItemID")
    itemId_label.grid(row=0, column=0, padx=10, pady=10)
    itemId_entry = Entry(data_frame)
    itemId_entry.grid(row=0, column=1, padx=10, pady=10)


    warranty_label = Label(data_frame, text="Warranty")
    warranty_label.grid(row=0, column=2, padx=10, pady=10)
    warranty_entry = Entry(data_frame)
    warranty_entry.grid(row=0, column=3, padx=10, pady=10)

    ss_label = Label(data_frame, text="Service Status")
    ss_label.grid(row=0, column=4, padx=10, pady=10)
    ss_entry = Entry(data_frame)
    ss_entry.grid(row=0, column=5, padx=10, pady=10)

    c_label = Label(data_frame, text="Category")
    c_label.grid(row=1, column=0, padx=10, pady=10)
    c_entry = Entry(data_frame)
    c_entry.grid(row=1, column=1, padx=10, pady=10)
    
    m_label = Label(data_frame, text="Model")
    m_label.grid(row=1, column=2, padx=10, pady=10)
    m_entry = Entry(data_frame)
    m_entry.grid(row=1, column=3, padx=10, pady=10)
    
    pd_label = Label(data_frame, text="Model")
    pd_label.grid(row=1, column=4, padx=10, pady=10)
    pd_entry = Entry(data_frame)
    pd_entry.grid(row=1, column=5, padx=10, pady=10) 

    def clear_entries():
            # Clear entry boxes
            itemId_entry.delete(0, END)
            warranty_entry .delete(0, END)
            c_entry.delete(0, END)
            ss_entry.delete(0, END)
            m_entry.delete(0, END)
            pd_entry.delete(0,END)
            
            
    def select_record(e):
            # Clear entry boxes
            itemId_entry.delete(0, END)
            warranty_entry .delete(0, END)
            c_entry.delete(0, END)
            ss_entry.delete(0, END)
            m_entry.delete(0, END)
            pd_entry.delete(0,END)
            

            # Grab record Number
            selected = my_tree.focus()
            # Grab record values
            values = my_tree.item(selected, 'values')


            itemId = values[0]
            print(itemId)
            warranty = values[8]
            
            # outpus to entry boxes
            itemId_entry.insert(0, values[0])
            c_entry.insert(0, values[1])
            m_entry.insert(0, values[2])
            pd_entry.insert(0,values[10])
            
            warranty_entry.insert(0, values[8])
            ss_entry.insert(0, values[9])
            


    #buttons
    button_frame = LabelFrame(root, text="")
    button_frame.pack(fill="x", expand="yes", padx=20)
    
    update_button = Button(button_frame, text="Request service",command=lambda: customerRequestService(username,itemId_entry.get()))
    update_button.grid(row=0, column=0, padx=10, pady=10)

    select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
    select_record_button.grid(row=0, column=7, padx=10, pady=10)

    # Bind the treeview
    my_tree.bind("<ButtonRelease-1>",select_record)

    query_database(username,my_tree)

#TEST CASES
conn = sqlite3.connect('OSHE') 
c = conn.cursor()
sql = open('oshe.sql', 'r')
sqlfile = sql.read()
sql.close()
sqlQueries = sqlfile.split(';')
for query in sqlQueries:
    c.execute(query)
customerPurchaseItem("1234567890","1001","01012020","Unsold")
customerPurchaseItem("1234567890","1002","01012020","Unsold")
customerPurchaseItem("1234567890","1003","01012020","Unsold")
customerPurchaseItem("1234567893","1004","01012020","Unsold")
custTable("1234567890")
