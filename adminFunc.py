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
itemSold()
