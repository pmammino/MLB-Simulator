import bs4
import requests
import pandas
import timeit



## Function Definitions

def set_lineups(n):
  away_lineup = list_lineups[n].reset_index(drop = True)
  home_lineup = list_lineups[n + 1].reset_index(drop = True)
  away_pitcher = pandas.DataFrame(pitchers.iloc[n]).T.reset_index(drop = True)
  home_pitcher = pandas.DataFrame(pitchers.iloc[n+1]).T.reset_index(drop = True)
  return(away_lineup, home_lineup, away_pitcher, home_pitcher)


start = timeit.default_timer()

#
#
# scrape Steamer projection files

batter_steamer = pandas.read_csv("steamer_batter_2018.csv")
pitcher_steamer = pandas.read_csv("steamer_pitcher_2018.csv")


#
#
# pull lineups from Rotogrinders

res = requests.get('https://rotogrinders.com/lineups/mlb?site=fanduel')
soup = bs4.BeautifulSoup(res.text, 'lxml')

list1 = []

for i in soup.select('.pname'):
    list1.append(i.text)
    
lineups = pandas.DataFrame(list1)
lineups = lineups[0].str.strip()
lineups = pandas.DataFrame(lineups)

lineups.columns = ["name"]

list2 = []

for i in soup.select('div[class="pitcher players"] a[class="player-popup"]'):
    list2.append(i.text)
    
pitchers = pandas.DataFrame(list2)
pitchers = pitchers[0].str.strip()
pitchers = pandas.DataFrame(pitchers)

pitchers.columns = ["name"]

#
#
# pull teams from Rotogrinders

res2 = requests.get('https://rotogrinders.com/lineups/mlb?site=fanduel')
soup2 = bs4.BeautifulSoup(res2.text, 'lxml')

list3 = []

for i in soup2.select('.shrt'):
    list3.append(i.text)
    
teams = pandas.DataFrame(list3)

res3 = requests.get('https://rotogrinders.com/lineups/mlb?site=fanduel')
soup3 = bs4.BeautifulSoup(res3.text, 'lxml')

list4 = []

for i in soup3.select('span.status span.stats'):
    list4.append(i.text)
    
handedness = pandas.DataFrame(list4)
handedness = handedness[0].str.strip()
handedness = pandas.DataFrame(handedness)
handedness.columns = ["Bats"]
handedness = pandas.DataFrame(handedness)

list5 = []

for i in soup3.select('div[class="pitcher players"] span[class="stats"]'):
    list5.append(i.text)
    
pitcher_handedness = pandas.DataFrame(list5)
pitcher_handedness = pitcher_handedness[0].str.strip()
pitcher_handedness = pandas.DataFrame(pitcher_handedness)
pitcher_handedness.columns = ["Throws"]
pitcher_handedness = pandas.DataFrame(pitcher_handedness)

lineups["Bats"] = handedness
pitchers["Throws"] = pitcher_handedness

merge = batter_steamer[["name","mlbamid"]].drop_duplicates()

lineups_merged = lineups.merge(merge, on = ["name"], how = "left")
lineups_merged["vRCode"] = "0-vR-" + lineups_merged['mlbamid'].astype(str).replace('\.0', '', regex=True)
lineups_merged["vLCode"] = "0-vL-" + lineups_merged['mlbamid'].astype(str).replace('\.0', '', regex=True)

lineups_merged = lineups_merged.merge(batter_steamer[["m_id", "BB", "K", "Single", "Double", "Triple", "HR", "BO"]], left_on = ["vRCode"], right_on = ["m_id"], how = "left")
lineups_merged = lineups_merged.rename(index=str, columns={"BB" : "bbR", "K" : "kR", "Single" : "1bR", "Double" : "2bR", "Triple" : "3bR", "HR" : "hrR", "BO" : "boR"})

lineups_merged = lineups_merged.merge(batter_steamer[["m_id", "BB", "K", "Single", "Double", "Triple", "HR", "BO"]], left_on = ["vLCode"], right_on = ["m_id"], how = "left")
lineups_merged = lineups_merged.rename(index=str, columns={"BB" : "bbL", "K" : "kL", "Single" : "1bL", "Double" : "2bL", "Triple" : "3bL", "HR" : "hrL", "BO" : "boL"})


merge_2 = pitcher_steamer[["name","mlbamid"]].drop_duplicates()

