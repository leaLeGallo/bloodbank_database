from cProfile import label
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
    newWindow = tk.Tk()
    cursor.execute(q.show_table(table, cursor))
    if (table == 'Donors'):
        e=Label(newWindow,width=17,text='Donors id',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=0)
        e=Label(newWindow,width=17,text='First name',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=1)
        e=Label(newWindow,width=17,text='Last name',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=2)
        e=Label(newWindow,width=17,text='Date of Birth',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=3)
        e=Label(newWindow,width=17,text='Address',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=4)
        e=Label(newWindow,width=17,text='Phone Number',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=5)
        e=Label(newWindow,width=17,text='Email',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=6)
        e=Label(newWindow,width=17,text='Blood Type',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=7)
    elif (table == 'Recipients'):
        e=Label(newWindow,width=17,text='Recipients id',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=0)
        e=Label(newWindow,width=17,text='First name',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=1)
        e=Label(newWindow,width=17,text='Last name',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=2)
        e=Label(newWindow,width=17,text='Date of Birth',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=3)
        e=Label(newWindow,width=17,text='Address',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=4)
        e=Label(newWindow,width=17,text='Phone Number',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=5)
        e=Label(newWindow,width=17,text='Email',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=6)
        e=Label(newWindow,width=17,text='Blood Type',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=7)
    elif (table == 'Donations'):
        e=Label(newWindow,width=17,text='Number',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=0)
        e=Label(newWindow,width=17,text='Donors id',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=1)
        e=Label(newWindow,width=17,text='Date',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=2)
        e=Label(newWindow,width=17,text='Quantity',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=3)
        e=Label(newWindow,width=17,text='Expired',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=4)
    elif (table == 'Transfusions'):
        e=Label(newWindow,width=17,text='Number',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=0)
        e=Label(newWindow,width=17,text='Date',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=1)
        e=Label(newWindow,width=17,text='Recipient id',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=2)
        e=Label(newWindow,width=17,text='Quantity',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=3)
        e=Label(newWindow,width=17,text='Blood Type',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=4)
        e=Label(newWindow,width=17,text='Donation Id',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=5)
    elif (table == 'AvailableStocks'):
        e=Label(newWindow,width=17,text='Blood Type',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=0)
        e=Label(newWindow,width=17,text='Stock',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=1)
    elif (table == 'Top3'):
        e=Label(newWindow,width=17,text='Name',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=0)
        e=Label(newWindow,width=17,text='People Saved',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=1)
    
    
    i = 1
    
    
    for thing in cursor: 
        for j in range(len(thing)):
            e = Label(newWindow,width=17, text=thing[j], borderwidth=2,relief='ridge', anchor="w")  
            e.grid(row=i, column=j) 
            #e.insert(END, person[j])
            
        i=i+1

def retrieveInfo(fname, lname):
    wholename = fname + " " + lname
    infoWindow = Toplevel(window) # creat new window for info
    cursor.execute(q.findDonor(wholename, cursor))
    i = 1
    e=Label(infoWindow,width=17,text='Donors id',borderwidth=2, relief='ridge',anchor='w')
    e.grid(row=0,column=0)
    e=Label(infoWindow,width=17,text='First name',borderwidth=2, relief='ridge',anchor='w')
    e.grid(row=0,column=1)
    e=Label(infoWindow,width=17,text='Last name',borderwidth=2, relief='ridge',anchor='w')
    e.grid(row=0,column=2)
    e=Label(infoWindow,width=17,text='Date of Birth',borderwidth=2, relief='ridge',anchor='w')
    e.grid(row=0,column=3)
    e=Label(infoWindow,width=17,text='Address',borderwidth=2, relief='ridge',anchor='w')
    e.grid(row=0,column=4)
    e=Label(infoWindow,width=17,text='Phone Number',borderwidth=2, relief='ridge',anchor='w')
    e.grid(row=0,column=5)
    e=Label(infoWindow,width=17,text='Email',borderwidth=2, relief='ridge',anchor='w')
    e.grid(row=0,column=6)
    e=Label(infoWindow,width=17,text='Blood Type',borderwidth=2, relief='ridge',anchor='w')
    e.grid(row=0,column=7)
    for wholename in cursor: 
        for j in range(len(wholename)):
            e = Label(infoWindow,width=17, text=wholename[j], borderwidth=2,relief='ridge', anchor="w")  
            e.grid(row=i, column=j) 
            #e.insert(END, wholename[j])
        i=i+1

