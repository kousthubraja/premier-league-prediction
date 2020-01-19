import csv
from rds_creds import *
from datetime import datetime

print("Connecting to AWS RDS.This may timeout if service is down or port 3306 is blocked.")  
cursor = get_rds_cursor()
rds = get_rds_db()
print("RDS connection successfull.")

def clean_db():
    sql_clean = "delete from PremierLeague"
    cursor.execute(sql_clean)
    rds.commit()
    
def insert_to_db(val):
    sql_insert = "INSERT INTO PremierLeague (date, time, HomeTeam, AwayTeam, FTHG, FTAG) VALUES (%s, %s, %s, %s, %s, %s )"
    
    #First value is a date, it needs to be in date format to push to db
    val[0] = datetime.strptime(val[0],  "%d/%m/%Y")
    
    cursor.execute(sql_insert, val)
    
print('--- Pushing data to db... ---')

with open("cleaned.csv") as input_csv:
    clean_db()
    
    csv_reader = csv.reader(input_csv)
    isHeader = True
    for row in csv_reader:
        if isHeader:
            isHeader = False
            continue
        insert_to_db(row)
        print(row)
    rds.commit()
        
print('--- Pushing data to db complete ---')
