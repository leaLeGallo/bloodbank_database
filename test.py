from bloodBank import *
import queries as q
from tkinter import *
from tkinter.ttk import *
from functools import partial

cnx= mysql.connector.connect(user='root', password='root', host='127.0.0.1:8889', unix_socket= '/Applications/MAMP/tmp/mysql/mysql.sock', database = 'bloodbank')
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
    donors = combo.get()
    newWindow = Tk()
    newWindow.geometry("900x600") 
    cursor.execute(q.show_table(donors, cursor))
    headers = [e[0] for e in cursor.description]
    i=0
    for donors in cursor: 
        for j in range(len(donors)):
            e = Entry(newWindow, width=10) 
            e.grid(row=i, column=j) 
            e.insert(END, donors[j])
        i=i+1
    # table = combo.get() # table equals comboget
    # tableWindow = Toplevel(window) # create new window 
    # tableWindow.title(table) # set new window title 
    # tablelabel = Label( tableWindow, # label of new window 
    # text = q.show_table(table, cursor) ) # text of new window calls show_table method
    # tableWindow.geometry('1000x500') # new window size
    # tablelabel.grid(column=0, row=0) #label pos
    
    # enter = Entry(tableWindow)
    # enter.grid(column=0, row=1)
    # lbl1 = Label(tableWindow, text="Search persons information by first name")
    # lbl1.grid(column=0, row=2)
    # nameButton = Button(tableWindow, text = "Choose", command = enter.bind('<<openNewWindow>>', insertToTables))
    # nameButton.grid(column=0, row=3)

def retrieveInfo():
    infoname = infoentry.get()
    infoWindow = Toplevel(window) # creat new window for info
    infoWindow.title(infoname) # title 
    infolabel = Label( infoWindow,
    text = q.findDonor(infoname, cursor) ) #calling findDonor
    infoWindow.geometry('750x100')
    infolabel.grid(column=0, row=0)

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



window.mainloop()