def retrieveNextDonation(fname, lname):
    wholename = fname + " " + lname
    donationWindow = Toplevel(window) # new window for donation
    donationWindow.title(wholename) # title 
    nextdonlabel = Label( donationWindow, text = q.nextdonation(wholename, cursor) ) # call nextDonation
    donationWindow.geometry('300x100')
    nextdonlabel.grid(column=0, row=0)

def retrieveGiving(fname, lname):
    wholename = fname + " " + lname
    givingWindow = Toplevel(window)
    givingWindow.title(wholename)
    lbl = Label( givingWindow,
    text = q.givingblood(wholename, cursor) )
    givingWindow.geometry('300x300')
    lbl.grid(column=0, row=0)








 
def add_data():
    
    r = Toplevel(window)
    tree = ttk.Treeview(r)
    
    firstName=tk.StringVar()
    lastName=tk.StringVar()
    dateOfBirth=tk.StringVar()
    address=tk.StringVar()
    phoneNumber=tk.StringVar()
    email=tk.StringVar()
    bloodType=tk.StringVar()
    cursor.execute("SELECT * from Donors")
    
    tree['show'] = 'headings'

    s = ttk.Style(window)
    s.theme_use("clam")
    s.configure(".", font = ('Helvetica', 11))
    s.configure("Treeview.Heading", foreground='red')

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
    tree.heading("address", text="Address", anchor=tk.CENTER)
    tree.heading("phoneNumber", text="Phone number", anchor=tk.CENTER)
    tree.heading("email", text="Email", anchor=tk.CENTER)
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
    
    l1=Label(r, text="First name", width=12, font=('Times', 11, 'bold'))
    e1=Entry(r, textvariable=firstName, width=15)
    l1.place(x=400, y=300)
    e1.place(x=520, y=300)

    l2=Label(r, text="Last name", width=12, font=('Times', 11, 'bold'))
    e2=Entry(r, textvariable=lastName, width=15)
    l2.place(x=400, y=340)
    e2.place(x=520, y=340)

    l3=Label(r, text="Date of birth", width=12, font=('Times', 11, 'bold'))
    e3=Entry(r, textvariable=dateOfBirth, width=15)
    l3.place(x=400, y=380)
    e3.place(x=520, y=380)

    l4=Label(r, text="Address", width=12, font=('Times', 11, 'bold'))
    e4=Entry(r, textvariable=address, width=15)
    l4.place(x=400, y=420)
    e4.place(x=520, y=420)

    l5=Label(r, text="Phone number", width=12, font=('Times', 11, 'bold'))
    e5=Entry(r, textvariable=phoneNumber, width=15)
    l5.place(x=400, y=460)
    e5.place(x=520, y=460)

    l6=Label(r, text="Email", width=12, font=('Times', 11, 'bold'))
    e6=Entry(r, textvariable=email, width=15)
    l6.place(x=400, y=500)
    e6.place(x=520, y=500)

    l7=Label(r, text="Blood type", width=12, font=('Times', 11, 'bold'))
    e7=Entry(r, textvariable=bloodType, width=15)
    l7.place(x=400, y=540)
    e7.place(x=520, y=540)
    
    def insert_data():
        nonlocal e1, e2, e3, e4, e5, e6, e7
        s_firstName = firstName.get()
        s_lastName = lastName.get()
        dob = dateOfBirth.get()
        add = address.get()
        phone = phoneNumber.get()
        e = email.get()
        bt = bloodType.get()
        # adds the data to a list
        datalist = [s_firstName, s_lastName, dob, add, phone, e, bt]
        # inserts data into MySQL database
        q.insertrow("Donors", datalist, cursor)
        print(cursor.lastrowid)
        cnx.commit()
        # life-view of data inserting
        tree.insert('', 'end', text="", values=(31, s_firstName, s_lastName, dob, add, phone, e, bt))
        mb.showinfo("Sucess", "donor registered")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
        e7.delete(0, END)
        

        
    deletebutton = tk.Button(r, text="Delete", command=lambda: delete_data(tree))
    deletebutton.configure(font=('Times', 11, 'bold'), bg='grey', fg='black')
    deletebutton.place(x=600, y=580)

    submitbutton = tk.Button(r, text="Submit", command= insert_data)
    submitbutton.configure(font=('Times', 11, 'bold'), bg='grey', fg='black')
    submitbutton.place(x=500, y=580)

    cancelbutton = tk.Button(r, text="Cancel", command=r.destroy)
    cancelbutton.configure(font=('Times', 11, 'bold'), bg='grey', fg='black')
    cancelbutton.place(x=550, y=620)



