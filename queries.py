#All queries for the bloodbank application


def show_table(table):
    query = f"select * from {table}"
    return query


def nextdonation(lastname):
    query = f"select date from donations join donors on donations.donorID = donors.donorID where lastName = '{lastname}'"
    return query