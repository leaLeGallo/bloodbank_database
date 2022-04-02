from bloodBank import *
import queries as q
from tkinter import *
from tkinter.ttk import *




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



# METHODS FOR THE APP THE APP 

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



import tkinter  as tk 
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as mb
 



# def Registrationform():
    # r = tk.Tk()
    # r.geometry("600x600")
    # r.title("User detail")

    

    # cursor.execute("SELECT * from Donors")
    # tree = ttk.Treeview(r)
    # tree['show'] = 'headings'

    # s = ttk.Style(r)
    # s.theme_use("clam")
    # s.configure(".", font = ('Helvetica', 11))
    # s.configure("Treeview.Heading", foreground='red', font=('Helvetica', 11, "bold"))

    # tree["columns"] = ("donorsId", "firstName", "lastName", "dateOfBirth", "address", "phoneNumber", "email", "bloodType")

    # tree.column("firstName", width=50, minwidth=150, anchor=tk.CENTER)
    # tree.column("lastName", width=50, minwidth=150, anchor=tk.CENTER)
    # tree.column("dateOfBirth", width=50, minwidth=150, anchor=tk.CENTER)
    # tree.column("address", width=50, minwidth=150, anchor=tk.CENTER)
    # tree.column("phoneNumber", width=50, minwidth=150, anchor=tk.CENTER)
    # tree.column("email", width=50, minwidth=150, anchor=tk.CENTER)
    # tree.column("bloodType", width=50, minwidth=150, anchor=tk.CENTER)

    # tree.heading("firstName", text="First Name", anchor=tk.CENTER)
    # tree.heading("lastName", text="Last Name", anchor=tk.CENTER)
    # tree.heading("dateOfBirth", text="Date of birth", anchor=tk.CENTER)
    # tree.heading("address", text="address", anchor=tk.CENTER)
    # tree.heading("phoneNumber", text="phone number", anchor=tk.CENTER)
    # tree.heading("email", text="email", anchor=tk.CENTER)
    # tree.heading("bloodType", text="Blood Type", anchor=tk.CENTER)

    # i = 0
    # for ro in cursor:
    #     tree.insert('', i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5], ro[6], ro[7]))
    #     i = i + 1

    # hsb = ttk.Scrollbar(r, orient="horizontal")
    # hsb.configure(command=tree.xview)
    # tree.configure(xscrollcommand=hsb.set)
    # hsb.pack(fill=X, side = BOTTOM)

    # vsb = ttk.Scrollbar(r, orient="vertical")
    # vsb.configure(command=tree.yview)
    # tree.configure(yscrollcommand=vsb.set)
    # vsb.pack(fill=Y, side = RIGHT)

    # tree.pack()
    # firstName=tk.StringVar()
    # lastName=tk.StringVar()
    # dateOfBirth=tk.StringVar()
    # address=tk.StringVar()
    # phoneNumber=tk.StringVar()
    # email=tk.StringVar()
    # bloodType=tk.StringVar()
r = tk.Tk()

def delete_data():
    r.geometry("650x650")
    r.title("User detail")
    firstName=tk.StringVar()
    
    
    f=Frame(r, width=400, height=320, background="grey")
    f.place(x=100, y=250)
    l1=Label(f, text="firstName", width=8, font=('Times', 11, 'bold'))
    e1=Entry(f, textvariable=firstName, width=15)
    l1.place(x=50, y=30)
    e1.place(x=170, y=30)
    
    

    def deleting_data():
        nonlocal e1
        s_firstName = firstName.get()
        
        query = ("DELETE FROM Donors WHERE firstName=%s",(s_firstName))
        cursor.execute(query)
        
        cnx.commit()
        #tree.insert('', 'end', text="", values=(conn.lastrowid, s_firstName, s_lastName, dob, add, phone, e, bt))
        mb.showinfo("Sucess", "you did it")
        
    
    submitbutton = tk.Button(f, text="Submit", command= deleting_data)
    submitbutton.configure(font=('Times', 11, 'bold'), bg='grey', fg='black')
    submitbutton.place(x=100, y=300)

        # insertbutton = tk.Button(r, text="insert", command=lambda: add_data())
        # insertbutton.configure(font = ('calabri', 14, 'bold'), bg = 'grey', fg = 'black')
        # insertbutton.place(x=200, y=260)

        # deletebutton = tk.Button(r, text="delete", command=None)
        # deletebutton.configure(font = ('calabri', 14, 'bold'), bg = 'grey', fg = 'black')
        # deletebutton.place(x=300, y=260)


    r.mainloop()
    
