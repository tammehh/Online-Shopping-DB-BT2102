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

class sqlFunc():
    def addAdmin(ID, name, gender, number, pw):
        val = (ID, name, gender, number, pw)
        sql = "INSERT INTO Administrator (AdministratorID, AdminName, Gender, PhoneNumber, Password) VALUES " + str(val) + ";"
        c.execute(sql)
        return "done"
    def addCustomer(ID, name, address, gender, email, number, pw):
        val = (ID, name, address, gender, email, number, pw)
        sql = "INSERT INTO Customers(CustomerID, CustomerName, Address, Gender, EmailAddress, PhoneNumber, Password) VALUES" + str(val) + ";" 
        c.execute(sql)
        return "done"

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        self.allUserId = ()

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #headings for the page
        tk.Label(self,text="Welcome to OSHES", width=20,font=("Bold",20,)).pack()

        #interactive buttons
        tk.Button(self, text='Customer Login' , width=20,bg="green",fg='white',command= lambda: master.switch_frame(CustLogin)).pack(padx=10,pady=10)
        tk.Button(self, text='Admin Login' , width=20,bg="orange",fg='white',command= lambda: master.switch_frame(AdminLogin)).pack(padx=10,pady=10)
        tk.Button(self, text='Customer Register' , width=20,bg="blue",fg='white',command= lambda: master.switch_frame(CustomerRegistration)).pack(padx=10,pady=10)
        tk.Button(self, text='Admin Register' , width=20,bg= "black",fg='white',command= lambda: master.switch_frame(AdminRegistration)).pack(padx=10,pady=10)
       
class CustomerRegistration(tk.Frame):
    def validRegistration(self):
        problem = ""
        check = 0 
        if username.get() == "":
            problem += "\n"
            problem += "Please enter username"
        else:
            if username.get() in self.master.allUserId:
                problem += "\n"
                problem += "Please enter another username"
            else:
                self.master.allUserId += (username.get(),)
                check += 1
        if name.get() == "":
            problem += "\n"
            problem += "Please enter name"
        else:
            check += 1
        if add.get() == "":
            problem += "\n"
            problem += "Please enter address"
        else:
            check += 1    
        if gender.get() == "":
            problem += "\n"
            problem += "Please enter gender"
        elif gender.get() != "M" and gender.get() != "F":
            problem += "\n"
            problem += "Please enter M or F only"
        else:
            check += 1    
        if email.get() == "":
            problem += "\n"
            problem += "Please enter email"
        #elif (".com" or "@") not in email.get():
        #    problem += "\n"
        #    problem += "Please enter valid email address"
        else:
            check += 1
        if number.get() == "":
            problem += "\n"
            problem += "Please enter number"
        else:
            check += 1    
        if password.get() == "":
            problem += "\n"
            problem += "Please enter password"
        else:
            check += 1    
        if(problem != ""):
            return messagebox.showerror(title="ERROR",message=problem)
        self.output_label = tk.Label(self)
        self.output_label.pack()
        self.output_label.config(text= name.get() + "'s Registration as Customer successful")
        val = (username.get(), name.get(), add.get(), gender.get(), email.get(), number.get(), password.get())
        sql = "INSERT INTO Customers (CustomerID, CustomerName, Address, Gender, EmailAddress, PhoneNumber, Password) VALUES " + str(val) + ";"
        c.execute(sql)
        conn.commit()

    def __init__(self, master):
        global username
        global name
        global add
        global gender
        global email
        global number
        global password
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Customer Registration", width = 20, font=("bold",20)).pack()

        #accept input string text from user
        usernameLabel = tk.Label(self,text = "Username: ", font = ("bold", 10))
        usernameLabel.pack()
        username = tk.StringVar()
        usernameEntry = tk.Entry(self,textvariable=username, font = ("bold", 10))
        usernameEntry.pack(pady=10)
        
        nameLabel = tk.Label(self,text = "Name: ", font = ("bold", 10))
        nameLabel.pack()
        name = tk.StringVar()
        nameEntry = tk.Entry(self,textvariable=name, font = ("bold", 10))
        nameEntry.pack(pady=10)

        addLabel = tk.Label(self,text = "Address: ", font = ("bold", 10))
        addLabel.pack()
        add = tk.StringVar()
        addEntry = tk.Entry(self,textvariable=add, font = ("bold", 10))
        addEntry.pack(pady=10)

        genderLabel = tk.Label(self,text = "Gender (M/F): ", font = ("bold", 10))
        genderLabel.pack()
        gender = tk.StringVar()
        genderEntry = tk.Entry(self,textvariable=gender, font = ("bold", 10))
        genderEntry.pack(pady=10)

        emailLabel = tk.Label(self,text = "Email Address: ", font = ("bold", 10))
        emailLabel.pack()
        email = tk.StringVar()
        emailEntry = tk.Entry(self,textvariable=email, font = ("bold", 10))
        emailEntry.pack(pady=10)
        
        numberLabel = tk.Label(self,text = "Phone Number: ", font = ("bold", 10))
        numberLabel.pack()
        number = tk.StringVar()
        numberEntry = tk.Entry(self,textvariable=number, font = ("bold", 10))
        numberEntry.pack(pady=10)

        passwordLabel = tk.Label(self,text = "Password: ", font = ("bold", 10))
        passwordLabel.pack()
        password = tk.StringVar()
        passwordEntry = tk.Entry(self,textvariable=password, font = ("bold", 10))
        passwordEntry.pack(pady=10)

        tk.Button(self, text='REGISTER' , width=20,bg="black",fg='white',command= self.validRegistration).pack(pady = 10)
        tk.Button(self, text='BACK' , width=20,bg="black",fg='white',command= lambda: master.switch_frame(StartPage)).pack()

