import tkinter as tk
import sqlite3
import json
import pandas as pd
import numpy as np

##connection and addAdmin##
conn = sqlite3.connect('OSHE') 
c = conn.cursor()
sql = open('oshe.sql', 'r')
sqlfile = sql.read()
sql.close()
sqlQueries = sqlfile.split(';')
for query in sqlQueries:
    c.execute(query)
## end

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        self.masteruser = ""

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
        master.masteruser = username
        

        passwordLabel = tk.Label(self,text = "Password: ", font = ("bold", 10))
        passwordLabel.pack()
        password = tk.StringVar()
        passwordEntry = tk.Entry(self,textvariable=password, show="*", font = ("bold", 10))
        passwordEntry.pack(pady=10)
        
        ##INCLUDED MASTER AS PARMS
        tk.Button(self, text='LOGIN' , width=20,bg="black",fg='white',command= self.validLogin(master)).pack(pady = 10)
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

        check_query = "SELECT * FROM Administrator WHERE AdminID=? AND Password=?"
        if check == 2:
            try:
                c.execute(check_query,(username.get(),password.get()))
              
                row = c.fetchone()
                if row == None:
                    problem +="\n"
                    problem += "Invalid login information"
                    messagebox.showerror(title="ERROR",message=problem)
                else:
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
        master.masteruser = username
        

        passwordLabel = tk.Label(self,text = "Password: ", font = ("bold", 10))
        passwordLabel.pack()
        password = tk.StringVar()
        passwordEntry = tk.Entry(self,textvariable=password, show="*", font = ("bold", 10))
        passwordEntry.pack(pady=10)
        

        tk.Button(self, text='LOGIN' , width=20,bg="black",fg='white',command= self.validLogin(master)).pack(pady = 10)
        tk.Button(self, text='BACK' , width=20,bg="black",fg='white',command= lambda: master.switch_frame(StartPage)).pack()
        
class CustomerRegistration(tk.Frame):
    def validRegistration(self):
        self.output_label = tk.Label(self)
        self.output_label.pack()
        self.output_label.config(text= name.get() + "'s Registration as Customer successful")
        val = ("1234567890", name.get(), add.get(), gender.get(), email.get(), number.get(), password.get())
        sql = "INSERT INTO Customer (CustomerID, CustomerName, Gender, EmailAddress, PhoneNumber, Password) VALUES " + str(val) + ";"
        c.execute(sql)

    def __init__(self, master):
        global name
        global add
        global gender
        global email
        global number
        global password
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Administrator Registration", width = 20, font=("bold",20)).pack()

        #accept input string text from user
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

        #change this code to iterate and find avail codes
        ID = "1234567890"
        #
        tk.Button(self, text='REGISTER' , width=20,bg="black",fg='white',command= self.validRegistration).pack(pady = 10)
        tk.Button(self, text='BACK' , width=20,bg="black",fg='white',command= lambda: master.switch_frame(StartPage)).pack()

class AdminRegistration(tk.Frame):
    def validRegistration(self):
        self.output_label = tk.Label(self)
        self.output_label.pack()
        self.output_label.config(text= name.get() + "'s Registration as Administrator successful")
        #start changes#
        val = ("1234567890", name.get(), gender.get(), number.get(), password.get())
        sql = "INSERT INTO Customers(CustomerID, CustomerName, Address, Gender, EmailAddress, PhoneNumber, Password) VALUES" + str(val) + ";" 
        c.execute(sql)
        #end changes#

    def __init__(self, master):
        global name
        global gender
        global number
        global password
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Administrator Registration", width = 20, font=("bold",20)).pack()

        #accept input string text from user
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

        #change this code to iterate and find avail codes
        ID = "1234567890"
        #
        tk.Button(self, text='REGISTER' , width=20,bg="black",fg='white',command= self.validRegistration).pack(pady = 10)
        tk.Button(self, text='BACK' , width=20,bg="black",fg='white',command= lambda: master.switch_frame(StartPage)).pack()
        
class CustomerHomepage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.username = master.masteruser.get()
        tk.Label(self, text="Welcome, " + self.username + "!", width = 20, font=("bold",20)).pack()
    
class AdminHomepage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.username = master.masteruser.get()
        tk.Label(self, text="Welcome, " + self.username + "!", width = 20, font=("bold",20)).pack()
       
if __name__ == "__main__":
    app = SampleApp()
    app.title("OSHES System")
    # The size of the window
    app.geometry("700x400")
    app.mainloop()
