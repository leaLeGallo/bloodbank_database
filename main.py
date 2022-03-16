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
    else:
        print(err)
else:
    print("Database {} already exists".format(DATABASE_NAME))





# QUERIES


# show any table
table = "donations"
#print(q.show_table(table, cursor))


# checks when someone can next give blood
#name = "Blanche" + " " + "Henson"
#print(q.nextdonation(name, cursor))

# insert a donor

#q.insertdonor("Lea", "Le Gallo", "1998-07-23", "10 rue nouvelle merlevenez", "0767239256", "leacestmoi@hotmail.fr", "O+", cursor)
print("")
#val = ["21", "2019-01-01", "1", "1"]
#q.insertrow(table, val, cursor)

q.deleterow("donations", 21, cursor)

#print(type(q.insertrow(table, cursor)))
