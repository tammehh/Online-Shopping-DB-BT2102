from tkinter import *
from tkinter import ttk

import sqlite3
import json
import numpy as np
import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine
from tkinter import messagebox
from datetime import date

def inventoryfunct(my_tree):
    # Set up connection to mongoDB and DB object, instantiate a lst to store [model, count_sold, count_unsold]
    mongodb = MongoClient('localhost', 27017)
    db = mongodb.OSHES
    items = db["Items"]
    lst = []

    # Populate lst with [model, count_sold, count_unsold]
    models = ['Light1', 'Light2', 'SmartHome1', 'Safe1', 'Safe2', 'Safe3']
    for model in models:
        counts_sold = items.count_documents({'0.Model': model, '0.PurchaseStatus': "Sold"})
        counts_unsold = items.count_documents({'0.Model': model, '0.PurchaseStatus': "Unsold"})
        lst.append([model, counts_sold, counts_unsold])

    # Insert/Populate table in GUI using lst.
    global row_num
    row_num = 0
    for row in lst:
        if row_num % 2 == 0:
            my_tree.insert(parent='', index='end', iid=row_num, text='',
                           values=(row[0], row[1], row[2]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=row_num, text='',
                           values=(row[0], row[1], row[2]), tags=('oddrow',))
            # increment counter
        row_num += 1
    
    
#add in the funct to get sold and unsold
def itemSold():
    #initializing screen
    root = Tk()
    root.title('Inventory')
    root.geometry("600x300")
    
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
    my_tree['columns'] = ("IID","Number of 'SOLD' items", "Number of 'UNSOLD' items")                      

    # Format Our Columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("IID", anchor=CENTER, width=100)
    my_tree.column("Number of 'SOLD' items", anchor=CENTER, width=200)
    my_tree.column("Number of 'UNSOLD' items", anchor=CENTER, width=200)
    
    # Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("IID",text="IID", anchor=CENTER)
    my_tree.heading("Number of 'SOLD' items",text="Number of 'SOLD' items", anchor=CENTER)
    my_tree.heading("Number of 'UNSOLD' items", text="Number of 'UNSOLD' items", anchor=CENTER)


    # Create Striped Row Tags
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")                  
        
    inventoryfunct(my_tree)

#itemSold()

def query_database(username,my_tree):
        conn = sqlite3.connect('oshes')
        c = conn.cursor()
        sql = "SELECT  Distinct s.RequestID, s.ServiceStatus,r.CustomerID, r.ItemID, r.RequestStatus From Service s JOIN Request r ON  s.RequestID = r.RequestID"
        c.execute(sql)
        Records = c.fetchall()

        # Add our data to the screen
        global count
        count = 0

        #for record in records:
        #	print(record)


        for record in Records:
                if count % 2 == 0:
                        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3],record[4]), tags=('evenrow',))
                else:
                        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3],record[4]), tags=('oddrow',))
                # increment counter
                count += 1


        # Commit changes
        conn.commit()
        conn.close()


