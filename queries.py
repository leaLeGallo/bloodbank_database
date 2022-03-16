#All queries for the bloodbank application
from tabulate import tabulate
from datetime import date
from bloodBank import cnx

# used to show any table from the database
def show_table(table, cursor):
    query = f"select * from {table}"
    cursor.execute(query)
    results = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    return(tabulate(results, headers, tablefmt='pretty'))

# returns a sentence saying how many days are needed for a donor to give blood again
def nextdonation(wholename, cursor):
    query = f"select date from donations join donors on donations.donorsID = donors.donorsID where concat (firstName, ' ' , lastName) = '{wholename}'"
    cursor.execute(query)
    donationdate = cursor.fetchone()
    diff = date.today() - donationdate[0]
    if (56 - int(diff.days)) < 0:
        ret = f"{wholename} can give blood now"
    else:
        ret = f"{wholename} can give blood again in {56 - int(diff.days)} day.s"
    return ret

# interts a donor into the database
def insertdonor(firstname, lastname, dob, add, phone, email, bt, cursor):
    query = "INSERT INTO donors(firstName, lastName, dateOfBirth, address, phoneNumber, email, bloodType)"\
           f"values ('{firstname}', '{lastname}', '{dob}', '{add}', '{phone}', '{email}', '{bt}');"
    cursor.execute(query)
    cnx.commit()


def insertrow(table, cursor):
    query = f"select * from {table}"
    cursor.execute(query)
    #cnx.commit()
    headers = [i[0] for i in cursor.description]
    headers.pop(0) # deletes the first column header (the index)
    headers = (', '.join(headers))
    query = f"INSERT INTO {table}({headers})"\
            "values ('Lea', 'Le lmao', '1998-07-23', '10 rue nouvelle merlevenez', '0767239256', 'leacestmoi@hotmail.fr', 'O+');"
    cursor.execute(query)
    cnx.commit()


# deletes a row from any table
def deleterow(table, row, cursor):
    query = f"delete from {table} where {table}ID = {row}"
    cursor.execute(query)
    cnx.commit()
    # reset auto increment
    query2 = f"alter table {table} auto_increment = 1"
    cursor.execute(query2)
    cnx.commit()