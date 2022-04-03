from bloodBank import *
import queries as q

# creating the database, the tables and populating them
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



# QUERIES

'''
# show any table
query = q.show_table("donors")
cursor.execute(query)
results = cursor.fetchall()
headers = [i[0] for i in cursor.description]
print(tabulate(results, headers, tablefmt='pretty'))
'''
'''
# checks when someone can next give blood
query = q.nextdonation("Henson")
cursor.execute(query)
donationdate = cursor.fetchone()
today = date.today()
print(donationdate[0])
print(" ")
print(today)
diff = today - donationdate[0]
print(56 - int(diff.days))
'''

from tkinter import *

from tkinter.ttk import *

def retrieve():
    table = combo.get()
    newWindow = Toplevel(window)
    newWindow.title(table)
    lbl = Label( newWindow,
    text = q.show_table(table, cursor) )
    newWindow.geometry('1000x500')
    lbl.grid(column=0, row=0)
    
    enter = Entry(newWindow)
    enter.grid(column=0, row=1)
    lbl1 = Label(newWindow, text="Search persons information by first name")
    lbl1.grid(column=0, row=2)
    nameButton = Button(newWindow, text = "Choose", command = enter.bind('<<openNewWindow>>', anotherthing))
    nameButton.grid(column=0, row=3)

def submit():
    name = e1.get()# + " " + e2.get()
    newWindow = Toplevel(window)
    newWindow.title(name)
    lbl = Label( newWindow,
    text = q.findDonor(name, cursor) )
    newWindow.geometry('750x100')
    lbl.grid(column=0, row=0)

def thething():
    name1 = enter1.get()# + " " + e2.get()
    newWindow = Toplevel(window)
    newWindow.title(name1)
    lbl = Label( newWindow,
    text = q.nextdonation(name1, cursor) )
    newWindow.geometry('300x100')
    lbl.grid(column=0, row=0)

def anotherthing():
    table = combo.get()
    value = []
    text = q.insertrow(table, value, cursor)
    return text.append

def giving():
    forgiving = entergiving.get()
    newWindow = Toplevel(window)
    newWindow.title(forgiving)
    lbl = Label( newWindow,
    text = q.givingblood(forgiving, cursor) )
    newWindow.geometry('300x300')
    lbl.grid(column=0, row=0)
    
    




window = Tk()

window.title("The Blood bank app")

window.geometry('300x350')

lbl = Label(window, text="Blood Bank Tables")

lbl.grid(column=0, row=0)

combo = Combobox(window, state = 'readonly')

combo['values']= ("Donors", "Recipients", "Donations", "Transfusions", "AvailableStocks", "Top3")

combo.set("Select Table") #begin with empty box'

combo.grid(column=0, row=1)

tableButton = Button(window, text = "Choose", command = combo.bind('<<openNewWindow>>', retrieve))
tableButton.grid(column=0, row=2)

e1 = Entry(window)
e1.grid(column=0, row=4)
lbl1 = Label(window, text="Search persons information by first name")
lbl1.grid(column=0, row=3)


nameButton = Button(window, text = "Choose", command = e1.bind('<<openNewWindow>>', submit))
nameButton.grid(column=0, row=6)

enter1 = Entry(window)
enter1.grid(column=0, row=8)
lbl2 = Label(window, text="Can the person donate again by both name")
lbl2.grid(column=0, row=7)
nameButton = Button(window, text = "Choose", command = enter1.bind('<<openNewWindow>>', thething))
nameButton.grid(column=0, row=9)

entergiving = Entry(window)
entergiving.grid(column=0, row=10)
lblgiving = Label(window, text="Can the person donate again by both name")
lblgiving.grid(column=0, row=11)
nameButton = Button(window, text = "Choose", command = entergiving.bind('<<openNewWindow>>', giving))
nameButton.grid(column=0, row=12)


window.mainloop()