class AdminRegistration(tk.Frame):
    def validRegistration(self):
        problem = ""
        check = 0 
        if username.get() == "":
            problem += "\n"
            problem += "Please enter username"
        else:
            if username.get() in self.master.allUserId:
                problem += "\n"
                problem += "Please enter another username"
            else:
                self.master.allUserId += (username.get(),)
                check += 1
        if name.get() == "":
            problem += "\n"
            problem += "Please enter name"
        else:
            check += 1
        if gender.get() == "":
            problem += "\n"
            problem += "Please enter gender"
        elif gender.get() != "M" and gender.get() != "F":
            problem += "\n"
            problem += "Please enter M or F as Gender only"
        else:
            check += 1    
        if number.get() == "":
            problem += "\n"
            problem += "Please enter number"
        else:
            check += 1    
        if password.get() == "":
            problem += "\n"
            problem += "Please enter password"
        else:
            check += 1    
        if(problem != ""):
            return messagebox.showerror(title="ERROR",message=problem)
        self.output_label = tk.Label(self)
        self.output_label.pack()
        self.output_label.config(text= name.get() + "'s Registration as Administrator successful")
        #start changes#
        val = (username.get(), name.get(), gender.get(), number.get(), password.get())
        sql = "INSERT INTO Administrator (AdministratorID, AdminName, Gender, PhoneNumber, Password) VALUES" + str(val) + ";" 
        c.execute(sql)
        #end changes#

    def __init__(self, master):
        global username
        global name
        global gender
        global number
        global password
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Administrator Registration", width = 20, font=("bold",20)).pack()

        #accept input string text from user
        usernameLabel = tk.Label(self,text = "Username: ", font = ("bold", 10))
        usernameLabel.pack()
        username = tk.StringVar()
        usernameEntry = tk.Entry(self,textvariable=username, font = ("bold", 10))
        usernameEntry.pack(pady=10)
        
        nameLabel = tk.Label(self,text = "Name: ", font = ("bold", 10))
        nameLabel.pack()
        name = tk.StringVar()
        nameEntry = tk.Entry(self,textvariable=name, font = ("bold", 10))
        nameEntry.pack(pady=10)

        genderLabel = tk.Label(self,text = "Gender (M/F): ", font = ("bold", 10))
        genderLabel.pack()
        gender = tk.StringVar()
        genderEntry = tk.Entry(self,textvariable=gender, font = ("bold", 10))
        genderEntry.pack(pady=10)
        
        numberLabel = tk.Label(self,text = "Phone Number: ", font = ("bold", 10))
        numberLabel.pack()
        number = tk.StringVar()
        numberEntry = tk.Entry(self,textvariable=number, font = ("bold", 10))
        numberEntry.pack(pady=10)

        passwordLabel = tk.Label(self,text = "Password: ", font = ("bold", 10))
        passwordLabel.pack()
        password = tk.StringVar()
        passwordEntry = tk.Entry(self,textvariable=password, font = ("bold", 10))
        passwordEntry.pack(pady=10)

        
        tk.Button(self, text='REGISTER' , width=20,bg="black",fg='white',command= self.validRegistration).pack(pady = 10)
        tk.Button(self, text='BACK' , width=20,bg="black",fg='white',command= lambda: master.switch_frame(StartPage)).pack()
     
        
