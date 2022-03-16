from bloodBank import *
import queries as q
from tabulate import tabulate
from datetime import date

# creating the database, the tables and populating them
try:
    cursor.execute("USE {}".format(DATABASE_NAME)) # function to create database
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
    else:
        print(err)
else:
    print("Database {} already exists".format(DATABASE_NAME))





# QUERIES


# show any table
query = q.show_table("donors")
cursor.execute(query)
results = cursor.fetchall()
headers = [i[0] for i in cursor.description]
print(tabulate(results, headers, tablefmt='pretty'))

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