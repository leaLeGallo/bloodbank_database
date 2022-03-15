#All queries for the bloodbank application

def create_stocks_view(cursor):
    query = "create view availableStocks as select bloodType, sum(donations.quantity) as stock from donors"\
            "join donations on donors.donorID = donations.donorID "\
            "where donations.donationsID not in (select donationsID from transfusions)"\
            "group by bloodtype"\
            "order by stock desc"