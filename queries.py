#All queries for the bloodbank application
from sqlite3 import Cursor
from tabulate import tabulate
from datetime import date
from bloodBank import cnx


def show_table(table, cursor):
    query = f"select * from {table}"
    cursor.execute(query)
    results = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    return(tabulate(results, headers, tablefmt='pretty'))


def nextdonation(wholename, cursor):
    query = f"select date from donations join donors on donations.donorID = donors.donorID where concat (firstName, ' ' , lastName) = '{wholename}'"
    cursor.execute(query)
    donationdate = cursor.fetchone()
    diff = date.today() - donationdate[0]
    if (56 - int(diff.days)) < 0:
        print("smaller")
        ret = f"{wholename} can give blood now"
    else:
        ret = f"{wholename} can give blood again in {56 - int(diff.days)} day.s"
    return ret


def insertdonor(firstname, lastname, dob, add, phone, email, bt, cursor):
    query = "INSERT INTO donors(firstName, lastName, dateOfBirth, address, phoneNumber, email, bloodType)"\
           f"values ('{firstname}', '{lastname}', '{dob}', '{add}', '{phone}', '{email}', '{bt}');"
    cursor.execute(query)
    cnx.commit()

def deleterow(table, row, cursor):
    query = f"delete from {table} where {table}ID = {row}"
    cursor.execute(query)
