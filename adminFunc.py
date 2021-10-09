from tkinter import *
from tkinter import ttk

import sqlite3
import json
import numpy as np
import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine

def inventoryfunct():
    pass
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
        
    inventoryfunct()
#itemSold()

def query_database(username):
        conn = sqlite3.connect('oshes')
        c = conn.cursor()
        sql = "SELECT s.RequestID, s.ServiceStatus,r.CustomerID, r.ItemID, r.RequestStatus From Service s JOIN Request r ON  s.RequestID = r.RequestID"
        c.execute(sql)
        Records = c.fetchall()

        # Add our data to the screen
        global count
        count = 0

        #for record in records:
        #	print(record)


        for record in Records:
                if count % 2 == 0:
                        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3]), tags=('evenrow',))
                else:
                        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3]), tags=('oddrow',))
                # increment counter
                count += 1


        # Commit changes
        conn.commit()


def adminServiceTable(*username):
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
            iid_entry.delete(0, END)
            rs_entry.delete(0,END)
            
            
    def select_record(e):
            # Clear entry boxes
            itemId_entry.delete(0, END)
            reqId_entry.delete(0, END)
            ss_entry.delete(0, END)
            cID_entry.delete(0, END)
            iid_entry.delete(0, END)
            rs_entry.delete(0,END)
            

            # Grab record Number
            selected = my_tree.focus()
            # Grab record values
            values = my_tree.item(selected, 'values')
            
            itemId = values[0]
            warranty = values[8]
            
            # outputs to entry boxes
            reqId_entry.insert(0, values[0])
            itemId_entry.insert(0, values[1])
            ss_entry.insert(0, values[2])
            cID_entry.insert(0,values[3])
            
            itemId_entry.insert(0, values[4])
            rs_entry.insert(0, values[5])

    def adminApproveRequest(RequestID):
        pass

    def adminServiceRequest(RequestID):
        pass

                
        


    #buttons
    button_frame = LabelFrame(root, text="")
    button_frame.pack(fill="x", expand="yes", padx=20)
    
    cancel_button = Button(button_frame, text="Approve request", command=lambda:adminApproveRequest(reqId_entry.get()))
    cancel_button.grid(row=0, column=0, padx=10, pady=10)

    pay_button = Button(button_frame, text="Service request", command=lambda:adminServiceRequest(reqId_entry.get()))
    pay_button.grid(row=0, column=5, padx=10, pady=10)
    
    clear_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
    clear_record_button.grid(row=0, column=7, padx=10, pady=10)

    # Bind the treeview
    #my_tree.bind("", select_record)
    query_database(username)
    
#adminServiceTable()

def unpaidCustomer():
        conn = sqlite3.connect('oshes')
        c = conn.cursor()
        sql = "SELECT Request.CustomerID, Request.RequestID, ServiceFee.ServiceFee ,ServiceFee.SettlementDate From Request JOIN ServiceFee ON  Request.RequestID = ServiceFee.RequestID WHERE Request.RequestStatus = 'Submitted and Waiting for payment'"
        c.execute(sql)
        Records = c.fetchall()

        # Add our data to the screen
        global count
        count = 0

        #for record in records:
        #	print(record)


        for record in Records:
                if count % 2 == 0:
                        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2]), tags=('evenrow',))
                else:
                        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2]), tags=('oddrow',))
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
        
    unpaidCustomer()

#unpaidCust()