def delete_data(tree):
   selected_item=tree.selection()[0]
   did=tree.item(selected_item)['values'][0]
   q.deleterow("donors", did, cursor)
   tree.delete(selected_item)
   mb.showinfo("Sucess", "donor deleted")

    



# THE APP

# Create the main window

window = Tk()
window.title("The Blood bank app") # window title
window.geometry('450x470') # window size






tablelabel = Label(window, text="Blood Bank Tables") # label for the tables
tablelabel.place(x=155, y=0) # label pos
# create a combox to choose tables from
combo = Combobox(window, state = 'readonly') # create combobox
combo['values']= ("Donors", "Recipients", "Donations", "Transfusions", "AvailableStocks", "Top3") #insert values to combobox
combo.set("Select Table") # begin with empty box'
combo.place(x=105, y=30) # pos of combobox
# create button, set button text to choose, set command to combo bind open new window and call retrievetables
tableButton = Button(window, text = "Choose", command = retrieveTables)
tableButton.place(x=175, y=60) # pos for button


# creating entry to insert firstName to find all information about donors
infolabel = Label(window, text="Enter a person's first  and last name to see their information")
infolabel.place(x=47, y=100)
firName = Entry(window, width=10) # create entry
firName.place(x=115, y=130)
lasName = Entry(window, width=10) # create entry
lasName.place(x=225, y=130)
infoButton = Button(window, text = "Choose", command = lambda: ('<<openNewWindow>>', retrieveInfo(firName.get(), lasName.get())))
infoButton.place(x=175, y=160)


# create entry to find when donors can donate next
nextdonlabel = Label(window, text="Enter a donor's first  and last name to know when they can donate again")
nextdonlabel.place(x=2, y=200)
frstName = Entry(window, width=10) # create entry
frstName.place(x=115, y=230)
lstName = Entry(window, width=10) # create entry
lstName.place(x=225, y=230)
nextdonButton = Button(window, text = "Choose", command = lambda: ('<<openNewWindow>>', retrieveNextDonation(frstName.get(), lstName.get())))
nextdonButton.place(x=175, y=260)


# create entry for gi
labelgiving = Label(window, text="Enter first and last name of recipient to see who they can get blood from")
labelgiving.place(x=2, y=300)
fname = Entry(window, width=10)
fname.place(x=115, y=330)
lname = Entry(window, width=10)
lname.place(x=225, y=330)
nameButton = Button(window, text = "Choose", command = lambda: ('<<openNewWindow>>', retrieveGiving(fname.get(), lname.get())))
nameButton.place(x=175, y=360)



insert = Combobox(window, state = 'readonly') # create combobox
insert['values']= ("Donors", "Recipients", "Donations", "Transfusions") #insert values to combobox
insert.set("Select Table") # begin with empty box'
insert.place(x=105, y=400) # pos of combobox

manupbutton = tk.Button(window, text="insert", command=lambda: add_data())
manupbutton.place(x=175, y=430)









window.mainloop()