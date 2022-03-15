import mysql.connector
from mysql.connector import errorcode
import csv

# Connects to SQL server
cnx = mysql.connector.connect(user='root', password='Ihtwasc?', host='127.0.0.1')
cursor = cnx.cursor()


DATABASE_NAME = 'BloodBank' 

cursor = cnx.cursor() 

# creates the database in mysql
def creating_databases(cursor, DATABASE_NAME): 
    try:
        cursor.execute("Create database {} DEFAULT CHARACTER SET 'utf8'".format(DATABASE_NAME)) # try to create is
    except mysql.connector.Error as err:
        print("Failed to create database {}".format(err)) # if not error
        exit(1)

# creates table donors in database
def create_tables_donors(cursor): 
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

#populates the donors database    
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

# creates table recipients in database
def create_tables_recipients(cursor): 
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

# populates the recipients table   
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

# creates the donations tables in database
def create_tables_donations(cursor): 
    create_donations = "CREATE TABLE donations (" \
                 "  donationsID int(100) NOT NULL AUTO_INCREMENT," \
                 "  donorID int(100)," \
                 "  date date," \
                 "  quantity int(100)," \
                 "  expired int(1)," \
                 "  PRIMARY KEY (donationsID)" \
                 ") ENGINE=InnoDB"
    try:
        print("Creating table donations: ") # try create tables
        cursor.execute(create_donations)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.") # error if the tables already exist
        else:
            print(err.msg)
    else:
        print("Table donations created") # worked

# populates the donations table
def insert_into_donations(cursor):
    with open("donations.csv", "r") as donationsfile:
        donationsfile = csv.reader(donationsfile, delimiter=",")
        next(donationsfile) # skips headers 
        # iterates through the rows
        for row in donationsfile:
            try: # adding the values of each rows 
                cursor.execute("INSERT INTO donations(donorID, date, quantity, expired)"\
                               "VALUES (%s, %s, %s, %s);", row)
            except mysql.connector.Error as err:
                print(err.msg)
            else:
                # Make sure data is committed to the database
                cnx.commit()
        print("Values inserted into the donations table.")
        
def create_tables_transfusions(cursor): # function to create tables in database
    create_transfusions = "CREATE TABLE transfusions (" \
                 "  transfusionsID int(100) NOT NULL AUTO_INCREMENT," \
                 "  date date," \
                 "  recipientID int(100)," \
                 "  quantity int(100)," \
                 "  bloodtype varchar(100)," \
                 "  donationsID int(100)," \
                 "  PRIMARY KEY (transfusionsID)" \
                 ") ENGINE=InnoDB"
    try:
        print("Creating table transfusions: ") # try create tables
        cursor.execute(create_transfusions)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.") # error if the tables already exist
        else:
            print(err.msg)
    else:
        print("Table transfusions created") # worked

def insert_into_transfusions(cursor):
    with open("transfusion.csv", "r") as transfusionsfile:
        transfusionsfile = csv.reader(transfusionsfile, delimiter=",")
        next(transfusionsfile) # skips headers 
        # iterates through the rows
        for row in transfusionsfile:
            try: # adding the values of each rows 
                cursor.execute("INSERT INTO transfusions(date, recipientID, quantity, bloodtype, donationsID)"\
                               "VALUES (%s, %s, %s, %s, %s);", row)
            except mysql.connector.Error as err:
                print(err.msg)
            else:
                # Make sure data is committed to the database
                cnx.commit()
        print("Values inserted into the transfusions table.")

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
    else:
        print(err)
else:
    print("Database {} already exists".format(DATABASE_NAME))