class CustLogin(tk.Frame):
    def validLogin(self):
        problem = ""
        check = 0 
        if username.get() == "":
            problem += "\n"
            problem += "Please enter username"
        else:
            check += 1
        if password.get() == "":
            problem += "\n"
            problem += "Please enter password"
        else:
            check += 1
        if(problem != ""):
            return messagebox.showerror(title="ERROR",message=problem)

        check_query = "SELECT * FROM Customers WHERE CustomerID=? AND Password=?"
        if check == 2:
            try:
                c.execute(check_query,(username.get(),password.get()))
              
                row = c.fetchone()
                if row == None:
                    problem +="\n"
                    problem += "Invalid login information"
                    messagebox.showerror(title="ERROR",message=problem)
                else:
                    global customerName
                    global custId
                    custId = row[0]
                    customerName = row[1]
                    messagebox.showinfo(message="Successful login, Welcome " + customerName)
                    self.master.switch_frame(custHome)
            except Exception as e:
                messagebox.showerror(title="ERROR",message="SystemERROR")
            


    def __init__(self, master):
        global username
        global password
        tk.Frame.__init__(self, master)
        tk.Label(self,text="Customer Login", width=20,font=("bold",20)).pack()
        
        
        #this will accept the input string text from the user.
        usernameLabel = tk.Label(self,text = "User ID: ", font = ("bold", 10))
        usernameLabel.pack()
        username = tk.StringVar()
        usernameEntry = tk.Entry(self,textvariable=username, font = ("bold", 10))
        usernameEntry.pack(pady=10)
        

        passwordLabel = tk.Label(self,text = "Password: ", font = ("bold", 10))
        passwordLabel.pack()
        password = tk.StringVar()
        passwordEntry = tk.Entry(self,textvariable=password, show="*", font = ("bold", 10))
        passwordEntry.pack(pady=10)
        

        tk.Button(self, text='LOGIN' , width=20,bg="black",fg='white',command= self.validLogin).pack(pady = 10)
        tk.Button(self, text='BACK' , width=20,bg="black",fg='white',command= lambda: master.switch_frame(StartPage)).pack()
    
class AdminLogin(tk.Frame):
    def validLogin(self):
        problem = ""
        check = 0 
        if username.get() == "":
            problem += "\n"
            problem += "Please enter username"
        else:
            check += 1
        if password.get() == "":
            problem += "\n"
            problem += "Please enter password"
        else:
            check += 1
        if(problem != ""):
            return messagebox.showerror(title="ERROR",message=problem)

        check_query = "SELECT * FROM Administrator WHERE AdministratorID=? AND Password=?"
        if check == 2:
            try:
                c.execute(check_query,(username.get(),password.get()))

                row = c.fetchone()
                if row == None:
                    problem +="\n"
                    problem += "Invalid login information"
                    messagebox.showerror(title="ERROR",message=problem)
                else:
                    global adminID
                    global adminName
                    adminID = row[0]
                    adminName = row[1]
                    messagebox.showinfo(message="Successful login, Welcome " + adminName)
                    self.master.switch_frame(adminHome)
            except Exception as e:
                messagebox.showerror(title="ERROR",message="SystemERROR")
        

    def __init__(self, master):
        global username
        global password
        tk.Frame.__init__(self, master)
        tk.Label(self,text="Admin Login", width=20,font=("bold",20)).pack()
        
        
        #this will accept the input string text from the user.
        usernameLabel = tk.Label(self,text = "User ID: ", font = ("bold", 10))
        usernameLabel.pack()
        username = tk.StringVar()
        usernameEntry = tk.Entry(self,textvariable=username, font = ("bold", 10))
        usernameEntry.pack(pady=10)
        

        passwordLabel = tk.Label(self,text = "Password: ", font = ("bold", 10))
        passwordLabel.pack()
        password = tk.StringVar()
        passwordEntry = tk.Entry(self,textvariable=password, show="*", font = ("bold", 10))
        passwordEntry.pack(pady=10)
        

        tk.Button(self, text='LOGIN' , width=20,bg="black",fg='white',command= self.validLogin).pack(pady = 10)
        tk.Button(self, text='BACK' , width=20,bg="black",fg='white',command= lambda: master.switch_frame(StartPage)).pack()


