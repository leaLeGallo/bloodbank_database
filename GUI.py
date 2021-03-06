
from tracemalloc import start
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
    print("Database {} does not exist".format(DATABASE_NAME)) 
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        # creating and popuating the database if it does not exist
        creating_databases(cursor, DATABASE_NAME)
        print("Database {} created succesfully.".format(DATABASE_NAME)) 
        cnx.database = DATABASE_NAME
        create_tables_donors(cursor) 
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
    try:
        table = combo.get()
        tableWindow = tk.Tk() # create new window for the table
        tableWindow.title(f"{table}")
        q.show_table(table, cursor)
        headers = [i[0] for i in cursor.description]
        i = 0
        # show the column names
        for header in headers:
            e = Label(tableWindow,width=17, text=header, borderwidth=2,relief='ridge', anchor="w")
            e.grid(row=0, column=i)
            i+=1
        i = 1
        # show the rows
        for row in cursor: 
            for j in range(len(row)):
                e = Label(tableWindow,width=17, text=row[j], borderwidth=2,relief='ridge', anchor="w")  
                e.grid(row=i, column=j)   
            i+=1
    except:
        mb.showerror("Failure", "No table selected")
        tableWindow.destroy()

def retrieveInfo(fname, lname):
    
    wholename = fname + " " + lname
    infoWindow = Toplevel(window) # create new window for info
    cursor.execute(q.find_person(wholename, cursor))
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
    if (i == 1):
        mb.showerror("Failure", "No-one found with that name")
        infoWindow.destroy()
        
    
        
def retrieveNextDonation(fname, lname):
    try:
        wholename = fname + " " + lname
        donationWindow = Toplevel(window) # new window for donation
        donationWindow.title(wholename)
        nextdonlabel = Label( donationWindow, text = q.nextdonation(wholename, cursor) ) # call nextDonation
        donationWindow.geometry('300x100')
        nextdonlabel.grid(column=0, row=0)
    except:
        mb.showerror("Failure", "No donor found with that name")
        donationWindow.destroy()

def retrieveGiving(fname, lname):
    try:
        wholename = fname + " " + lname
        givingWindow = Toplevel(window) # creates window for the info
        givingWindow.title(wholename)
        lbl = Label( givingWindow,
        text = q.givingblood(wholename, cursor) )
        givingWindow.geometry('300x300')
        lbl.grid(column=0, row=0)
    except:
        mb.showerror("Failure", "No recipient found with that name")
        givingWindow.destroy()
        
