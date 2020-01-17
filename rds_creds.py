import mysql.connector

rds = mysql.connector.connect(
  host="premier-league.cskwqupuhic2.us-east-2.rds.amazonaws.com",
  user="admin",
  passwd="adminadmin",
  database="premierleague"
)


def get_rds_cursor():
    cursor = rds.cursor()
    return cursor

def get_rds_db():
    return rds
