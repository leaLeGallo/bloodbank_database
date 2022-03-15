import mysql.connector
from mysql.connector import errorcode
import csv

cnx= mysql.connector.connect(user='root', password='root', host='127.0.0.1:8889', unix_socket= '/Applications/MAMP/tmp/mysql/mysql.sock')


DATABASE_NAME = 'BloodBank' 

cursor = cnx.cursor() 

def creating_databases(cursor, DATABASE_NAME): # create the database in mysql
    try:
        cursor.execute("Create database {} DEFAULT CHARACTER SET 'utf8'".format(DATABASE_NAME)) # try to create is
    except mysql.connector.Error as err:
        print("Failed to create database {}".format(err)) # if not error
        exit(1)

def create_tables_donor(cursor): # function to create tables in database
    create_donors = "CREATE TABLE donors (" \
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
        print("Creating table donors: ") # try create tables
        cursor.execute(create_donors)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.") # error if the tables already exist
        else:
            print(err.msg)
    else:
        print("Table donors created") # worked
        
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

def create_tables_recipients(cursor): # function to create tables in database
    create_recipients = "CREATE TABLE recipients (" \
                 "  recipientsID int(100) NOT NULL AUTO_INCREMENT," \
                 "  firstName varchar(10)," \
                 "  lastName varchar(40)," \
                 "  dateOfBirth date," \
                 "  address varchar(50)," \
                 "  phoneNumber varchar(50)," \
                 "  email varchar(50)," \
                 "  bloodType varchar(3)," \
                 "  PRIMARY KEY (recipientsID)" \
                 ") ENGINE=InnoDB"
    try:
        print("Creating table recipients: ") # try create tables
        cursor.execute(create_recipients)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.") # error if the tables already exist
        else:
            print(err.msg)
    else:
        print("Table recipients created") # worked
        
def insert_into_recipients(cursor):
    with open("recipients.csv", "r") as recipientsfile:
        recipientsfile = csv.reader(recipientsfile, delimiter=",")
        next(recipientsfile) # skips headers 
        # iterates through the rows
        for row in recipientsfile:
            try: # adding the values of each rows 
                cursor.execute("INSERT INTO recipients(firstName, lastName, dateOfBirth, address, phoneNumber, email, bloodType)"\
                               "VALUES (%s, %s, %s, %s, %s, %s, %s);", row)
            except mysql.connector.Error as err:
                print(err.msg)
            else:
                # Make sure data is committed to the database
                cnx.commit()
        print("Values inserted into the recipients table.")

try:
    cursor.execute("USE {}".format(DATABASE_NAME)) # function to create database
except mysql.connector.Error as err:
    print("Database {} does not exist".format(DATABASE_NAME)) # if it does not exist
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        creating_databases(cursor, DATABASE_NAME)
        print("Database {} created succesfully.".format(DATABASE_NAME)) # if created
        cnx.database = DATABASE_NAME
        create_tables_donor(cursor) # calling functions
        insert_into_donors(cursor)
        create_tables_recipients(cursor)
        insert_into_recipients(cursor)
    else:
        print(err)
else:
    print("Database {} already exists".format(DATABASE_NAME))