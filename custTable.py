from tkinter import *
from tkinter import ttk

import sqlite3
import json
import numpy as np
import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine



def query_database():
	# Create a database or connect to one that exists
	conn = sqlite3.connect('OSHE')

	# Create a cursor instance
	c = conn.cursor()

	c.execute("SELECT ItemID, PurchaseDate FROM Item where CustomerID =?",username)
	records = c.fetchall()
	
	# Add our data to the screen
	global count
	count = 0
	
	#for record in records:
	#	print(record)


	for record in records:
		if count % 2 == 0:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[4], record[5], record[6], record[7]), tags=('evenrow',))
		else:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[4], record[5], record[6], record[7]), tags=('oddrow',))
		# increment counter
		count += 1


	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()

def custTable():
    #initializing screen
    root = Tk()
    root.title('Past purchases')
    root.geometry("1000x500")
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
    
    update_button = Button(button_frame, text="Request service")
    update_button.grid(row=0, column=0, padx=10, pady=10)

    select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
    select_record_button.grid(row=0, column=7, padx=10, pady=10)

    # Bind the treeview
    #my_tree.bind("", select_record)
    query_database()
    
#custTable()
