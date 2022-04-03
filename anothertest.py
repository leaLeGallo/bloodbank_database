from bloodBank import *
import queries as q
from tkinter.ttk import *
import tkinter  as tk 
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as mb



cnx= mysql.connector.connect(user='root', password='root', host='127.0.0.1:8889', unix_socket= '/Applications/MAMP/tmp/mysql/mysql.sock')
cursor = cnx.cursor(buffered=True)
 

try:
    cursor.execute("USE {}".format(DATABASE_NAME)) # function to use database
except mysql.connector.Error as err:
    print("Database {} does not exist".format(DATABASE_NAME)) # if it does not exist
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        creating_databases(cursor, DATABASE_NAME)
        print("Database {} created succesfully.".format(DATABASE_NAME)) # if created
        cnx.database = DATABASE_NAME
        create_tables_donors(cursor) # calling functions
        insert_into_donors(cursor)
        create_tables_recipients(cursor)
        insert_into_recipients(cursor)
        create_tables_donations(cursor)
        insert_into_donations(cursor)
        create_tables_transfusions(cursor)
        insert_into_transfusions(cursor)
        create_stocks_view(cursor)
        top_saviours_view(cursor)
    else:
        print(err)
else:
    print("Database {} already exists".format(DATABASE_NAME))



# METHODS FOR THE APP

def retrieveTables():
    table = combo.get()
    newWindow = Tk()
    cursor.execute(q.show_table(table, cursor))
    headers = [e[0] for e in cursor.description]
    i = 1
    for table in cursor: 
        for j in range(len(table)):
            e = Entry(newWindow, width=10) 
            e.grid(row=i, column=j) 
            e.insert(END, table[j])
        i=i+1

def retrieveInfo():
    infoname = infoentry.get()
    infoWindow = Toplevel(window) # creat new window for info
    cursor.execute(q.findDonor(infoname, cursor))
    i = 1
    for infoname in cursor: 
        for j in range(len(infoname)):
            e = Entry(infoWindow, width=10) 
            e.grid(row=i, column=j) 
            e.insert(END, infoname[j])
        i=i+1

def retrieveNextDonation():
    name = nextdonentry.get()
    donationWindow = Toplevel(window) # new window for donation
    donationWindow.title(name) # title 
    nextdonlabel = Label( donationWindow,
    text = q.nextdonation(name, cursor) ) # call nextDonation
    donationWindow.geometry('300x100')
    nextdonlabel.grid(column=0, row=0)

def retrieveGiving():
    name = entergiving.get()
    givingWindow = Toplevel(window)
    givingWindow.title(name)
    lbl = Label( givingWindow,
    text = q.givingblood(name, cursor) )
    givingWindow.geometry('300x300')
    lbl.grid(column=0, row=0)

def insertToTables():
    name = combo.get()
    value = []
    text = q.insertrow(name, value, cursor)
    return text.append





tree = ttk.Treeview()


firstName=tk.StringVar()
lastName=tk.StringVar()
dateOfBirth=tk.StringVar()
address=tk.StringVar()
phoneNumber=tk.StringVar()
email=tk.StringVar()
bloodType=tk.StringVar()
 