def add_data():
    try:
        table = insert.get()
        addWindow = Toplevel(window) # new window showing the modifiable table
        tree = ttk.Treeview(addWindow)
        q.show_table(table, cursor)
        headers = [i[0] for i in cursor.description] # retrieve headers
        tree['show'] = 'headings'
        
        addWindow.geometry("1050x700")
        addWindow.title("User detail")
        addWindow.resizable(width=False, height=False)

        s = ttk.Style(window)
        s.theme_use("clam")
        s.configure(".", font = ('Helvetica', 11))
        s.configure("Treeview.Heading", foreground='red')

        tree["columns"] = (headers)
        for header in headers:
            tree.column(header, width=50, minwidth=150, anchor=tk.CENTER)
        # show headers
        for header in headers:
            tree.heading(header, text=header, anchor=tk.CENTER)
        i = 0
        # show rows
        for row in cursor:
            tree.insert('', "end", text="", values = row)
            i = i + 1
        
        tree.pack(ipadx='250', ipady='29')
        
        #Horizontal scrollbar 
        hsb = ttk.Scrollbar(addWindow, orient="horizontal")
        hsb.configure(command=tree.xview)
        tree.configure(xscrollcommand=hsb.set)
        hsb.place(x=75, y=290, width = 898)

        #Vertical scrollbar
        vsb = ttk.Scrollbar(addWindow, orient="vertical")
        vsb.configure(command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.place(x=980, y=3, height=270)
        
            
        headers.pop(0) # remove first column
        yas = 320
        xas = 520
        for header in headers:
            entry = Entry(addWindow, width=15)
            entry.place(x=xas, y = yas )
            label = Label(addWindow, text=header, width=12, font=('Times', 11, 'bold'))
            # instruction for dates
            if (header == "date" or header=="dateOfBirth"):
                format = Label(addWindow, text="(format: yyyy-mm-dd)", width=18, font=('Times', 11, 'bold'))
                format.place(x=xas + 150, y=yas)
            label.place(x=400, y=yas)
            yas += 40
    except:
        mb.showerror("Failure", "No table selected")
        addWindow.destroy()
        
    def insert_data():
        try:
            entries = get_all_entry(addWindow)
            datalist = [entry.get() for entry in entries]
            q.insertrow(table, datalist, cursor)
            cnx.commit()
            datalist.insert(0, cursor.lastrowid)
            tree.insert('', 'end', text="", values=(datalist))
            #Success message
            mb.showinfo("Sucess", f"{table[:-1]} registered")
            #Empty all entry widgets
            for widget in addWindow.winfo_children():
                if isinstance(widget, Entry):
                    widget.delete(0, "end")
        except:
            mb.showerror("Failure", "Incorrect insertion or empty box!")

    deletebutton = tk.Button(addWindow, text="Delete", command=lambda: delete_data(tree))
    deletebutton.configure(font=('Times', 11, 'bold'), bg='grey', fg='black')
    deletebutton.place(x=100, y=330)
    deleteLabel = Label(addWindow, text="Select a row you want to delete", width=30, font=('Times', 11, 'bold'))
    deleteLabel.place(x=50, y=350)

    submitbutton = tk.Button(addWindow, text="Submit", command= insert_data)
    submitbutton.configure(font=('Times', 11, 'bold'), bg='grey', fg='black')
    submitbutton.place(x=500, y=600)

    cancelbutton = tk.Button(addWindow, text="Cancel", command=addWindow.destroy)
    cancelbutton.configure(font=('Times', 11, 'bold'), bg='grey', fg='black')
    cancelbutton.place(x=600, y=600)


def get_all_entry(root):
    # function to get all the entries within a window in a list
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
window.resizable(width=False, height=False)


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
infolabel = Label(window, text="Enter a person's first  and last name to see their information:")

infolabel.place(x=47, y=100)
firName = Entry(window, width=10) # create entry
firName.place(x=115, y=130)
lasName = Entry(window, width=10) # create entry
lasName.place(x=225, y=130)
infoButton = Button(window, text = "Choose", command = lambda: ('<<opentableWindow>>', retrieveInfo(firName.get(), lasName.get())))
infoButton.place(x=175, y=160)

# create entry to find when donors can donate next
nextdonlabel = Label(window, text="Enter a donor's first  and last name to know when they can donate again:")

nextdonlabel.place(x=2, y=200)
frstName = Entry(window, width=10) # create entry
frstName.place(x=115, y=230)
lstName = Entry(window, width=10) # create entry
lstName.place(x=225, y=230)
nextdonButton = Button(window, text = "Choose", command = lambda: ('<<opentableWindow>>', retrieveNextDonation(frstName.get(), lstName.get())))
nextdonButton.place(x=175, y=260)


# create entry for information on whom can  give blood to whom
labelgiving = Label(window, text="Enter first and last name of a recipient to see who they can get blood from:")

labelgiving.place(x=2, y=300)
fname = Entry(window, width=10)
fname.place(x=115, y=330)
lname = Entry(window, width=10)
lname.place(x=225, y=330)
nameButton = Button(window, text = "Choose", command = lambda: ('<<opentableWindow>>', retrieveGiving(fname.get(), lname.get())))
nameButton.place(x=175, y=360)


insert = Combobox(window, state = 'readonly') # create combobox
insert['values']= ("Donors", "Recipients", "Donations", "Transfusions") #insert values to combobox
insert.set("Select Table") # begin with empty box'
insert.place(x=105, y=400) # pos of combobox


manupbutton = tk.Button(window, text="insert", command=lambda: add_data())
manupbutton.place(x=175, y=430)