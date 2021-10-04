import tkinter as tk

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

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
        tk.Button(self, text='Customer Register' , width=20,bg="blue",fg='white',command= lambda: master.switch_frame(PageOne)).pack(padx=10,pady=10)
        tk.Button(self, text='Admin Register' , width=20,bg= "black",fg='white',command= lambda: master.switch_frame(AdminRegistration)).pack(padx=10,pady=10)

class CustLogin(tk.Frame):
    def validLogin(self):
        self.output_label = tk.Label(self)
        self.output_label.pack()
        self.output_label.config(text= username.get() + "Login successful")

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
        self.output_label = tk.Label(self)
        self.output_label.pack()
        self.output_label.config(text= username.get() + "Login successful")

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
        
class AdminRegistration(tk.Frame):
    def validRegistration(self):
        self.output_label = tk.Label(self)
        self.output_label.pack()
        self.output_label.config(text= name.get() + "'s Registration as Administrator successful")

    def addAdmin(ID, name, gender, number, pw):
        val = (ID, name, gender, number, pw)
        sql = "INSERT INTO Administrator (AdministratorID, AdminName, Gender, PhoneNumber, Password) VALUES " + str(val) + ";"
        c.execute(sql)
        self.validRegistration()
        
    def __init__(self, master):
        global name
        global gender
        global phone
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
        
        phoneLabel = tk.Label(self,text = "Phone Number: ", font = ("bold", 10))
        phoneLabel.pack()
        phone = tk.StringVar()
        phoneEntry = tk.Entry(self,textvariable=phone, font = ("bold", 10))
        phoneEntry.pack(pady=10)

        passwordLabel = tk.Label(self,text = "Password: ", font = ("bold", 10))
        passwordLabel.pack()
        password = tk.StringVar()
        passwordEntry = tk.Entry(self,textvariable=password, font = ("bold", 10))
        passwordEntry.pack(pady=10)

        #change this code to iterate and find avail ID
        ID = 1234567890
        #
        tk.Button(self, text='REGISTER' , width=20,bg="black",fg='white',command= self.validRegistration).pack(pady = 10)
        tk.Button(self, text='BACK' , width=20,bg="black",fg='white',command= lambda: master.switch_frame(StartPage)).pack()
    

if __name__ == "__main__":
    app = SampleApp()
    app.title("OSHES System")
    # The size of the window
    app.geometry("700x400")
    app.mainloop()
