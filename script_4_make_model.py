from datetime import datetime
from rds_creds import *

print("Connecting to AWS RDS.This may timeout if service is down or port 3306 is blocked.")  
cursor = get_rds_cursor()
rds = get_rds_db()
print("RDS connection successfull.")

#For this scenario, model is just a average of team's home and away goals, so easier
# to use SQL aggregate function to build it, and then insert to another table

sql_clean = "delete from GoalAvg"
    
sql_tmp_table_home = "create temporary table HomeAvg (team varchar(30), FTHAG double)"
sql_tmp_table_away = "create temporary table AwayAvg (team varchar(30), FTAAG double)"

sql_insert_tmp_table_home = """insert into HomeAvg (team,FTHAG)
(select HomeTeam as team, avg(FTHG) as FTHAG
from PremierLeague
group by HomeTeam)"""
sql_insert_tmp_table_away = """insert into AwayAvg (team,FTAAG)
(select AwayTeam as team, avg(FTAG) as FTAAG
from PremierLeague
group by AwayTeam)"""

sql_insert_goalavg = """insert into GoalAvg(team, FTHAG, FTAAG)
(select distinct * from HomeAvg
join
AwayAvg using(team))"""

print('--- Making model... ---')

cursor.execute(sql_clean)
cursor.execute(sql_tmp_table_home)
cursor.execute(sql_tmp_table_away)
cursor.execute(sql_insert_tmp_table_home)
cursor.execute(sql_insert_tmp_table_away)
rds.commit()

cursor.execute(sql_insert_goalavg)

rds.commit()

print('--- Making model complete ---')