def add_data():
    
    r.geometry("650x650")
    r.title("User detail")
    firstName=tk.StringVar()
    lastName=tk.StringVar()
    dateOfBirth=tk.StringVar()
    address=tk.StringVar()
    phoneNumber=tk.StringVar()
    email=tk.StringVar()
    bloodType=tk.StringVar()
    
    f=Frame(r, width=400, height=320, background="grey")
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
        cursor.execute('INSERT INTO Donors(firstName, lastName, dateOfBirth, address, phoneNumber, email, bloodType) VALUES(%s,%s,%s,%s,%s,%s,%s)', (s_firstName, s_lastName, dob, add, phone, e, bt))
        print(cursor.lastrowid)
        cnx.commit()
        #tree.insert('', 'end', text="", values=(conn.lastrowid, s_firstName, s_lastName, dob, add, phone, e, bt))
        mb.showinfo("Sucess", "you did it")
        
    
    submitbutton = tk.Button(f, text="Submit", command= insert_data)
    submitbutton.configure(font=('Times', 11, 'bold'), bg='grey', fg='black')
    submitbutton.place(x=100, y=300)

        # insertbutton = tk.Button(r, text="insert", command=lambda: add_data())
        # insertbutton.configure(font = ('calabri', 14, 'bold'), bg = 'grey', fg = 'black')
        # insertbutton.place(x=200, y=260)

        # deletebutton = tk.Button(r, text="delete", command=None)
        # deletebutton.configure(font = ('calabri', 14, 'bold'), bg = 'grey', fg = 'black')
        # deletebutton.place(x=300, y=260)


    r.mainloop()

    



# THE APP

# Create the main window 
window = Tk()
window.title("The Blood bank app") # window title
window.geometry('400x400') # window size


tablelabel = Label(window, text="Blood Bank Tables") # label for the tables
tablelabel.grid(column=0, row=0) # label pos
# create a combox to choose tables from
combo = Combobox(window, state = 'readonly') # create combobox
combo['values']= ("Donors", "Recipients", "Donations", "Transfusions", "AvailableStocks", "Top3") #insert values to combobox
combo.set("Select Table") # begin with empty box'
combo.grid(column=0, row=1) # pos of combobox
# create button, set button text to choose, set command to combo bind open new window and call retrievetables
tableButton = Button(window, text = "Choose", command = retrieveTables)
tableButton.grid(column=0, row=2) # pos for button


# creating entry to insert firstName to find all information about donors
infolabel = Label(window, text="Search persons information by first name")
infolabel.grid(column=0, row=3)
infoentry = Entry(window) # create entry
infoentry.grid(column=0, row=4)
infoButton = Button(window, text = "Choose", command = infoentry.bind('<<openNewWindow>>', retrieveInfo))
infoButton.grid(column=0, row=5)


# create entry to find when donors can donate next
nextdonlabel = Label(window, text="Can the person donate again by both name")
nextdonlabel.grid(column=0, row=7)
nextdonentry = Entry(window)
nextdonentry.grid(column=0, row=8)
nextdonButton = Button(window, text = "Choose", command = nextdonentry.bind('<<openNewWindow>>', retrieveNextDonation))
nextdonButton.grid(column=0, row=9)


# create entry for gi
labelgiving = Label(window, text="Enter name of recipient to see who he can get blood from")
labelgiving.grid(column=0, row=10)
entergiving = Entry(window)
entergiving.grid(column=0, row=11)
nameButton = Button(window, text = "Choose", command = entergiving.bind('<<openNewWindow>>', retrieveGiving))
nameButton.grid(column=0, row=12)


insertbutton = tk.Button(window, text="insert", command=lambda: add_data())
insertbutton.grid(column=0, row=13)

deletebutton = tk.Button(window, text="delete", command=lambda: delete_data())
deletebutton.grid(column=1, row=13)





window.mainloop()

