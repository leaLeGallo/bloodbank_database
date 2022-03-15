import mysql.connector
from mysql.connector import errorcode
import csv

# Connects to SQL server
cnx = mysql.connector.connect(user='root', password='Ihtwasc?', host='127.0.0.1')
cursor = cnx.cursor()


# Creates database
def create_database(cursor, DB_NAME):
    try:
        cursor.execute(f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
    except mysql.connector.Error as err:
        print(f"Failed to create database {err}")
        exit(1)


# Creates a table for planets with headers
def create_table_donors(cursor):
    create_planets = "CREATE TABLE donors (" \
                 "  donorID int(100) NOT NULL AUTO_INCREMENT," \
                 "  firstName varchar(10)," \
                 "  lastName varchar(40)," \
                 "  dateOfBirth date," \
                 "  address varchar(50)," \
                 "  phoneNumber varchar(50)," \
                 "  email varchar(50)," \
                 "  bloodType varchar(3)," \
                 "  PRIMARY KEY (donorID)" \
                 ") ENGINE=InnoDB"
    try:
        print("Creating table donors: ")
        cursor.execute(create_planets)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("donors OK")


# Populates the donor table with data in the donor csv file
def insert_into_donors(cursor):
    # reads the planets.csv file
    with open("donors.csv", "r") as donorsfile:
        donorsfile = csv.reader(donorsfile, delimiter=",")
        next(donorsfile) # skips headers 
        # iterates through the rows
        for row in donorsfile:
            try: # adding the values of each rows 
                cursor.execute("INSERT INTO donors(firstName, lastName, dateOfBirth, address, phoneNumber, email, bloodType)"\
                               "VALUES (%s, %s, %s, %s, %s, %s, %s);", row)
            except mysql.connector.Error as err:
                print(err.msg)
            else:
                # Make sure data is committed to the database
                cnx.commit()
        print("Values inserted into the donors table.")



# Creating the database 
DB_NAME = "bloodBank"
try: #Tries to use the database
    cursor.execute(f"USE {DB_NAME}")
except mysql.connector.Error as err:
    print("Database {} does not exist".format(DB_NAME))
    # if the error is that the database is unknown, create the database.
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor, DB_NAME)
        print("Database {} created succesfully.".format(DB_NAME))
        cnx.database = DB_NAME
        create_table_donors(cursor)
        insert_into_donors(cursor)
    else:
        print(err)
else:
    print(f"Database {DB_NAME} already exists.")