import mysql.connector
from mysql.connector import errorcode

import tkinter  as tk 
from tkinter import * 



cnx= mysql.connector.connect(user='root', password='root', host='127.0.0.1:8889', unix_socket= '/Applications/MAMP/tmp/mysql/mysql.sock', database = 'bloodbank')
cursor = cnx.cursor(buffered=True)

my_w = tk.Tk()
my_w.geometry("400x250") 
cursor.execute("SELECT * FROM donors")
i=0 
for donors in cursor: 
    for j in range(len(donors)):
        e = Label(my_w, width=10, text=donors[j]) 
        e.grid(row=i, column=j) 
        #e.insert(END, donors[j])
    i=i+1
my_w.mainloop()