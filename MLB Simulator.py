import bs4
import requests
import pandas
import timeit

start = timeit.default_timer()

#
#
# scrape Steamer projection files

batter_steamer = pandas.read_csv("steamer_batter_2018.csv")
pitcher_steamer = pandas.read_csv("steamer_pitcher_2018.csv")
mlbamid_database = pandas.read_csv("MLBAMID Database.csv")

#
#
# pull lineups from Rotogrinders

res = requests.get('https://rotogrinders.com/lineups/mlb?site=fanduel')
soup = bs4.BeautifulSoup(res.text, 'lxml')

list1 = []

for i in soup.select('.player-popup'):
    list1.append(i.text)
    
players = pandas.DataFrame(list1)

lineups = players[players.index % 10 != 0]
lineups.columns = ["name"]
pitchers = players[players.index % 10 == 0]
pitchers.columns = ["name"]
lineups = pandas.DataFrame(lineups)
lineups.reset_index(drop=True, inplace=True)
pitchers = pandas.DataFrame(pitchers)
pitchers.reset_index(drop=True, inplace=True)

#
#
# pull teams from Rotogrinders

res2 = requests.get('https://rotogrinders.com/lineups/mlb?site=fanduel')
soup2 = bs4.BeautifulSoup(res2.text, 'lxml')

list2 = []

for i in soup2.select('.shrt'):
    list2.append(i.text)
    
teams = pandas.DataFrame(list2)

res3 = requests.get('https://rotogrinders.com/lineups/mlb?site=fanduel')
soup3 = bs4.BeautifulSoup(res3.text, 'lxml')

list3 = []

for i in soup3.select('span.status span.stats'):
    list3.append(i.text)
    
handedness = pandas.DataFrame(list3)
handedness = handedness[0].str.strip()
handedness = pandas.DataFrame(handedness)
handedness.columns = ["Bats"]
handedness = pandas.DataFrame(handedness)

list4 = []

for i in soup3.select('div[class="pitcher players"] span[class="stats"]'):
    list4.append(i.text)
    
pitcher_handedness = pandas.DataFrame(list4)
pitcher_handedness = pitcher_handedness[0].str.strip()
pitcher_handedness = pandas.DataFrame(pitcher_handedness)
pitcher_handedness.columns = ["Throws"]
pitcher_handedness = pandas.DataFrame(pitcher_handedness)

lineups["Bats"] = handedness
pitchers["Throws"] = pitcher_handedness


#lineups = lineups[["name", "Bats"]].merge(batter_steamer[["name", "mlbamid"]], on = "name", how = "left")
#lineups = lineups.drop_duplicates(keep = "first")


lineups = pandas.merge(lineups, mlbamid_database, how = 'left')
pitchers = pandas.merge(lineups, mlbamid_database, how = 'left')

#lineups["M_ID"] = ["1", lineups["Bats"], lineups["mlbamid"]]

#
#
# manipulate lineup scrape into each specific team's lineup

if lineups.shape[0] > 10:
    away_lineup1 = lineups[:9]
    away_pitcher1 = pitchers[:1]
    home_lineup1 = lineups[10:19]
    home_pitcher1 = pitchers[1:2]

print(away_pitcher1)
print(away_lineup1)
print(home_pitcher1)
print(home_lineup1)

away_batter = pandas.DataFrame(away_lineup1.iloc[0])

#
#
# basic odds ratio calculator
# =============================================================================
# 
# odds1b = ((batter_p1b / (1 - batter_p1b)) * (pitcher_p1b / (1 - pitcher_p1b)) / (league_p1b / (1 - league_p1b)))
# odds2b = ((batter_p2b / (1 - batter_p2b)) * (pitcher_p2b / (1 - pitcher_p2b)) / (league_p2b / (1 - league_p2b)))
# odds3b = ((batter_p3b / (1 - batter_p3b)) * (pitcher_p3b / (1 - pitcher_p3b)) / (league_p3b / (1 - league_p3b)))
# oddshr = ((batter_phr / (1 - batter_phr)) * (pitcher_phr / (1 - pitcher_phr)) / (league_phr / (1 - league_phr)))
# oddsbb = ((batter_pbb / (1 - batter_pbb)) * (pitcher_pbb / (1 - pitcher_pbb)) / (league_pbb / (1 - league_pbb)))
# oddsso = ((batter_pso / (1 - batter_pso)) * (pitcher_pso / (1 - pitcher_pso)) / (league_pso / (1 - league_pso)))
# oddsbo = ((batter_pbo / (1 - batter_pbo)) * (pitcher_pbo / (1 - pitcher_pbo)) / (league_pbo / (1 - league_pbo)))
# 
# #
# #
# # turn odds from odds calculator  into probabilities
# 
# p1b = odds1b / (odds1b +1)
# p2b = odds2b / (odds2b +1)
# p3b = odds3b / (odds3b +1)
# phr = oddshr / (oddshr +1)
# pbb = oddsbb / (oddsbb +1)
# pso = oddsso / (oddsso +1)
# pbo = oddsbo / (oddsbo +1)
# total = p1b + p2b + p3b + phr + pbb + pso + pbo
# 
# #
# #
# # normalize probabilities to equal 1
# 
# np1b = p1b / total
# np2b = p2b / total
# np3b = p3b / total
# nphr = phr / total
# npbb = pbb / total
# npso = pso / total
# npbo = pbo / total
# =============================================================================







stop = timeit.default_timer()

print(stop - start)