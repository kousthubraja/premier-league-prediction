import numpy as np
from datetime import datetime
from rds_creds import *

def get_team_avg(team, side):
    if side == 1:
        sql = "select FTHAG from GoalAvg where team = '%s'"
    else:
        sql = "select FTAAG from GoalAvg where team = '%s'"

    cursor = get_rds_cursor()
    cursor.execute(sql %(team))
    avg = cursor.fetchone()[0]
    return float(avg)

def insert_odds_to_db(game):
    rds = get_rds_db()
    cursor = get_rds_cursor()
    sql = """insert into Odds (date, team1, team2, odds_team1, odds_team2, odds_draw)
            values (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, game)
    rds.commit()

def get_odds(team_home, team_away):
    team_home_avg = get_team_avg(team_home, 1)
    team_away_avg = get_team_avg(team_away, 2)

    team_home_poison_dist = np.random.poisson(team_home_avg, 10000)
    team_away_poison_dist = np.random.poisson(team_away_avg, 10000)

    team_home_win_count = 0
    team_away_win_count = 0
    draw_count = 0

    simulation_count = 10000
    for i in range(0, simulation_count-1):
        if team_home_poison_dist[i] > team_away_poison_dist[i]:
            team_home_win_count += 1;
        elif team_home_poison_dist[i] == team_away_poison_dist[i]:
            draw_count += 1
        else:
            team_away_win_count += 1

    home_odds = simulation_count/team_home_win_count
    away_odds = simulation_count/team_away_win_count
    draw_odds = simulation_count/draw_count

    print(team_home, team_away, home_odds, draw_odds, away_odds)
    return [home_odds, draw_odds, away_odds]

upcoming_matches = [
['18/01/2019', 'Watford', 'Tottenham'],
['18/01/2019', 'Arsenal', 'Sheffield United'],
['18/01/2019', 'Brighton', 'Aston Villa'],
['18/01/2019', 'Man City', 'Crystal Palace'],
['18/01/2019', 'Norwich', 'Bournemouth'],
['18/01/2019', 'Southampton', 'Wolves'],
['18/01/2019', 'West Ham', 'Everton'],
['18/01/2019', 'Newcastle', 'Chelsea'],
['18/01/2019', 'Burnley', 'Leicester'],
['19/01/2019', 'Liverpool', 'Man United']
]

print('--- Predicting... ---')

sql_clean = "delete from Odds"

for match in upcoming_matches:
    odds = get_odds(match[1], match[2])
    match[0] = datetime.strptime(match[0],  "%d/%m/%Y")
    insert_odds_to_db([match[0], match[1], match[2], odds[0], odds[1], odds[2]])

print('--- Predicting complete ---')
