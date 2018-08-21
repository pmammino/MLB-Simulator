import bs4
import requests
import pandas
import timeit
import numpy as np



## Function Definitions

def set_lineups(n):
  away_lineup = list_lineups[n].reset_index(drop = True)
  home_lineup = list_lineups[n + 1].reset_index(drop = True)
  away_pitcher = pandas.DataFrame(pitchers.iloc[n]).T.reset_index(drop = True)
  home_pitcher = pandas.DataFrame(pitchers.iloc[n+1]).T.reset_index(drop = True)
  return(away_lineup, home_lineup, away_pitcher, home_pitcher)

def at_bat(pitcher, hitter):
    if pitcher.at[0,"Throws"] == "R":
       batter_p1b = hitter.at[0,"1bR"]
       batter_p2b = hitter.at[0,"2bR"]
       batter_p3b = hitter.at[0,"3bR"]
       batter_phr = hitter.at[0,"hrR"]
       batter_pbb = hitter.at[0,"bbR"]
       batter_pso = hitter.at[0,"kR"]
       batter_pbo = hitter.at[0,"boR"]
    else:
       batter_p1b = hitter.at[0,"1bL"]
       batter_p2b = hitter.at[0,"2bL"]
       batter_p3b = hitter.at[0,"3bL"]
       batter_phr = hitter.at[0,"hrL"]
       batter_pbb = hitter.at[0,"bbL"]
       batter_pso = hitter.at[0,"kL"]
       batter_pbo = hitter.at[0,"boL"]
        
    if hitter.at[0,"Bats"] == "R" or (hitter.at[0,"Bats"] == "S" and pitcher.at[0,"Throws"] == "L"):
       pitcher_p1b = pitcher.at[0,"1bR"]
       pitcher_p2b = pitcher.at[0,"2bR"]
       pitcher_p3b = pitcher.at[0,"3bR"]
       pitcher_phr = pitcher.at[0,"hrR"]
       pitcher_pbb = pitcher.at[0,"bbR"]
       pitcher_pso = pitcher.at[0,"kR"]
       pitcher_pbo = pitcher.at[0,"boR"]
    else:
       pitcher_p1b = pitcher.at[0,"1bL"]
       pitcher_p2b = pitcher.at[0,"2bL"]
       pitcher_p3b = pitcher.at[0,"3bL"]
       pitcher_phr = pitcher.at[0,"hrL"]
       pitcher_pbb = pitcher.at[0,"bbL"]
       pitcher_pso = pitcher.at[0,"kL"]
       pitcher_pbo = pitcher.at[0,"boL"]
        
    league_p1b = .152056268409
    league_p2b = .045140889455
    league_p3b = .004727358249
    league_phr = .026802180461
    league_pbb = .081558771793
    league_pso = .198009085542
    league_pbo = .491705446091

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
    
    results = ['1b', '2b', '3b', 'hr', 'bb', 'so', 'bo']
    probs = [np1b, np2b, np3b, nphr, npbb, npso, npbo]
    
    result = np.random.choice(results, 1, p=probs)
    
    return(result)
  
start = timeit.default_timer()

#
#
# scrape Steamer projection files

batter_steamer = pandas.read_csv("steamer_batter_2018.csv")
pitcher_steamer = pandas.read_csv("steamer_pitcher_2018.csv")

dummy_hitter_pitcher = pandas.read_excel("DummyHitter.xlsx", sheetname = "DummyHitter")

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