class custHome(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #headings for the page
        welcome = "Welcome " + customerName 
        tk.Label(self,text=welcome, width=20,font=("Bold",30),fg="white",bg="Light blue").pack()

        #interactive buttons
        #Search page to search for items
        tk.Button(self, text='Search/Buy products' , width=20,bg="grey",fg='white',command=lambda: master.switch_frame(searchpage)).pack(pady=5)
        
        #past purchase has a tree view table along with the option to request a service for a product
        tk.Button(self, text='Past purchase' , width=20,bg="orange",fg='white',command= custTable ).pack(pady=5)
        
        tk.Button(self, text='Existing requests' , width=20,bg="orange",fg='white',command= lambda: master.switch_frame(AdminLogin)).pack(pady=5)
        tk.Button(self, text='Payments' , width=20,bg="grey",fg='white',command= lambda: master.switch_frame(CustLogin)).pack(pady=5)
        
        tk.Button(self, text='LOGOUT' , width=20,bg="blue",fg='white',command= lambda: master.switch_frame(StartPage)).pack(pady=5)

    
    
class adminHome(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #headings for the page
        welcome = "Welcome administrator: " +  adminName  
        tk.Label(self,text=welcome, width=20,font=("Bold",30),fg="white",bg="Light blue").pack()

        #interactive buttons
        tk.Button(self, text='Search products' , width=20,bg="grey",fg='white',command=lambda: master.switch_frame(adminSearchPage)).pack(pady=5)
        tk.Button(self, text='Inventory' , width=20,bg="orange",fg='white',command= itemSold).pack(pady=5)
        tk.Button(self, text='Current Request' , width=20,bg="blue",fg='white',command= adminServiceTable).pack(pady=5)
        tk.Button(self, text='Unpaid Customers' , width=20,bg= "black",fg='white',command= unpaidCust).pack(pady=5)
  

#NEED to add in search functions
class searchpage(tk.Frame):
    #display result of search in seperate screen incomplete
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Label(self, 
                 text="""Simple Search""",
                 justify = tk.LEFT,
                 padx = 20,font="bold").pack()
        tk.Label(self, 
                 text="""Category:""",
                 justify = tk.LEFT,
                 padx = 20).pack()
        OPTIONScat = [
        "None","Lights", "Locks"
        ] 
        category = tk.StringVar(self)
        category.set(OPTIONScat[0]) # default value
        catOption = tk.OptionMenu(self, category, *OPTIONScat)
        catOption.pack()

        tk.Label(self, 
                 text="""Model:""",
                 justify = tk.LEFT,
                 padx = 20).pack()

        OPTIONSm = [
        "None","Light1", "Light2", "SmartHome1","Safe1", "Safe2", "Safe3"
        ] 

        model = tk.StringVar(self)
        model.set(OPTIONSm[0]) # default value

        modelOption = tk.OptionMenu(self, model, *OPTIONSm)
        modelOption.pack()


        tk.Label(self, 
                 text="""Advanced Search""",
                 justify = tk.LEFT,
                 padx = 20,font="bold").pack()

        tk.Label(self, 
                 text="""price:""",
                 justify = tk.LEFT,
                 padx = 20).pack()

        OPTIONS = [
        "None",
        "0-100",
        "100-200",
        "200-300"
        ] 

        price = tk.StringVar(self)
        price.set(OPTIONS[0]) # default value

        priceOption = tk.OptionMenu(self, price, *OPTIONS)
        priceOption .pack()

        #colour
        tk.Label(self, 
                 text="""colour:""",
                 justify = tk.LEFT,
                 padx = 20).pack()

        OPTIONSc = [
         "None", "Blue","Yellow", "Green", "Black"
        ] 

        col = tk.StringVar(self)
        col.set(OPTIONSc[0]) # default value

        colOption = tk.OptionMenu(self, col, *OPTIONSc)
        colOption .pack()

        #Factory
        tk.Label(self, 
                 text="""factory:""",
                 justify = tk.LEFT,
                 padx = 20).pack()

        OPTIONSf = [
         "None", "Malaysia", "China", "Philippines"
        ] 

        fac = tk.StringVar(self)
        fac.set(OPTIONSf[0]) # default value

        facOption = tk.OptionMenu(self, fac, *OPTIONSf)
        facOption .pack()

        #power supply option
        tk.Label(self, 
                 text="""Power supply:""",
                 justify = tk.LEFT,
                 padx = 20).pack()

        OPTIONSp = [
         "None", "Battery", "USB"
        ] 

        ps = tk.StringVar(self)
        ps.set(OPTIONSp[0]) # default value

        psOption = tk.OptionMenu(self, ps, *OPTIONSp)
        psOption .pack()

        #Production year
        tk.Label(self, 
                 text="""Production Year:""",
                 justify = tk.LEFT,
                 padx = 20).pack()

        OPTIONSpy = [
         "None", "2014", "2015","2016", "2017", "2018", "2019", "2020"
        ] 

        py = tk.StringVar(self)
        py.set(OPTIONSpy[0]) # default value

        pyOption = tk.OptionMenu(self, py, *OPTIONSpy)
        pyOption .pack()
        tk.Button(self, text='SUBMIT' , width=20,bg="black",fg='white').pack(pady=5)
        tk.Button(self, text='BACK' , width=20,bg="black",fg='white',command= lambda: master.switch_frame(custHome)).pack(pady=5)
        
#Replace with customer search after that part is done w function, include a item id search as well
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Label(self, 
                 text="""Simple Search""",
                 justify = tk.LEFT,
                 padx = 20,font="bold").pack()


        tk.Label(self, 
                 text="""Category:""",
                 justify = tk.LEFT,
                 padx = 20).pack()

        OPTIONScat = [
        "None","Lights", "Locks"
        ] 

        category = tk.StringVar(self)
        category.set(OPTIONScat[0]) # default value

        catOption = tk.OptionMenu(self, category, *OPTIONScat)
        catOption.pack()

        tk.Label(self, 
                 text="""Model:""",
                 justify = tk.LEFT,
                 padx = 20).pack()

        OPTIONSm = [
        "None","Light1", "Light2", "SmartHome1","Safe1", "Safe2", "Safe3"
        ] 

        model = tk.StringVar(self)
        model.set(OPTIONSm[0]) # default value

        modelOption = tk.OptionMenu(self, model, *OPTIONSm)
        modelOption.pack()


        tk.Label(self, 
                 text="""Advanced Search""",
                 justify = tk.LEFT,
                 padx = 20,font="bold").pack()

        tk.Label(self, 
                 text="""price:""",
                 justify = tk.LEFT,
                 padx = 20).pack()

        OPTIONS = [
        "None",
        "0-100",
        "100-200",
        "200-300"
        ] 

        price = tk.StringVar(self)
        price.set(OPTIONS[0]) # default value

        priceOption = tk.OptionMenu(self, price, *OPTIONS)
        priceOption .pack()

        #colour
        tk.Label(self, 
                 text="""colour:""",
                 justify = tk.LEFT,
                 padx = 20).pack()

        OPTIONSc = [
         "None", "Blue","Yellow", "Green", "Black"
        ] 

        col = tk.StringVar(self)
        col.set(OPTIONSc[0]) # default value

        colOption = tk.OptionMenu(self, col, *OPTIONSc)
        colOption .pack()

        #Factory
        tk.Label(self, 
                 text="""factory:""",
                 justify = tk.LEFT,
                 padx = 20).pack()

        OPTIONSf = [
         "None", "Malaysia", "China", "Philippines"
        ] 

        fac = tk.StringVar(self)
        fac.set(OPTIONSf[0]) # default value

        facOption = tk.OptionMenu(self, fac, *OPTIONSf)
        facOption .pack()

        #power supply option
        tk.Label(self, 
                 text="""Power supply:""",
                 justify = tk.LEFT,
                 padx = 20).pack()

        OPTIONSp = [
         "None", "Battery", "USB"
        ] 

        ps = tk.StringVar(self)
        ps.set(OPTIONSp[0]) # default value

        psOption = tk.OptionMenu(self, ps, *OPTIONSp)
        psOption .pack()

        #Production year
        tk.Label(self, 
                 text="""Production Year:""",
                 justify = tk.LEFT,
                 padx = 20).pack()

        OPTIONSpy = [
         "None", "2014", "2015","2016", "2017", "2018", "2019", "2020"
        ] 

        py = tk.StringVar(self)
        py.set(OPTIONSpy[0]) # default value

        pyOption = tk.OptionMenu(self, py, *OPTIONSpy)
        pyOption .pack()

        tk.Label(self,text = "Item ID ", font = ("bold", 10),justify = tk.LEFT).pack()
        itemID = tk.StringVar(self)
        itemIDEntry = tk.Entry(self,textvariable=itemID, show="*", font = ("bold", 10))
        itemIDEntry .pack(pady=10)
        
        tk.Button(self, text='SUBMIT' , width=20,bg="black",fg='white').pack(pady=5)
        tk.Button(self, text='BACK' , width=20,bg="black",fg='white',command= lambda: master.switch_frame(adminHome)).pack(pady=5)

                                                                                    
if __name__ == "__main__":
    conn = sqlite3.connect('OSHE') 
    c = conn.cursor()
    sql = open('oshe.sql', 'r')
    sqlfile = sql.read()
    sql.close()
    sqlQueries = sqlfile.split(';')
    for query in sqlQueries:
        c.execute(query)
    sqlFunc.addCustomer("1234567809","ben","assc","M","ascac","1234","123")
    app = App()
    app.title("OSHES System")
    # The size of the window
    app.geometry("700x600")
    app.mainloop()
