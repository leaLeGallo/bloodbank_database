import mysql.connector
import tkinter  as tk 
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as mb

r = tk.Tk()
r.geometry("600x600")
r.title("User detail")

connect = mysql.connector.connect(user='root', password='Ihtwasc?', host='127.0.0.1', database = 'Bloodbank')
conn = connect.cursor(buffered=True)

conn.execute("SELECT * from Donors")
tree = ttk.Treeview(r)
tree['show'] = 'headings'

s = ttk.Style(r)
s.theme_use("clam")
s.configure(".", font = ('Helvetica', 11))
s.configure("Treeview.Heading", foreground='red', font=('Helvetica', 11, "bold"))

tree["columns"] = ("donorsId", "firstName", "lastName", "dateOfBirth", "address", "phoneNumber", "email", "bloodType")

tree.column("firstName", width=50, minwidth=150, anchor=tk.CENTER)
tree.column("lastName", width=50, minwidth=150, anchor=tk.CENTER)
tree.column("dateOfBirth", width=50, minwidth=150, anchor=tk.CENTER)
tree.column("address", width=50, minwidth=150, anchor=tk.CENTER)
tree.column("phoneNumber", width=50, minwidth=150, anchor=tk.CENTER)
tree.column("email", width=50, minwidth=150, anchor=tk.CENTER)
tree.column("bloodType", width=50, minwidth=150, anchor=tk.CENTER)

tree.heading("firstName", text="First Name", anchor=tk.CENTER)
tree.heading("lastName", text="Last Name", anchor=tk.CENTER)
tree.heading("dateOfBirth", text="Date of birth", anchor=tk.CENTER)
tree.heading("address", text="address", anchor=tk.CENTER)
tree.heading("phoneNumber", text="phone number", anchor=tk.CENTER)
tree.heading("email", text="email", anchor=tk.CENTER)
tree.heading("bloodType", text="Blood Type", anchor=tk.CENTER)

i = 0
for ro in conn:
   tree.insert('', i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5], ro[6], ro[7]))
   i = i + 1

hsb = ttk.Scrollbar(r, orient="horizontal")
hsb.configure(command=tree.xview)
tree.configure(xscrollcommand=hsb.set)
hsb.pack(fill=X, side = BOTTOM)

vsb = ttk.Scrollbar(r, orient="vertical")
vsb.configure(command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
vsb.pack(fill=Y, side = RIGHT)

tree.pack()
firstName=tk.StringVar()
lastName=tk.StringVar()
dateOfBirth=tk.StringVar()
address=tk.StringVar()
phoneNumber=tk.StringVar()
email=tk.StringVar()
bloodType=tk.StringVar()

def add_data(tree):
   f=Frame(r, width=400, height=320, background="black")
   f.place(x=100, y=250)
   l1=Label(f, text="firstName", width=8, font=('Times', 11, 'bold'))
   e1=Entry(f, textvariable=firstName, width=15)
   l1.place(x=50, y=30)
   e1.place(x=170, y=30)
   
   l2=Label(f, text="lastName", width=8, font=('Times', 11, 'bold'))
   e2=Entry(f, textvariable=lastName, width=15)
   l2.place(x=50, y=70)
   e2.place(x=170, y=70)
   
   l3=Label(f, text="dateOfBirth", width=8, font=('Times', 11, 'bold'))
   e3=Entry(f, textvariable=dateOfBirth, width=15)
   l3.place(x=50, y=110)
   e3.place(x=170, y=110)
   
   l4=Label(f, text="address", width=8, font=('Times', 11, 'bold'))
   e4=Entry(f, textvariable=address, width=15)
   l4.place(x=50, y=150)
   e4.place(x=170, y=150)
   
   l5=Label(f, text="phoneNumber", width=8, font=('Times', 11, 'bold'))
   e5=Entry(f, textvariable=phoneNumber, width=15)
   l5.place(x=50, y=190)
   e5.place(x=170, y=190)
   
   l6=Label(f, text="email", width=8, font=('Times', 11, 'bold'))
   e6=Entry(f, textvariable=email, width=15)
   l6.place(x=50, y=230)
   e6.place(x=170, y=230)
   
   l7=Label(f, text="bloodType", width=8, font=('Times', 11, 'bold'))
   e7=Entry(f, textvariable=bloodType, width=15)
   l7.place(x=50, y=270)
   e7.place(x=170, y=270)
   
   def insert_data():
      nonlocal e1, e2, e3, e4, e5, e6, e7
      s_firstName = firstName.get()
      s_lastName = lastName.get()
      dob = dateOfBirth.get()
      add = address.get()
      phone = phoneNumber.get()
      e = email.get()
      bt = bloodType.get()
      conn.execute('INSERT INTO Donors(firstName, lastName, dateOfBirth, address, phoneNumber, email, bloodType) VALUES(%s,%s,%s,%s,%s,%s,%s)', (s_firstName, s_lastName, dob, add, phone, e, bt))
      print(conn.lastrowid)
      connect.commit()
      tree.insert('', 'end', text="", values=(conn.lastrowid, s_firstName, s_lastName, dob, add, phone, e, bt))
      mb.showinfo("Sucess", "donor registered")
      e1.delete(0, END)
      e2.delete(0, END)
      e3.delete(0, END)
      e4.delete(0, END)
      e5.delete(0, END)
      e6.delete(0, END)
      e7.delete(0, END)
      f.destroy()
      
      
   
   submitbutton = tk.Button(f, text="Submit", command= insert_data)
   submitbutton.configure(font=('Times', 11, 'bold'), bg='green', fg='white')
   submitbutton.place(x=100, y=300)
   
   cancelbutton = tk.Button(f, text="cancel", command=f.destroy)
   cancelbutton.configure(font=('Times', 11, 'bold'), bg='red', fg='white')
   cancelbutton.place(x=240, y=300)

def delete_data(tree):
   selected_item=tree.selection()[0]
   print(tree.item(selected_item)['values'])
   did=tree.item(selected_item)['values'][0]
   del_query="DELETE FROM Donors WHERE donorsID=%s"
   sel_data=(did,)
   conn.execute(del_query, sel_data)
   connect.commit()
   tree.delete(selected_item)
   mb.showinfo("Sucess", "donor deleted")

insertbutton = tk.Button(r, text="insert", command=lambda: add_data(tree))
insertbutton.configure(font = ('calabri', 14, 'bold'), bg = 'grey', fg = 'black')
insertbutton.place(x=200, y=260)

deletebutton = tk.Button(r, text="delete", command=lambda: delete_data(tree))
deletebutton.configure(font = ('calabri', 14, 'bold'), bg = 'grey', fg = 'black')
deletebutton.place(x=300, y=260)


r.mainloop()