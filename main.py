import bloodBank as bb


try:
    bb.cursor.execute("USE {}".format(bb.DATABASE_NAME)) # function to create database
except bb.mysql.connector.Error as err:
    print("Database {} does not exist".format(bb.DATABASE_NAME)) # if it does not exist
    if err.errno == bb.errorcode.ER_BAD_DB_ERROR:
        bb.creating_databases(bb.cursor, bb.DATABASE_NAME)
        print("Database {} created succesfully.".format(bb.DATABASE_NAME)) # if created
        bb.cnx.database = bb.DATABASE_NAME
        bb.create_tables_donors(bb.cursor) # calling functions
        bb.insert_into_donors(bb.cursor)
        bb.create_tables_recipients(bb.cursor)
        bb.insert_into_recipients(bb.cursor)
        bb.create_tables_donations(bb.cursor)
        bb.insert_into_donations(bb.cursor)
        bb.create_tables_transfusions(bb.cursor)
        bb.insert_into_transfusions(bb.cursor)
    else:
        print(err)
else:
    print("Database {} already exists".format(bb.DATABASE_NAME))