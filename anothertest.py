from bloodBank import *
import queries as q
from tkinter.ttk import *
import tkinter  as tk 
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as mb



cnx = mysql.connector.connect(user='root', password='Ihtwasc?', host='127.0.0.1', database = "Bloodbank")
cursor = cnx.cursor(buffered=True)
 
# CREATING AND POPULATING THE DATABASE

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
    q.show_table(table, cursor)
    headers = [i[0] for i in cursor.description]
    i = 0
    # show the column names
    for header in headers:
        e = Label(newWindow,width=17,text=header,borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=i)
        i+=1
    i = 1
    # show the rows
    for row in cursor:
        for j in range(len(row)):
            e = Label(newWindow,width=17, text=row[j], borderwidth=2,relief='ridge', anchor="w")  
            e.grid(row=i, column=j) 
        i+=1

def retrieveInfo(fname, lname):
    wholename = fname + " " + lname
    infoWindow = Toplevel(window) # create new window for info
    q.findDonor(wholename, cursor)
    headers = [i[0] for i in cursor.description]
    i = 0
    # show the column names
    for header in headers:
        e = Label(infoWindow,width=17, text=header, borderwidth=2,relief='ridge', anchor="w")
        e.grid(row=0, column=i)
        i+=1
    i = 1
    # show the row
    for wholename in cursor: 
        for j in range(len(wholename)):
            e = Label(infoWindow,width=17, text=wholename[j], borderwidth=2,relief='ridge', anchor="w")
            e.grid(row=i, column=j) 
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
    table = insert.get() # selected table

    r = Toplevel(window)
    r.geometry("1050x700")
    r.title("User detail")
    r.resizable(False, False) 
    tree = ttk.Treeview(r)

    q.show_table(table, cursor)
    headers = [i[0] for i in cursor.description]


    tree['show'] = 'headings' #ask gummi about that

    # style
    s = ttk.Style(window)
    s.theme_use("clam")
    s.configure(".", font = ('Helvetica', 11))
    s.configure("Treeview.Heading", foreground='red')

    #Define columns
    tree["columns"] = (headers)

    #Format columns
    for header in headers:
        tree.column(header, width=50, minwidth=150, anchor=tk.CENTER)

    #Create headings
    for header in headers:
        tree.heading(header, text=header, anchor=tk.CENTER)

    #Insert rows
    for row in cursor:
        tree.insert('', "end", text="", values = row)
    
    tree.pack(ipadx='250', ipady='29')

    #Horizontal scrollbar 
    hsb = ttk.Scrollbar(r, orient="horizontal")
    hsb.configure(command=tree.xview)
    tree.configure(xscrollcommand=hsb.set)
    #hsb.pack(fill=X, side = BOTTOM)
    hsb.place(x=75, y=290, width = 898)

    #Vertical scrollbar
    vsb = ttk.Scrollbar(r, orient="vertical")
    vsb.configure(command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    #vsb.pack(fill=Y, side = RIGHT)
    vsb.place(x=980, y=3, height=270)
    
    #Create all entries
    headers.pop(0) # removing the index

    yas = 320
    for header in headers:
        entry=Entry(r, width=15)
        entry.place(x=520, y = yas )
        label =Label(r, text=header, width=12, font=('Times', 11, 'bold'))
        label.place(x=400, y = yas)
        yas += 40

    def insert_data():
        entries = get_all_entry_widgets_text_content(r)

        datalist = [entry.get() for entry in entries]
        # inserts data into MySQL database
        q.insertrow(table, datalist, cursor)
        cnx.commit()
        datalist.insert(0, cursor.lastrowid)
        # insert data in interface table
        tree.insert('', 'end', text="", values=(datalist))
        #Success message
        mb.showinfo("Sucess", f"{table[:-1]} registered")
        #Empty all entry widgets
        for widget in r.winfo_children():
            if isinstance(widget, Entry):
                widget.delete(0, "end")



    deletebutton = tk.Button(r, text="Delete", command=lambda: delete_data(tree))
    deletebutton.configure(font=('Times', 11, 'bold'), bg='grey', fg='black')
    deletebutton.place(x=600, y=590)

    submitbutton = tk.Button(r, text="Submit", command= insert_data)
    submitbutton.configure(font=('Times', 11, 'bold'), bg='grey', fg='black')
    submitbutton.place(x=500, y=590)

    cancelbutton = tk.Button(r, text="Cancel", command=r.destroy)
    cancelbutton.configure(font=('Times', 11, 'bold'), bg='grey', fg='black')
    cancelbutton.place(x=550, y=630)


def get_all_entry_widgets_text_content(root):
    all_entries = [widget for widget in root.winfo_children() if isinstance(widget, Entry)]
    return all_entries


def delete_data(tree):
   table = insert.get()
   selected_item=tree.selection()[0]
   did=tree.item(selected_item)['values'][0]
   q.deleterow(table, did, cursor)
   tree.delete(selected_item)
   mb.showinfo("Sucess", f"{table[:-1]}, deleted")

    
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


# create entry to search who can give blood to a certain recipient
labelgiving = Label(window, text="Enter first and last name of recipient to see who they can get blood from")
labelgiving.place(x=2, y=300)
fname = Entry(window, width=10)
fname.place(x=115, y=330)
lname = Entry(window, width=10)
lname.place(x=225, y=330)
nameButton = Button(window, text = "Choose", command = lambda: ('<<openNewWindow>>', retrieveGiving(fname.get(), lname.get())))
nameButton.place(x=175, y=360)


# manipulating the tables
insert = Combobox(window, state = 'readonly') # create combobox
insert['values']= ("Donors", "Recipients", "Donations", "Transfusions") #insert values to combobox
insert.set("Select Table") # begin with empty box'
insert.place(x=105, y=400) # pos of combobox

manupbutton = tk.Button(window, text="insert", command=lambda: add_data())
manupbutton.place(x=175, y=430)


window.mainloop()