def adminServiceTable(username):
    #initializing screen
    root = Tk()
    root.title('adminServices')
    root.geometry("900x500")
    
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
    my_tree['columns'] = ("RequestID", "Service Status", "CustomerID", "ItemID","Request Status")                      

    # Format Our Columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("RequestID", anchor=CENTER, width=100)
    my_tree.column("Service Status", anchor=CENTER, width=130)
    my_tree.column("CustomerID", anchor=CENTER, width=100)
    my_tree.column("ItemID", anchor=CENTER, width=130)
    my_tree.column("Request Status", anchor=CENTER, width=100)


    # Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("RequestID",text="RequestID", anchor=CENTER)
    my_tree.heading("Service Status",text="Service Status", anchor=CENTER)
    my_tree.heading("CustomerID", text="CustomerID",anchor=CENTER)
    my_tree.heading("ItemID", text ="ItemID", anchor=CENTER)
    my_tree.heading("Request Status", text="Request Status", anchor=CENTER)


    # Create Striped Row Tags
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")
    
    data_frame = LabelFrame(root, text="Service information")
    data_frame.pack(fill="x", expand="yes", padx=10)

    reqId_label = Label(data_frame, text="RequestID")
    reqId_label.grid(row=0, column=0, padx=10, pady=10)
    reqId_entry = Entry(data_frame)
    reqId_entry.grid(row=0, column=1, padx=10, pady=10)


    ss_label = Label(data_frame, text="Service Status")
    ss_label.grid(row=0, column=2, padx=10, pady=10)
    ss_entry = Entry(data_frame)
    ss_entry.grid(row=0, column=3, padx=10, pady=10)

    cID_label = Label(data_frame, text="CustomerID")
    cID_label.grid(row=0, column=4, padx=10, pady=10)
    cID_entry = Entry(data_frame)
    cID_entry.grid(row=0, column=5, padx=10, pady=10)

    itemId_label = Label(data_frame, text="ItemID")
    itemId_label.grid(row=1, column=0, padx=10, pady=10)
    itemId_entry = Entry(data_frame)
    itemId_entry.grid(row=1, column=1, padx=10, pady=10)
    
    rs_label = Label(data_frame, text="Request Status")
    rs_label.grid(row=1, column=2, padx=10, pady=10)
    rs_entry = Entry(data_frame)
    rs_entry.grid(row=1, column=3, padx=10, pady=10)

    
    
    #Button functions
    def clear_entries():
            # Clear entry boxes
            itemId_entry.delete(0, END)
            reqId_entry.delete(0, END)
            ss_entry.delete(0, END)
            cID_entry.delete(0, END)
            rs_entry.delete(0,END)
            
            
    def select_record(e):
            # Clear entry boxes
            itemId_entry.delete(0, END)
            reqId_entry.delete(0, END)
            ss_entry.delete(0, END)
            cID_entry.delete(0, END)
            rs_entry.delete(0,END)
            

            # Grab record Number
            selected = my_tree.focus()
            # Grab record values
            values = my_tree.item(selected, 'values')
            
            itemId = values[0]
            
            # outputs to entry boxes
            reqId_entry.insert(0, values[0])
            itemId_entry.insert(0, values[3])
            ss_entry.insert(0, values[1])
            cID_entry.insert(0,values[2])
            rs_entry.insert(0, values[4])
 
    def administratorApprove(AdministratorID,RequestID, ItemID):
        if(rs_entry.get() == "Approved" or rs_entry_entry == "Completed"):
            return messagebox.showerror(title="ERROR",message="Service has already been approved/Completed")
        selected = my_tree.focus()
        mongodb = MongoClient('localhost', 27017)
        db = mongodb.OSHES
        conn = sqlite3.connect('oshes')
        c = conn.cursor()
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
        db.Items.update_one(myquery, newvalues))

        my_tree.item(selected, text="", values=(reqId_entry.get(),"In progress",cID_entry.get(),itemId_entry.get(),"Approved"))  
        itemId_entry.delete(0, END)
        reqId_entry.delete(0, END)
        ss_entry.delete(0, END)
        cID_entry.delete(0, END)
        rs_entry.delete(0,END) 
        
        return "done"

    def administratorCompleteService(RequestID, ItemID):
        if(rs_entry.get() == "Completed"):
            return messagebox.showerror(title="ERROR",message="Service has already been completed")
        selected = my_tree.focus()
        mongodb = MongoClient('localhost', 27017)
        db = mongodb.OSHES
        conn = sqlite3.connect('oshes')
        c = conn.cursor()        
        sql = "UPDATE Request SET RequestStatus = 'Completed' WHERE RequestID = ?"
        data = (RequestID,)
        c.execute(sql, data)
        conn.commit()
            
        myquery = { "0.ItemID": ItemID }
        newvalues = { "$set": { "0.ServiceStatus": "Completed"} }
        db.Items.update_one(myquery, newvalues)
        my_tree.item(selected, text="", values=(reqId_entry.get(),"Completed",cID_entry.get(),itemId_entry.get(),"Completed"))
        itemId_entry.delete(0, END)
        reqId_entry.delete(0, END)
        ss_entry.delete(0, END)
        cID_entry.delete(0, END)
        rs_entry.delete(0,END) 
           
        return "done"

                

    #buttons
    button_frame = LabelFrame(root, text="")
    button_frame.pack(fill="x", expand="yes", padx=20)
    
    cancel_button = Button(button_frame, text="Approve request", command=lambda:administratorApprove(username,reqId_entry.get(),itemId_entry.get()))
    cancel_button.grid(row=0, column=0, padx=10, pady=10)

    pay_button = Button(button_frame, text="Service request", command=lambda:administratorCompleteService(reqId_entry.get(),itemId_entry.get()))
    pay_button.grid(row=0, column=5, padx=10, pady=10)
    
    clear_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
    clear_record_button.grid(row=0, column=7, padx=10, pady=10)

    # Bind the treeview
    my_tree.bind("<ButtonRelease-1>", select_record)
    query_database(username,my_tree)
#testing treeview

#adminServiceTable("Admin123")

def unpaidCustomer(my_tree):
        sql = "SELECT Request.CustomerID, Request.RequestID, ServiceFee.ServiceFee ,ServiceFee.SettlementDate From Request JOIN ServiceFee ON  Request.RequestID = ServiceFee.RequestID WHERE Request.RequestStatus = 'Submitted and Waiting for payment'"
        c.execute(sql)
        # Add our data to the screen
        global count
        count = 0
        records = c.fetchall()
        #for record in records:
        	#print(record)


        for record in records:
                if count % 2 == 0:
                        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3]), tags=('evenrow',))
                else:
                        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3]), tags=('oddrow',))
                # increment counter
                count += 1


        # Commit changes
        conn.commit()
    
#add in the funct to get sold and unsold
def unpaidCust():
    #initializing screen
    root = Tk()
    root.title('Unpaid')
    root.geometry("600x300")
    
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
    my_tree['columns'] = ("CustomerID","RequestID", "ServiceFee","SettlementDate")                      

    # Format Our Columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("CustomerID", anchor=CENTER, width=100)
    my_tree.column("RequestID", anchor=CENTER, width=100)
    my_tree.column("ServiceFee", anchor=CENTER, width=100)
    my_tree.column("SettlementDate", anchor=CENTER, width=100)

    
    # Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("CustomerID",text="CustomerID", anchor=CENTER)
    my_tree.heading("RequestID",text="RequestID", anchor=CENTER)
    my_tree.heading("ServiceFee",text="ServiceFee", anchor=CENTER)
    my_tree.heading("SettlementDate",text="SettlementDate", anchor=CENTER)


    # Create Striped Row Tags
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")                  
        
    unpaidCustomer(my_tree)
#unpaidCust()

def cancelAllExpiredRequests():
    sql = "UPDATE Request SET RequestStatus = 'Cancelled' WHERE julianday('now') - julianday(RequestDate) > 10;"
    c.execute(sql)
    conn.commit()
    
    # Use to check if the expired request has been cancelled
    c.execute("SELECT * FROM REQUEST")
    print(c.fetchall())