lineups_merged['bbL'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['BBL'][0],lineups_merged['bbL'])
lineups_merged['bbL'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['BBL'][1],lineups_merged['bbL'])
lineups_merged['kL'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['SOL'][0],lineups_merged['kL'])
lineups_merged['kL'] = np.where(lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['SOL'][1],lineups_merged['kL'])
lineups_merged['1bL'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['1bL'][0],lineups_merged['1bL'])
lineups_merged['1bL'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['1bL'][1],lineups_merged['1bL'])
lineups_merged['2bL'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['2bL'][0],lineups_merged['2bL'])
lineups_merged['2bL'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['2bL'][1],lineups_merged['2bL'])
lineups_merged['3bL'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['3bL'][0],lineups_merged['3bL'])
lineups_merged['3bL'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['3bL'][1],lineups_merged['3bL'])
lineups_merged['hrL'] = np.where(lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['HRL'][0],lineups_merged['hrL'])
lineups_merged['hrL'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['HRL'][1],lineups_merged['hrL'])
lineups_merged['boL'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['BOL'][0],lineups_merged['boL'])
lineups_merged['boL'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['BOL'][1],lineups_merged['boL'])
lineups_merged['bbR'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['BBR'][0],lineups_merged['bbR'])
lineups_merged['bbR'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['BBR'][1],lineups_merged['bbR'])
lineups_merged['kR'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['SOR'][0],lineups_merged['kR'])
lineups_merged['kR'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['SOR'][1],lineups_merged['kR'])
lineups_merged['1bR'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['1bR'][0],lineups_merged['1bR'])
lineups_merged['1bR'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['1bR'][1],lineups_merged['1bR'])
lineups_merged['2bR'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['2bR'][0],lineups_merged['2bR'])
lineups_merged['2bR'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['2bR'][1],lineups_merged['2bR'])
lineups_merged['3bR'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['3bR'][0],lineups_merged['3bR'])
lineups_merged['3bR'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['3bR'][1],lineups_merged['3bR'])
lineups_merged['hrR'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['HRR'][0],lineups_merged['hrR'])
lineups_merged['hrR'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['HRR'][1],lineups_merged['hrR'])
lineups_merged['boR'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['BOR'][0],lineups_merged['boR'])
lineups_merged['boR'] = np.where((lineups_merged['mlbamid'].isnull.()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['BOR'][1],lineups_merged['boR'])

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

###Function To Simulate One Game
def game_sim(away_lineup, home_lineup, away_pitcher, home_pitcher):
    inning = 1
    half = 'top'
    away_batter = 0
    home_batter = 0
    away_runs = 0
    home_runs = 0
    away_box_score = pandas.DataFrame({'Name' : away_lineup['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
    home_box_score = pandas.DataFrame({'Name' : home_lineup['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
    
    while (inning < 10):
      if (half == 'top'):
        outs = 0
        first_base = ''
        second_base = ''
        third_base = ''
        while (outs < 3):
          pa_result = at_bat(home_pitcher,pandas.DataFrame(away_lineup.iloc[away_batter]).T.reset_index(drop = True))
          
          if(pa_result == 'bo' or pa_result == 'so'):
            outs = outs + 1
            away_box_score['PA'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['PA'] + 1, away_box_score['PA'])
            
          if(pa_result == 'bb'):
            runs_before = away_runs                                  
            if (third_base != '' and second_base != '' and first_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==third_base, away_box_score['R'] + 1, away_box_score['R'])
              third_base = second_base
              second_base = first_base
              first_base = ''
            elif (third_base == '' and second_base != '' and first_base != ''):
              third_base = second_base
              second_base = first_base
              first_base = ''
            elif (third_base == '' and second_base == '' and first_base != ''):
              second_base = first_base
              first_base = ''
            elif (third_base != '' and second_base == '' and first_base != ''):
              second_base = first_base
              first_base = ''
            else:
              third_base = third_base
              second_base = second_base
              first_base = ''
            first_base = away_lineup.at[away_batter,"name"]
            runs_diff = away_runs - runs_before
            away_box_score['PA'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['PA'] + 1, away_box_score['PA'])
            away_box_score['BB'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['BB'] + 1, away_box_score['BB'])
            away_box_score['RBI'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['RBI'] + runs_diff, away_box_score['RBI'])
                                               
          if(pa_result == '1b'):
            runs_before = away_runs
            if (third_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==third_base, away_box_score['R'] + 1, away_box_score['R'])
              third_base = ''
            if (second_base != ''):
              third_base = second_base
              second_base = ''
            if (first_base != ''):
              second_base = first_base
              first_base = ''
            first_base = away_lineup.at[away_batter,"name"]
            runs_diff = away_runs - runs_before
            away_box_score['PA'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['PA'] + 1, away_box_score['PA'])
            away_box_score['H'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['H'] + 1, away_box_score['H'])
            away_box_score['Single'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['Single'] + 1, away_box_score['Single'])
            away_box_score['RBI'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['RBI'] + runs_diff, away_box_score['RBI'])
                          
          if(pa_result == '2b'):
            runs_before = away_runs
            if (third_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==third_base, away_box_score['R'] + 1, away_box_score['R'])
              third_base = ''
            if (second_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==second_base, away_box_score['R'] + 1, away_box_score['R'])
              second_base = ''
            if (first_base != ''):
              third_base = first_base
              first_base = ''
            second_base = away_lineup.at[away_batter,"name"]
            runs_diff = away_runs - runs_before
            away_box_score['PA'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['PA'] + 1, away_box_score['PA'])
            away_box_score['H'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['H'] + 1, away_box_score['H'])
            away_box_score['Double'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['Double'] + 1, away_box_score['Double'])
            away_box_score['RBI'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['RBI'] + runs_diff, away_box_score['RBI'])                                            
                        
          if(pa_result == '3b'):
            runs_before = away_runs
            if (third_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==third_base, away_box_score['R'] + 1, away_box_score['R'])                                               
              third_base = ''
            if (second_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==second_base, away_box_score['R'] + 1, away_box_score['R'])                                               
              second_base = ''
            if (first_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==first_base, away_box_score['R'] + 1, away_box_score['R'])                                                
              first_base = ''
            third_base = away_lineup.at[away_batter,"name"]
            runs_diff = away_runs - runs_before
            away_box_score['PA'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['PA'] + 1, away_box_score['PA'])
            away_box_score['H'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['H'] + 1, away_box_score['H'])
            away_box_score['Triple'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['Triple'] + 1, away_box_score['Triple'])
            away_box_score['RBI'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['RBI'] + runs_diff, away_box_score['RBI'])                                                                                      
                  
          if(pa_result == 'hr'):
            runs_before = away_runs
            if (third_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==third_base, away_box_score['R'] + 1, away_box_score['R'])                                               
              third_base = ''
            if (second_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==second_base, away_box_score['R'] + 1, away_box_score['R'])                                               
              second_base = ''
            if (first_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==first_base, away_box_score['R'] + 1, away_box_score['R'])                                                
              first_base = ''
            away_runs = away_runs + 1
            away_box_score['R'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['R'] + 1, away_box_score['R'])
            runs_diff = away_runs - runs_before
            away_box_score['PA'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['PA'] + 1, away_box_score['PA'])
            away_box_score['H'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['H'] + 1, away_box_score['H'])
            away_box_score['HR'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['Triple'] + 1, away_box_score['Triple'])
            away_box_score['RBI'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['RBI'] + runs_diff, away_box_score['RBI'])                                                                                      
                                                  
          
          if (away_batter == 8):
            away_batter = 0
          else:
            away_batter = away_batter + 1
      
            
      half = 'bottom'
      if (inning == 9 and half == 'bottom' and (home_runs > away_runs)):
          break
      if (half == 'bottom'):
        outs = 0
        first_base = ''
        second_base = ''
        third_base = ''
        while (outs < 3):
          pa_result = at_bat(away_pitcher,pandas.DataFrame(home_lineup.iloc[home_batter]).T.reset_index(drop = True))
          
          if(pa_result == 'bo' or pa_result == 'so'):
            outs = outs + 1
            home_box_score['PA'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['PA'] + 1, home_box_score['PA'])
                                               
          if(pa_result == 'bb'):
            runs_before = home_runs                                  
            if (third_base != '' and second_base != '' and first_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==third_base, home_box_score['R'] + 1, home_box_score['R'])
              third_base = second_base
              second_base = first_base
              first_base = ''
            elif (third_base == '' and second_base != '' and first_base != ''):
              third_base = second_base
              second_base = first_base
              first_base = ''
            elif (third_base == '' and second_base == '' and first_base != ''):
              second_base = first_base
              first_base = ''
            elif (third_base != '' and second_base == '' and first_base != ''):
              second_base = first_base
              first_base = ''
            else:
              third_base = third_base
              second_base = second_base
              first_base = ''
            first_base = home_lineup.at[home_batter,"name"]
            runs_diff = home_runs - runs_before
            home_box_score['PA'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['PA'] + 1, home_box_score['PA'])
            home_box_score['BB'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['BB'] + 1, home_box_score['BB'])
            home_box_score['RBI'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['RBI'] + runs_diff, home_box_score['RBI'])
                                               
          if(pa_result == '1b'):
            runs_before = home_runs
            if (third_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==third_base, home_box_score['R'] + 1, home_box_score['R'])
              third_base = ''
            if (second_base != ''):
              third_base = second_base
              second_base = ''
            if (first_base != ''):
              second_base = first_base
              first_base = ''
            first_base = home_lineup.at[home_batter,"name"]
            runs_diff = home_runs - runs_before
            home_box_score['PA'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['PA'] + 1, home_box_score['PA'])
            home_box_score['H'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['H'] + 1, home_box_score['H'])
            home_box_score['Single'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['Single'] + 1, home_box_score['Single'])
            home_box_score['RBI'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['RBI'] + runs_diff, home_box_score['RBI'])
                          
          if(pa_result == '2b'):
            runs_before = home_runs
            if (third_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==third_base, home_box_score['R'] + 1, home_box_score['R'])
              third_base = ''
            if (second_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==second_base, home_box_score['R'] + 1, home_box_score['R'])
              second_base = ''
            if (first_base != ''):
              third_base = first_base
              first_base = ''
            second_base = home_lineup.at[home_batter,"name"]
            runs_diff = home_runs - runs_before
            home_box_score['PA'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['PA'] + 1, home_box_score['PA'])
            home_box_score['H'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['H'] + 1, home_box_score['H'])
            home_box_score['Double'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['Double'] + 1, home_box_score['Double'])
            home_box_score['RBI'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['RBI'] + runs_diff, home_box_score['RBI'])                                            
                        
          if(pa_result == '3b'):
            runs_before = home_runs
            if (third_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==third_base, home_box_score['R'] + 1, home_box_score['R'])                                               
              third_base = ''
            if (second_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==second_base, home_box_score['R'] + 1, home_box_score['R'])                                               
              second_base = ''
            if (first_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==first_base, home_box_score['R'] + 1, home_box_score['R'])                                                
              first_base = ''
            third_base = home_lineup.at[home_batter,"name"]
            runs_diff = home_runs - runs_before
            home_box_score['PA'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['PA'] + 1, home_box_score['PA'])
            home_box_score['H'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['H'] + 1, home_box_score['H'])
            home_box_score['Triple'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['Triple'] + 1, home_box_score['Triple'])
            home_box_score['RBI'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['RBI'] + runs_diff, home_box_score['RBI'])                                                                                      
                  
          if(pa_result == 'hr'):
            runs_before = home_runs
            if (third_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==third_base, home_box_score['R'] + 1, home_box_score['R'])                                               
              third_base = ''
            if (second_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==second_base, home_box_score['R'] + 1, home_box_score['R'])                                               
              second_base = ''
            if (first_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==first_base, home_box_score['R'] + 1, home_box_score['R'])                                                
              first_base = ''
            home_runs = home_runs + 1
            home_box_score['R'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['R'] + 1, home_box_score['R'])
            runs_diff = home_runs - runs_before
            home_box_score['PA'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['PA'] + 1, home_box_score['PA'])
            home_box_score['H'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['H'] + 1, home_box_score['H'])
            home_box_score['HR'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['Triple'] + 1, home_box_score['Triple'])
            home_box_score['RBI'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['RBI'] + runs_diff, home_box_score['RBI'])       
          
          if (home_batter == 8):
            home_batter = 0
          else:
            home_batter = home_batter + 1
        half = 'top'
        inning = inning + 1
    
    return(away_box_score, home_box_score)    

if len(teams) >= 2:                                               
  away_lineup_1, home_lineup_1, away_pitcher_1, home_pitcher_1 = set_lineups(0)
  away_box_score_total_1 = pandas.DataFrame({'Name' : away_lineup_1['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_1 = pandas.DataFrame({'Name' : home_lineup_1['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_wins_1 = 0
  
  for i in range(1000):
    away_box_1, home_box_1 = game_sim(away_lineup_1, home_lineup_1, away_pitcher_1, home_pitcher_1)
    if Total = home_box_1['R'].sum() > away_box_1['R'].sum:
       home_wins_1 = home_wins_1 + 1
    away_box_score_total_1 = away_box_score_total_1 + away_box_1
    home_box_score_total_1 = home_box_score_total_1 + home_box_1

  del away_box_score_total_1['Name']
  away_box_score_total_1 = away_box_score_total_1/1000
  away_box_score_total_1['Name'] = away_lineup_1['name'].tolist()
  del home_box_score_total_1['Name']
  home_box_score_total_1 = home_box_score_total_1/1000
  home_box_score_total_1['Name'] = home_lineup_1['name'].tolist()
  home_win_percentage_1 = home_wins_1/1000
  
if len(teams) >= 4:                                               
  away_lineup_2, home_lineup_2, away_pitcher_2, home_pitcher_2 = set_lineups(2)
  away_box_score_total_2 = pandas.DataFrame({'Name' : away_lineup_2['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_2 = pandas.DataFrame({'Name' : home_lineup_2['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_2, home_box_2 = game_sim(away_lineup_2, home_lineup_2, away_pitcher_2, home_pitcher_2)
    away_box_score_total_2 = away_box_score_total_2 + away_box_2
    home_box_score_total_2 = home_box_score_total_2 + home_box_2

  del away_box_score_total_2['Name']
  away_box_score_total_2 = away_box_score_total_2/1000
  away_box_score_total_2['Name'] = away_lineup_2['name'].tolist()
  del home_box_score_total_2['Name']
  home_box_score_total_2 = home_box_score_total_2/1000
  home_box_score_total_2['Name'] = home_lineup_2['name'].tolist()

if len(teams) >= 6:                                               
  away_lineup_3, home_lineup_3, away_pitcher_3, home_pitcher_3 = set_lineups(4)
  away_box_score_total_3 = pandas.DataFrame({'Name' : away_lineup_3['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_3 = pandas.DataFrame({'Name' : home_lineup_3['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_3, home_box_3 = game_sim(away_lineup_3, home_lineup_3, away_pitcher_3, home_pitcher_3)
    away_box_score_total_3 = away_box_score_total_3 + away_box_3
    home_box_score_total_3 = home_box_score_total_3 + home_box_3

  del away_box_score_total_3['Name']
  away_box_score_total_3 = away_box_score_total_3/1000
  away_box_score_total_3['Name'] = away_lineup_3['name'].tolist()
  del home_box_score_total_3['Name']
  home_box_score_total_3 = home_box_score_total_3/1000
  home_box_score_total_3['Name'] = home_lineup_3['name'].tolist()

if len(teams) >= 8:                                               
  away_lineup_4, home_lineup_4, away_pitcher_4, home_pitcher_4 = set_lineups(6)
  away_box_score_total_4 = pandas.DataFrame({'Name' : away_lineup_4['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_4 = pandas.DataFrame({'Name' : home_lineup_4['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_4, home_box_4 = game_sim(away_lineup_4, home_lineup_4, away_pitcher_4, home_pitcher_4)
    away_box_score_total_4 = away_box_score_total_4 + away_box_4
    home_box_score_total_4 = home_box_score_total_4 + home_box_4

  del away_box_score_total_4['Name']
  away_box_score_total_4 = away_box_score_total_4/1000
  away_box_score_total_4['Name'] = away_lineup_4['name'].tolist()
  del home_box_score_total_4['Name']
  home_box_score_total_4 = home_box_score_total_4/1000
  home_box_score_total_4['Name'] = home_lineup_4['name'].tolist()

if len(teams) >= 10:                                               
  away_lineup_5, home_lineup_5, away_pitcher_5, home_pitcher_5 = set_lineups(8)
  away_box_score_total_5 = pandas.DataFrame({'Name' : away_lineup_5['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_5 = pandas.DataFrame({'Name' : home_lineup_5['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_5, home_box_5 = game_sim(away_lineup_5, home_lineup_5, away_pitcher_5, home_pitcher_5)
    away_box_score_total_5 = away_box_score_total_5 + away_box_5
    home_box_score_total_5 = home_box_score_total_5 + home_box_5

  del away_box_score_total_5['Name']
  away_box_score_total_5 = away_box_score_total_5/1000
  away_box_score_total_5['Name'] = away_lineup_5['name'].tolist()
  del home_box_score_total_5['Name']
  home_box_score_total_5 = home_box_score_total_5/1000
  home_box_score_total_5['Name'] = home_lineup_5['name'].tolist()

if len(teams) >= 12:                                               
  away_lineup_6, home_lineup_6, away_pitcher_6, home_pitcher_6 = set_lineups(10)
  away_box_score_total_6 = pandas.DataFrame({'Name' : away_lineup_6['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_6 = pandas.DataFrame({'Name' : home_lineup_6['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_6, home_box_6 = game_sim(away_lineup_6, home_lineup_6, away_pitcher_6, home_pitcher_6)
    away_box_score_total_6 = away_box_score_total_6 + away_box_6
    home_box_score_total_6 = home_box_score_total_6 + home_box_6

  del away_box_score_total_6['Name']
  away_box_score_total_6 = away_box_score_total_6/1000
  away_box_score_total_6['Name'] = away_lineup_6['name'].tolist()
  del home_box_score_total_6['Name']
  home_box_score_total_6 = home_box_score_total_6/1000
  home_box_score_total_6['Name'] = home_lineup_6['name'].tolist()

if len(teams) >= 14:                                               
  away_lineup_7, home_lineup_7, away_pitcher_7, home_pitcher_7 = set_lineups(12)
  away_box_score_total_7 = pandas.DataFrame({'Name' : away_lineup_7['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_7 = pandas.DataFrame({'Name' : home_lineup_7['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_7, home_box_7 = game_sim(away_lineup_7, home_lineup_7, away_pitcher_7, home_pitcher_7)
    away_box_score_total_7 = away_box_score_total_7 + away_box_7
    home_box_score_total_7 = home_box_score_total_7 + home_box_7

  del away_box_score_total_7['Name']
  away_box_score_total_7 = away_box_score_total_7/1000
  away_box_score_total_7['Name'] = away_lineup_7['name'].tolist()
  del home_box_score_total_7['Name']
  home_box_score_total_7 = home_box_score_total_7/1000
  home_box_score_total_7['Name'] = home_lineup_7['name'].tolist()

if len(teams) >= 16:                                               
  away_lineup_8, home_lineup_8, away_pitcher_8, home_pitcher_8 = set_lineups(14)
  away_box_score_total_8 = pandas.DataFrame({'Name' : away_lineup_8['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_8 = pandas.DataFrame({'Name' : home_lineup_8['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_8, home_box_8 = game_sim(away_lineup_8, home_lineup_8, away_pitcher_8, home_pitcher_8)
    away_box_score_total_8 = away_box_score_total_8 + away_box_8
    home_box_score_total_8 = home_box_score_total_8 + home_box_8

  del away_box_score_total_8['Name']
  away_box_score_total_8 = away_box_score_total_8/1000
  away_box_score_total_8['Name'] = away_lineup_8['name'].tolist()
  del home_box_score_total_8['Name']
  home_box_score_total_8 = home_box_score_total_8/1000
  home_box_score_total_8['Name'] = home_lineup_8['name'].tolist()

if len(teams) >= 18:                                               
  away_lineup_9, home_lineup_9, away_pitcher_9, home_pitcher_9 = set_lineups(16)
  away_box_score_total_9 = pandas.DataFrame({'Name' : away_lineup_9['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_9 = pandas.DataFrame({'Name' : home_lineup_9['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_9, home_box_9 = game_sim(away_lineup_9, home_lineup_9, away_pitcher_9, home_pitcher_9)
    away_box_score_total_9 = away_box_score_total_9 + away_box_9
    home_box_score_total_9 = home_box_score_total_9 + home_box_9

  del away_box_score_total_9['Name']
  away_box_score_total_9 = away_box_score_total_9/1000
  away_box_score_total_9['Name'] = away_lineup_9['name'].tolist()
  del home_box_score_total_9['Name']
  home_box_score_total_9 = home_box_score_total_9/1000
  home_box_score_total_9['Name'] = home_lineup_9['name'].tolist()

if len(teams) >= 20:                                               
  away_lineup_10, home_lineup_10, away_pitcher_10, home_pitcher_10 = set_lineups(18)
  away_box_score_total_10 = pandas.DataFrame({'Name' : away_lineup_10['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_10 = pandas.DataFrame({'Name' : home_lineup_10['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_10, home_box_10 = game_sim(away_lineup_10, home_lineup_10, away_pitcher_10, home_pitcher_10)
    away_box_score_total_10 = away_box_score_total_10 + away_box_10
    home_box_score_total_10 = home_box_score_total_10 + home_box_10

  del away_box_score_total_10['Name']
  away_box_score_total_10 = away_box_score_total_10/1000
  away_box_score_total_10['Name'] = away_lineup_10['name'].tolist()
  del home_box_score_total_10['Name']
  home_box_score_total_10 = home_box_score_total_10/1000
  home_box_score_total_10['Name'] = home_lineup_10['name'].tolist()

if len(teams) >= 22:                                               
  away_lineup_11, home_lineup_11, away_pitcher_11, home_pitcher_11 = set_lineups(20)
  away_box_score_total_11 = pandas.DataFrame({'Name' : away_lineup_11['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_11 = pandas.DataFrame({'Name' : home_lineup_11['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_11, home_box_11 = game_sim(away_lineup_11, home_lineup_11, away_pitcher_11, home_pitcher_11)
    away_box_score_total_11 = away_box_score_total_11 + away_box_11
    home_box_score_total_11 = home_box_score_total_11 + home_box_11

  del away_box_score_total_11['Name']
  away_box_score_total_11 = away_box_score_total_11/1000
  away_box_score_total_11['Name'] = away_lineup_11['name'].tolist()
  del home_box_score_total_11['Name']
  home_box_score_total_11 = home_box_score_total_11/1000
  home_box_score_total_11['Name'] = home_lineup_11['name'].tolist()

if len(teams) >= 24:                                               
  away_lineup_12, home_lineup_12, away_pitcher_12, home_pitcher_12 = set_lineups(22)
  away_box_score_total_12 = pandas.DataFrame({'Name' : away_lineup_12['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_12 = pandas.DataFrame({'Name' : home_lineup_12['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_12, home_box_12 = game_sim(away_lineup_12, home_lineup_12, away_pitcher_12, home_pitcher_12)
    away_box_score_total_12 = away_box_score_total_12 + away_box_12
    home_box_score_total_12 = home_box_score_total_12 + home_box_12

  del away_box_score_total_12['Name']
  away_box_score_total_12 = away_box_score_total_12/1000
  away_box_score_total_12['Name'] = away_lineup_12['name'].tolist()
  del home_box_score_total_12['Name']
  home_box_score_total_12 = home_box_score_total_12/1000
  home_box_score_total_12['Name'] = home_lineup_12['name'].tolist()

if len(teams) >= 26:                                               
  away_lineup_13, home_lineup_13, away_pitcher_13, home_pitcher_13 = set_lineups(24)
  away_box_score_total_13 = pandas.DataFrame({'Name' : away_lineup_13['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_13 = pandas.DataFrame({'Name' : home_lineup_13['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_13, home_box_13 = game_sim(away_lineup_13, home_lineup_13, away_pitcher_13, home_pitcher_13)
    away_box_score_total_13 = away_box_score_total_13 + away_box_13
    home_box_score_total_13 = home_box_score_total_13 + home_box_13

  del away_box_score_total_13['Name']
  away_box_score_total_13 = away_box_score_total_13/1000
  away_box_score_total_13['Name'] = away_lineup_13['name'].tolist()
  del home_box_score_total_13['Name']
  home_box_score_total_13 = home_box_score_total_13/1000
  home_box_score_total_13['Name'] = home_lineup_13['name'].tolist()

if len(teams) >= 28:                                               
  away_lineup_14, home_lineup_14, away_pitcher_14, home_pitcher_14 = set_lineups(26)
  away_box_score_total_14 = pandas.DataFrame({'Name' : away_lineup_14['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_14 = pandas.DataFrame({'Name' : home_lineup_14['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_14, home_box_14 = game_sim(away_lineup_14, home_lineup_14, away_pitcher_14, home_pitcher_14)
    away_box_score_total_14 = away_box_score_total_14 + away_box_14
    home_box_score_total_14 = home_box_score_total_14 + home_box_14

  del away_box_score_total_14['Name']
  away_box_score_total_14 = away_box_score_total_14/1000
  away_box_score_total_14['Name'] = away_lineup_14['name'].tolist()
  del home_box_score_total_14['Name']
  home_box_score_total_14 = home_box_score_total_14/1000
  home_box_score_total_14['Name'] = home_lineup_14['name'].tolist()

if len(teams) >= 30:                                               
  away_lineup_15, home_lineup_15, away_pitcher_15, home_pitcher_15 = set_lineups(28)
  away_box_score_total_15 = pandas.DataFrame({'Name' : away_lineup_15['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_15 = pandas.DataFrame({'Name' : home_lineup_15['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_15, home_box_15 = game_sim(away_lineup_15, home_lineup_15, away_pitcher_15, home_pitcher_15)
    away_box_score_total_15 = away_box_score_total_15 + away_box_15
    home_box_score_total_15 = home_box_score_total_15 + home_box_15

  del away_box_score_total_15['Name']
  away_box_score_total_15 = away_box_score_total_15/1000
  away_box_score_total_15['Name'] = away_lineup_15['name'].tolist()
  del home_box_score_total_15['Name']
  home_box_score_total_15 = home_box_score_total_15/1000
  home_box_score_total_15['Name'] = home_lineup_15['name'].tolist()

if len(teams) >= 32:                                               
  away_lineup_16, home_lineup_16, away_pitcher_16, home_pitcher_16 = set_lineups(30)
  away_box_score_total_16 = pandas.DataFrame({'Name' : away_lineup_16['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_16 = pandas.DataFrame({'Name' : home_lineup_16['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_16, home_box_16 = game_sim(away_lineup_16, home_lineup_16, away_pitcher_16, home_pitcher_16)
    away_box_score_total_16 = away_box_score_total_16 + away_box_16
    home_box_score_total_16 = home_box_score_total_16 + home_box_16

  del away_box_score_total_16['Name']
  away_box_score_total_16 = away_box_score_total_16/1000
  away_box_score_total_16['Name'] = away_lineup_16['name'].tolist()
  del home_box_score_total_16['Name']
  home_box_score_total_16 = home_box_score_total_16/1000
  home_box_score_total_16['Name'] = home_lineup_16['name'].tolist()

if len(teams) >= 34:                                               
  away_lineup_17, home_lineup_17, away_pitcher_17, home_pitcher_17 = set_lineups(32)
  away_box_score_total_17 = pandas.DataFrame({'Name' : away_lineup_17['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_17 = pandas.DataFrame({'Name' : home_lineup_17['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_17, home_box_17 = game_sim(away_lineup_17, home_lineup_17, away_pitcher_17, home_pitcher_17)
    away_box_score_total_17 = away_box_score_total_17 + away_box_17
    home_box_score_total_17 = home_box_score_total_17 + home_box_17

  del away_box_score_total_17['Name']
  away_box_score_total_17 = away_box_score_total_17/1000
  away_box_score_total_17['Name'] = away_lineup_17['name'].tolist()
  del home_box_score_total_17['Name']
  home_box_score_total_17 = home_box_score_total_17/1000
  home_box_score_total_17['Name'] = home_lineup_17['name'].tolist()

if len(teams) >= 36:                                               
  away_lineup_18, home_lineup_18, away_pitcher_18, home_pitcher_18 = set_lineups(34)
  away_box_score_total_18 = pandas.DataFrame({'Name' : away_lineup_18['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_18 = pandas.DataFrame({'Name' : home_lineup_18['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_18, home_box_18 = game_sim(away_lineup_18, home_lineup_18, away_pitcher_18, home_pitcher_18)
    away_box_score_total_18 = away_box_score_total_18 + away_box_18
    home_box_score_total_18 = home_box_score_total_18 + home_box_18

  del away_box_score_total_18['Name']
  away_box_score_total_18 = away_box_score_total_18/1000
  away_box_score_total_18['Name'] = away_lineup_18['name'].tolist()
  del home_box_score_total_18['Name']
  home_box_score_total_18 = home_box_score_total_18/1000
  home_box_score_total_18['Name'] = home_lineup_18['name'].tolist()

if len(teams) >= 38:                                               
  away_lineup_19, home_lineup_19, away_pitcher_19, home_pitcher_19 = set_lineups(36)
  away_box_score_total_19 = pandas.DataFrame({'Name' : away_lineup_19['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_19 = pandas.DataFrame({'Name' : home_lineup_19['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_19, home_box_19 = game_sim(away_lineup_19, home_lineup_19, away_pitcher_19, home_pitcher_19)
    away_box_score_total_19 = away_box_score_total_19 + away_box_19
    home_box_score_total_19 = home_box_score_total_19 + home_box_19

  del away_box_score_total_19['Name']
  away_box_score_total_19 = away_box_score_total_19/1000
  away_box_score_total_19['Name'] = away_lineup_19['name'].tolist()
  del home_box_score_total_19['Name']
  home_box_score_total_19 = home_box_score_total_19/1000
  home_box_score_total_19['Name'] = home_lineup_19['name'].tolist()

if len(teams) >= 40:                                               
  away_lineup_20, home_lineup_20, away_pitcher_20, home_pitcher_20 = set_lineups(38)
  away_box_score_total_20 = pandas.DataFrame({'Name' : away_lineup_20['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
  home_box_score_total_20 = pandas.DataFrame({'Name' : home_lineup_20['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])

  for i in range(1000):
    away_box_20, home_box_20 = game_sim(away_lineup_20, home_lineup_20, away_pitcher_20, home_pitcher_20)
    away_box_score_total_20 = away_box_score_total_20 + away_box_20
    home_box_score_total_20 = home_box_score_total_20 + home_box_20

  del away_box_score_total_20['Name']
  away_box_score_total_20 = away_box_score_total_20/1000
  away_box_score_total_20['Name'] = away_lineup_20['name'].tolist()
  del home_box_score_total_20['Name']
  home_box_score_total_20 = home_box_score_total_20/1000
  home_box_score_total_20['Name'] = home_lineup_20['name'].tolist()

stop = timeit.default_timer()

print(stop - start)
