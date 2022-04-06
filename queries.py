#All queries for the bloodbank application

from datetime import date
from bloodBank import cnx


# used to show any table from the database
def show_table(table, cursor):
    query = f"select * from {table}"
    cursor.execute(query)

# returns a sentence saying how many days are needed for a donor to give blood again
def nextdonation(wholename, cursor):
    query = f"select date from donations join donors on donations.donorsID = donors.donorsID where concat (firstName, ' ' ,lastName) = '{wholename}'"
    cursor.execute(query)
    donationdate = cursor.fetchone()
    diff = date.today() - donationdate[0]
    if (56 - int(diff.days)) < 0:
        ret = f"{wholename} can give blood now"
    else:
        ret = f"{wholename} can give blood again in {56 - int(diff.days)} day.s"
    return ret


# inserts a row into any table
def insertrow(table, values, cursor):

    # HEADERS
    query = f"select * from {table}"
    cursor.execute(query)
    headers = [i[0] for i in cursor.description] # inserts the column headers into a list
    headers.pop(0) # deletes the first column header (the index)
    headers = (', '.join(headers)) # turns list of headers into a single string

    #VALUES
    (', '.join("'" + value + "'" for value in values)) # turns list of values into a single string
    values = str(values) 

    query = f"INSERT INTO {table}({headers})"\
            f"values ({values[1:-1]});"
    cursor.execute(query)
    cnx.commit()


# deletes a row from any table
def deleterow(table, row, cursor):
    query = f"delete from {table} where {table}ID = {row}"
    cursor.execute(query)
    cnx.commit()
    query2 = f"alter table {table} auto_increment = 1"   # reset auto increment
    cursor.execute(query2)
    cnx.commit()

def givingblood(wholename, cursor):
    query = f"select bloodType from recipients where concat (firstName, ' ' , lastName) = '{wholename}'"
    cursor.execute(query)
    recblood = cursor.fetchone()
    if recblood[0] == "O+":
        query = "select concat (firstName, ' ' , lastName) as name from donors where bloodType = 'O+' or bloodType = 'O-' "
    elif recblood[0] == "A+":
        query = "select concat (firstName, ' ' , lastName) as name from donors where bloodType = 'A+' or bloodType = 'A-' or bloodType = 'O+'or bloodType = 'O-' "
    elif recblood[0] == "B+":
        query = "select concat (firstName, ' ' , lastName) as name from donors where bloodType = 'B+' or bloodType = 'B-' or bloodType = 'O+'or bloodType = 'O-' "
    elif recblood[0] == "AB+":
        query = "select concat (firstName, ' ' , lastName) as name from donors"
    elif recblood[0] == "A-":
        query = "select concat (firstName, ' ' , lastName) as name from donors where bloodType = 'A-' or bloodType = 'O-'"
    elif recblood[0] == "O-":
        query = "select concat (firstName, ' ' , lastName) as name from donors where bloodType = 'O-'"
    elif recblood[0] == "B-":
        query = "select concat (firstName, ' ' , lastName) as name from donors where bloodType = 'B-' or bloodType = 'O-'"
    elif recblood[0] == "AB-":
        query = "select concat (firstName, ' ' , lastName) as name from donors where bloodType = 'AB-' or bloodType = 'A-' or bloodType = 'B-' or bloodType = 'O-'"
    
    cursor.execute(query)
    donors = cursor.fetchall()
    res = ""
    for don in donors:
        res += f"• {don[0]} \n"
    return res

def findDonor(wholename, table, cursor):
    query = f"Select * from {table} where concat (firstName, ' ' , lastName) = '{wholename}'"
    cursor.execute(query)
    return query