def add_data(tree):
    r = Tk()
    tree = ttk.Treeview(r)
    cursor.execute("SELECT * from Donors")
    
    tree['show'] = 'headings'

    s = ttk.Style(window)
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
    for ro in cursor:
        tree.insert('', i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5], ro[6], ro[7]))
        i = i + 1
    
    tree.pack(ipadx='250', ipady='29')

    hsb = ttk.Scrollbar(r, orient="horizontal")
    hsb.configure(command=tree.xview)
    tree.configure(xscrollcommand=hsb.set)
    hsb.pack(fill=X, side = BOTTOM)

    vsb = ttk.Scrollbar(r, orient="vertical")
    vsb.configure(command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(fill=Y, side = RIGHT)
    r.geometry("1050x700")
    r.title("User detail")
    f=Frame(r, width=400, height=400, background="black")
    f.place(x=300, y=270)
    l1=Label(f, text="First name", width=12, font=('Times', 11, 'bold'))
    e1=Entry(f, textvariable=firstName, width=15)
    l1.place(x=50, y=30)
    e1.place(x=170, y=30)

    l2=Label(f, text="Last name", width=12, font=('Times', 11, 'bold'))
    e2=Entry(f, textvariable=lastName, width=15)
    l2.place(x=50, y=70)
    e2.place(x=170, y=70)

    l3=Label(f, text="Date of birth", width=12, font=('Times', 11, 'bold'))
    e3=Entry(f, textvariable=dateOfBirth, width=15)
    l3.place(x=50, y=110)
    e3.place(x=170, y=110)

    l4=Label(f, text="Address", width=12, font=('Times', 11, 'bold'))
    e4=Entry(f, textvariable=address, width=15)
    l4.place(x=50, y=150)
    e4.place(x=170, y=150)

    l5=Label(f, text="Phone number", width=12, font=('Times', 11, 'bold'))
    e5=Entry(f, textvariable=phoneNumber, width=15)
    l5.place(x=50, y=190)
    e5.place(x=170, y=190)

    l6=Label(f, text="Email", width=12, font=('Times', 11, 'bold'))
    e6=Entry(f, textvariable=email, width=15)
    l6.place(x=50, y=230)
    e6.place(x=170, y=230)

    l7=Label(f, text="Blood type", width=12, font=('Times', 11, 'bold'))
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
        cursor.execute('INSERT INTO Donors(firstName, lastName, dateOfBirth, address, phoneNumber, email, bloodType) VALUES(%s,%s,%s,%s,%s,%s,%s)', (s_firstName, s_lastName, dob, add, phone, e, bt))
        print(cursor.lastrowid)
        cnx.commit()
        tree.insert('', 'end', text="", values=(cursor.lastrowid, s_firstName, s_lastName, dob, add, phone, e, bt))
        mb.showinfo("Sucess", "donor registered")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
        e7.delete(0, END)
        f.destroy()

        
    deletebutton = tk.Button(f, text="delete", command=lambda: delete_data(tree))
    deletebutton.place(x=170, y=360)

    submitbutton = tk.Button(f, text="Submit", command= insert_data)
    submitbutton.configure(font=('Times', 11, 'bold'), bg='grey', fg='black')
    submitbutton.place(x=100, y=320)

    cancelbutton = tk.Button(f, text="cancel", command=f.destroy)
    cancelbutton.configure(font=('Times', 11, 'bold'), bg='grey', fg='black')
    cancelbutton.place(x=240, y=320)



def delete_data(tree):
   selected_item=tree.selection()[0]
   print(tree.item(selected_item)['values'])
   did=tree.item(selected_item)['values'][0]
   del_query="DELETE FROM Donors WHERE donorsID=%s"
   sel_data=(did,)
   cursor.execute(del_query, sel_data)
   cnx.commit()
   tree.delete(selected_item)
   mb.showinfo("Sucess", "donor deleted")

    



# THE APP

# Create the main window


window = Tk()
window.title("The Blood bank app") # window title
window.geometry('400x450') # window size


tablelabel = Label(window, text="Blood Bank Tables") # label for the tables
tablelabel.place(x=130, y=0) # label pos
# create a combox to choose tables from
combo = Combobox(window, state = 'readonly') # create combobox
combo['values']= ("Donors", "Recipients", "Donations", "Transfusions", "AvailableStocks", "Top3") #insert values to combobox
combo.set("Select Table") # begin with empty box'
combo.place(x=80, y=25) # pos of combobox
# create button, set button text to choose, set command to combo bind open new window and call retrievetables
tableButton = Button(window, text = "Choose", command = retrieveTables)
tableButton.place(x=150, y=50) # pos for button


# creating entry to insert firstName to find all information about donors
infolabel = Label(window, text="Search persons information by first name")
infolabel.place(x=60, y=85)
infoentry = Entry(window) # create entry
infoentry.place(x=90, y=110)
infoButton = Button(window, text = "Choose", command = infoentry.bind('<<openNewWindow>>', retrieveInfo))
infoButton.place(x=150, y=135)


# create entry to find when donors can donate next
nextdonlabel = Label(window, text="Can the person donate again by both name")
nextdonlabel.place(x=55, y=170)
nextdonentry = Entry(window)
nextdonentry.place(x=90, y=195)
nextdonButton = Button(window, text = "Choose", command = nextdonentry.bind('<<openNewWindow>>', retrieveNextDonation))
nextdonButton.place(x=150, y=220)


# create entry for gi
labelgiving = Label(window, text="Enter name of recipient to see who he can get blood from")
labelgiving.place(x=20, y=255)
entergiving = Entry(window)
entergiving.place(x=90, y=280)
nameButton = Button(window, text = "Choose", command = entergiving.bind('<<openNewWindow>>', retrieveGiving))
nameButton.place(x=150, y=305)


insert = Combobox(window, state = 'readonly') # create combobox
insert['values']= ("Donors", "Recipients", "Donations", "Transfusions") #insert values to combobox
insert.set("Select Table") # begin with empty box'
insert.place(x=80, y=340) # pos of combobox

manupbutton = tk.Button(window, text="insert", command=lambda: add_data(tree))
manupbutton.place(x=150, y=380)









window.mainloop()
