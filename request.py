from tkinter import *
from tkinter import ttk

import sqlite3
import json
import numpy as np
import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine



def query_database(username):
        conn = sqlite3.connect('oshes')
        c = conn.cursor()
        sql = "SELECT Request.RequestID, Request.ItemID, Request.RequestStatus, ServiceFee.ServiceFee ,ServiceFee.SettlementDate From Request JOIN ServiceFee ON  Request.RequestID = ServiceFee.RequestID WHERE Request.CustomerID ='{username}'"
        c.execute(sql)
        Records = c.fetchall()

        # Add our data to the screen
        global count
        count = 0

        #for record in records:
        #	print(record)


        for record in Records:
                if count % 2 == 0:
                        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('evenrow',))
                else:
                        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('oddrow',))
                # increment counter
                count += 1


        # Commit changes
        conn.commit()


def serviceTable(*username):
    #initializing screen
    root = Tk()
    root.title('Services')
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
    my_tree['columns'] = ("RequestID","ItemID","Request Status","Request Date",
                          "Service Fee","Settlement Date")                      

    # Format Our Columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("RequestID", anchor=CENTER, width=100)
    my_tree.column("ItemID", anchor=CENTER, width=100)
    my_tree.column("Request Status", anchor=CENTER, width=130)
    my_tree.column("Request Date", anchor=CENTER, width=130)
    my_tree.column("Service Fee", anchor=CENTER, width=100)
    my_tree.column("Settlement Date", anchor=CENTER, width=130)


    # Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("RequestID",text="RequestID", anchor=CENTER)
    my_tree.heading("ItemID",text="ItemID", anchor=CENTER)
    my_tree.heading("Request Status", text="Request Status", anchor=CENTER)
    my_tree.heading("Request Date", text="Request Date",anchor=CENTER)
    my_tree.heading("Service Fee", text ="Service Fee", anchor=CENTER)
    my_tree.heading("Settlement Date", text="Settlement Date", anchor=CENTER)


    # Create Striped Row Tags
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")
    
    data_frame = LabelFrame(root, text="Service information")
    data_frame.pack(fill="x", expand="yes", padx=10)

    reqId_label = Label(data_frame, text="RequestID")
    reqId_label.grid(row=0, column=0, padx=10, pady=10)
    reqId_entry = Entry(data_frame)
    reqId_entry.grid(row=0, column=1, padx=10, pady=10)


    itemId_label = Label(data_frame, text="ItemID")
    itemId_label.grid(row=0, column=2, padx=10, pady=10)
    itemId_entry = Entry(data_frame)
    itemId_entry.grid(row=0, column=3, padx=10, pady=10)

    rs_label = Label(data_frame, text="Request Status")
    rs_label.grid(row=0, column=4, padx=10, pady=10)
    rs_entry = Entry(data_frame)
    rs_entry.grid(row=0, column=5, padx=10, pady=10)

    rd_label = Label(data_frame, text="Request Date")
    rd_label.grid(row=1, column=0, padx=10, pady=10)
    rd_entry = Entry(data_frame)
    rd_entry.grid(row=1, column=1, padx=10, pady=10)
    
    sd_label = Label(data_frame, text="Settlement Date")
    sd_label.grid(row=1, column=2, padx=10, pady=10)
    sd_entry = Entry(data_frame)
    sd_entry.grid(row=1, column=3, padx=10, pady=10)

    sf_label = Label(data_frame, text="Service Fee")
    sf_label.grid(row=1, column=4, padx=10, pady=10)
    sf_entry = Entry(data_frame)
    sf_entry.grid(row=1, column=5, padx=10, pady=10)
    
    
    #Button functions
    def clear_entries():
            # Clear entry boxes
            itemId_entry.delete(0, END)
            reqId_entry.delete(0, END)
            rs_entry.delete(0, END)
            sd_entry.delete(0, END)
            rd_entry.delete(0, END)
            sf_entry.delete(0,END)
            
            
    def select_record(e):
            # Clear entry boxes
            itemId_entry.delete(0, END)
            reqId_entry.delete(0, END)
            rs_entry.delete(0, END)
            sd_entry.delete(0, END)
            rd_entry.delete(0, END)
            sf_entry.delete(0,END)
            

            # Grab record Number
            selected = my_tree.focus()
            # Grab record values
            values = my_tree.item(selected, 'values')
            
            itemId = values[0]
            warranty = values[8]
            
            # outputs to entry boxes
            reqId_entry.insert(0, values[0])
            itemId_entry.insert(0, values[1])
            rs_entry.insert(0, values[2])
            rd_entry.insert(0,values[3])
            
            sd_entry.insert(0, values[4])
            sf_entry.insert(0, values[5])

    def customerPayService(RequestID, ItemID):
            conn = sqlite3.connect('OSHE')
            c = conn.cursor()
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

            itemId_entry.delete(0, END)
            reqId_entry.delete(0, END)
            rs_entry.delete(0, END)
            sd_entry.delete(0, END)
            rd_entry.delete(0, END)
            sf_entry.delete(0,END)

            return "done"

    def customerCancelRequest(RequestID):
            conn = sqlite3.connect('OSHE')
            c = conn.cursor()
            sql = "UPDATE Request SET RequestStatus = ‘Cancelled’ WHERE RequestID = ?"
            data = (RequestID,)
            c.execute(sql, data)
            conn.commit()

            itemId_entry.delete(0, END)
            reqId_entry.delete(0, END)
            rs_entry.delete(0, END)
            sd_entry.delete(0, END)
            rd_entry.delete(0, END)
            sf_entry.delete(0,END)

            return "Request Cancelled."

                
        


    #buttons
    button_frame = LabelFrame(root, text="")
    button_frame.pack(fill="x", expand="yes", padx=20)
    
    cancel_button = Button(button_frame, text="Cancel service", command=lambda:customerCancelRequest(reqId_entry.get()))
    cancel_button.grid(row=0, column=0, padx=10, pady=10)

    pay_button = Button(button_frame, text="Pay service", command=lambda:customerPayService(reqId_entry.get(), itemId_entry.get()))
    pay_button.grid(row=0, column=5, padx=10, pady=10)
    
    clear_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
    clear_record_button.grid(row=0, column=7, padx=10, pady=10)

    # Bind the treeview
    #my_tree.bind("", select_record)
    query_database(username)

#if __name__ == "__main__":
 #   conn = sqlite3.connect('oshes') 
  #  c = conn.cursor()
    #sql = open('oshe.sql', 'r')
    #sqlfile = sql.read()
    #sql.close()
    #mongodb = MongoClient('localhost', 27017)
   # db = mongodb.OSHES #db is oshes
  #  sqlQueries = sqlfile.split(';')
 #   for query in sqlQueries:
        #c.execute(query)
serviceTable("123")