pitchers = pitchers.merge(merge_2, on = ["name"], how = "left")
pitchers["vRCode"] = "SP-0-vR-" + pitchers['mlbamid'].astype(str).replace('\.0', '', regex=True)
pitchers["vLCode"] = "SP-0-vL-" + pitchers['mlbamid'].astype(str).replace('\.0', '', regex=True)

pitchers = pitchers.merge(pitcher_steamer[["m_id", "BB", "K", "Single", "Double", "Triple", "HR", "BO"]], left_on = ["vRCode"], right_on = ["m_id"], how = "left")
pitchers = pitchers.rename(index=str, columns={"BB" : "bbR", "K" : "kR", "Single" : "1bR", "Double" : "2bR", "Triple" : "3bR", "HR" : "hrR", "BO" : "boR"})
pitchers = pitchers.merge(pitcher_steamer[["m_id", "BB", "K", "Single", "Double", "Triple", "HR", "BO"]], left_on = ["vLCode"], right_on = ["m_id"], how = "left")
pitchers = pitchers.rename(index=str, columns={"BB" : "bbL", "K" : "kL", "Single" : "1bL", "Double" : "2bL", "Triple" : "3bL", "HR" : "hrL", "BO" : "boL"})


n = 9  #chunk row size
list_lineups = [lineups_merged[i:i+n] for i in range(0,lineups_merged.shape[0],n)]

#
# manipulate lineup scrape into each specific team's lineup

  
away_lineup, home_lineup, away_pitcher, home_pitcher = set_lineups(0)  


def at_bat(pitcher, hitter):
    
    if away_pitcher["Throws"] == "R":
       batter_p1b = home_lineup["1bR"]
       batter_p2b = home_lineup["2bR"]
       batter_p3b = home_lineup["3bR"]
       batter_phr = home_lineup["hrR"]
       batter_pbb = home_lineup["bbR"]
       batter_pso = home_lineup["kR"]
       batter_pbo = home_lineup["boR"]
    elif away_pitcher["Throws"] == "L":
        batter_p1b = home_lineup["1bL"]
        batter_p2b = home_lineup["2bL"]
        batter_p3b = home_lineup["3bL"]
        batter_phr = home_lineup["hrL"]
        batter_pbb = home_lineup["bbL"]
        batter_pso = home_lineup["kL"]
        batter_pbo = home_lineup["boL"]
    
    return [batter_p1b, batter_p2b, batter_p3b, batter_phr, batter_pbb, batter_pso, batter_pbo]

def oddsCalc(batter, pitcher, league):
    
    odds1b = ((batter_p1b / (1 - batter_p1b)) * (pitcher_p1b / (1 - pitcher_p1b)) / (league_p1b / (1 - league_p1b)))
    odds2b = ((batter_p2b / (1 - batter_p2b)) * (pitcher_p2b / (1 - pitcher_p2b)) / (league_p2b / (1 - league_p2b)))
    odds3b = ((batter_p3b / (1 - batter_p3b)) * (pitcher_p3b / (1 - pitcher_p3b)) / (league_p3b / (1 - league_p3b)))
    oddshr = ((batter_phr / (1 - batter_phr)) * (pitcher_phr / (1 - pitcher_phr)) / (league_phr / (1 - league_phr)))
    oddsbb = ((batter_pbb / (1 - batter_pbb)) * (pitcher_pbb / (1 - pitcher_pbb)) / (league_pbb / (1 - league_pbb)))
    oddsso = ((batter_pso / (1 - batter_pso)) * (pitcher_pso / (1 - pitcher_pso)) / (league_pso / (1 - league_pso)))
    oddsbo = ((batter_pbo / (1 - batter_pbo)) * (pitcher_pbo / (1 - pitcher_pbo)) / (league_pbo / (1 - league_pbo)))

    p1b = odds1b / (odds1b +1)
    p2b = odds2b / (odds2b +1)
    p3b = odds3b / (odds3b +1)
    phr = oddshr / (oddshr +1)
    pbb = oddsbb / (oddsbb +1)
    pso = oddsso / (oddsso +1)
    pbo = oddsbo / (oddsbo +1)
    total = p1b + p2b + p3b + phr + pbb + pso + pbo
    
    np1b = p1b / total
    np2b = p2b / total
    np3b = p3b / total
    nphr = phr / total
    npbb = pbb / total
    npso = pso / total
    npbo = pbo / total
    
    return [np1b, np2b, np3b, nphr, npbb, npso, npbo]








stop = timeit.default_timer()

print(stop - start)