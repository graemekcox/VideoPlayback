from Tkinter import *

class loginScreen:
    
    def login(self):
        self.username=self.v1.get()
        self.password=self.v2.get()
        if self.username == "cedric":
            if self.password == "woo":
                root.destroy()
            else:
                print("Incorrect Username/Password")
        else: 
            print("Incorrect Username/Password")
    def close(self):
        root.destroy()
    
    def __init__(self,master):

        self.v1 = StringVar()
        self.v2 = StringVar()
        self.v1.set("")
        self.v2.set("")
        self.label_1 = Label(master, text="Username")
        self.label_1.grid(row=0)
        self.entry_1 = Entry(master, textvariable = self.v1)
        self.entry_1.grid(row=0,column=1)

        self.label_2 = Label(master, text="Password")
        self.label_2.grid(row=1)
        self.entry_2 = Entry(master, textvariable = self.v2)
        self.entry_2.grid(row=1,column=1)

        self.button1 = Button(master,text="Login", command=self.login)
        self.button1.grid(row=2)
        self.button2 = Button(master, text="Close", command=self.close)
        self.button2.grid(row=2,column=1)

   
root = Tk()
b = loginScreen(root)
root.mainloop()
