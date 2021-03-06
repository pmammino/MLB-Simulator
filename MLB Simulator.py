import bs4
import requests
import pandas
import timeit
import numpy as np
import difflib 



## Function Definitions

def set_lineups(n):
  away_lineup = list_lineups[n].reset_index(drop = True)
  home_lineup = list_lineups[n + 1].reset_index(drop = True)
  away_pitcher = pandas.DataFrame(pitchers.iloc[n]).T.reset_index(drop = True)
  home_pitcher = pandas.DataFrame(pitchers.iloc[n+1]).T.reset_index(drop = True)
  return(away_lineup, home_lineup, away_pitcher, home_pitcher)

def at_bat(pitcher,hitter):
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
    
    probs = ['1b', '2b', '3b', 'hr', 'bb', 'so', 'bo']
    probs = [np1b, np2b, np3b, nphr, npbb, npso, npbo]
    
    return(probs)
  
def moneyline_odds_calc(implied_prob):
  implied_prob_convert = implied_prob * 100
  if implied_prob_convert >= 50:
    odds = -(implied_prob_convert/(100-implied_prob_convert))*100
  else:
    odds =((100-implied_prob_convert)/implied_prob_convert)*100
    
  return(odds)

def game_repeater(num_sims, lineup_num,away_team,home_team):  
    away_lineup, home_lineup, away_pitcher, home_pitcher = set_lineups(lineup_num)
    away_box_score_total = pandas.DataFrame({'Name' : away_lineup['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
    home_box_score_total = pandas.DataFrame({'Name' : home_lineup['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
    away_pitcher_box_score_total = pandas.DataFrame({'Name' : away_pitcher['name'].tolist(),'IP' : [0],'H': [0],'BB' : [0],'R':[0], 'K' : [0]},columns = ['Name', 'IP', 'H', 'BB','R', 'K'])
    home_pitcher_box_score_total = pandas.DataFrame({'Name' : home_pitcher['name'].tolist(),'IP' : [0],'H': [0],'BB' : [0],'R':[0], 'K' : [0]},columns = ['Name', 'IP', 'H', 'BB','R', 'K'])
    home_wins = 0
    
    for i in range(num_sims):
      away_box, home_box, away_pitcher_box, home_pitcher_box = game_sim(away_team,home_team, away_lineup, home_lineup, away_pitcher, home_pitcher)
      if home_box['R'].sum() > away_box['R'].sum():
         home_wins = home_wins + 1
      away_box_score_total = away_box_score_total + away_box
      home_box_score_total = home_box_score_total + home_box
      away_pitcher_box_score_total = away_pitcher_box_score_total + away_pitcher_box
      home_pitcher_box_score_total = home_pitcher_box_score_total + home_pitcher_box
    
    del away_box_score_total['Name']
    away_box_score_total = away_box_score_total/num_sims
    away_box_score_total['Name'] = away_lineup['name'].tolist()
    del home_box_score_total['Name']
    home_box_score_total = home_box_score_total/num_sims
    home_box_score_total['Name'] = home_lineup['name'].tolist()
    del away_pitcher_box_score_total['Name']
    away_pitcher_box_score_total = away_pitcher_box_score_total/num_sims
    away_pitcher_box_score_total['Name'] = away_pitcher['name'].tolist()
    del home_pitcher_box_score_total['Name']
    home_pitcher_box_score_total = home_pitcher_box_score_total/num_sims
    home_pitcher_box_score_total['Name'] = home_pitcher['name'].tolist()
    
    home_win_percentage = home_wins/num_sims
    odds_win = moneyline_odds_calc(home_win_percentage)
    home_pythagwin_percentage = (home_box_score_total['R'].sum() ** 1.82)/((home_box_score_total['R'].sum() ** 1.82) + (away_box_score_total['R'].sum() ** 1.82))
    odds_pythagwin = moneyline_odds_calc(home_pythagwin_percentage)
    away_runs_scored = away_box_score_total['R'].sum()
    home_runs_scored = home_box_score_total['R'].sum()
    total_runs_scored = away_box_score_total['R'].sum() + home_box_score_total['R'].sum()
    
    return(away_box_score_total, home_box_score_total, away_pitcher_box_score_total, home_pitcher_box_score_total, odds_win, odds_pythagwin, away_runs_scored, home_runs_scored, total_runs_scored)
  
###Function To Simulate One Game
def game_sim(away_team, home_team,away_lineup, home_lineup, away_pitcher, home_pitcher):
    inning = 1
    half = 'top'
    away_batter = 0
    home_batter = 0
    away_runs = 0
    home_runs = 0
    away_starter_pc = 0
    home_starter_pc = 0
    away_pitcher_type = 'starter'
    home_pitcher_type = 'starter'
    away_bullpen = bullpens.loc[bullpens['Team'] == away_team].reset_index(drop = True)
    home_bullpen = bullpens.loc[bullpens['Team'] == home_team].reset_index(drop = True)
    away_bullpen_usage = bullpens_usage.loc[bullpens_usage['Team'] == away_team].reset_index(drop = True)
    home_bullpen_usage = bullpens_usage.loc[bullpens_usage['Team'] == home_team].reset_index(drop = True)
    away_box_score = pandas.DataFrame({'Name' : away_lineup['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H': [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R':[0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
    home_box_score = pandas.DataFrame({'Name' : home_lineup['name'].tolist(),'PA' : [0,0,0,0,0,0,0,0,0],'H' : [0,0,0,0,0,0,0,0,0],'BB' : [0,0,0,0,0,0,0,0,0],'Single' : [0,0,0,0,0,0,0,0,0],'Double' : [0,0,0,0,0,0,0,0,0],'Triple' : [0,0,0,0,0,0,0,0,0], 'HR' : [0,0,0,0,0,0,0,0,0], 'R' : [0,0,0,0,0,0,0,0,0], 'RBI' : [0,0,0,0,0,0,0,0,0]},columns = ['Name', 'PA', 'H', 'BB', 'Single', 'Double', 'Triple', 'HR', 'R', 'RBI'])
    away_pitcher_box_score = pandas.DataFrame({'Name' : away_pitcher['name'].tolist(),'IP' : [0],'H': [0],'BB' : [0],'R':[0], 'K' : [0]},columns = ['Name', 'IP', 'H', 'BB','R', 'K'])
    home_pitcher_box_score = pandas.DataFrame({'Name': home_pitcher['name'].tolist() ,'IP' : [0],'H': [0],'BB' : [0],'R':[0], 'K' : [0]},columns = ['Name', 'IP', 'H', 'BB','R', 'K'])
    
    
    while (inning < 10):
      if (half == 'top'):
        outs = 0
        first_base = ''
        second_base = ''
        third_base = ''
        while (outs < 3):
          pa_result = at_bat(home_pitcher,home_bullpen,home_bullpen_usage,home_pitcher_type,pandas.DataFrame(away_lineup.iloc[away_batter]).T.reset_index(drop = True))
          
          if(pa_result == 'so'):
            outs = outs + 1
            away_box_score['PA'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['PA'] + 1, away_box_score['PA'])
            if(home_pitcher_type == 'starter'):
              home_pitcher_box_score['K'] = home_pitcher_box_score['K'] + 1
              home_pitcher_box_score['IP'] = home_pitcher_box_score['IP'] + (1/3)
            
          if(pa_result == 'bo'):
            outs = outs + 1
            away_box_score['PA'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['PA'] + 1, away_box_score['PA'])
            if(home_pitcher_type == 'starter'):
              home_pitcher_box_score['IP'] = home_pitcher_box_score['IP'] + (1/3)
            
          if(pa_result == 'bb'):
            runs_before = away_runs                                  
            if (third_base != '' and second_base != '' and first_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==third_base, away_box_score['R'] + 1, away_box_score['R'])
              third_base = second_base
              second_base = first_base
              first_base = ''
              if(home_pitcher_type == 'starter'):
                home_pitcher_box_score['R'] = home_pitcher_box_score['R'] + 1
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
            if(home_pitcher_type == 'starter'):
                home_pitcher_box_score['BB'] = home_pitcher_box_score['BB'] + 1
            
          if(pa_result == '1b'):
            runs_before = away_runs
            if (third_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==third_base, away_box_score['R'] + 1, away_box_score['R'])
              if(home_pitcher_type == 'starter'):
                home_pitcher_box_score['R'] = home_pitcher_box_score['R'] + 1
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
            if(home_pitcher_type == 'starter'):
                home_pitcher_box_score['H'] = home_pitcher_box_score['H'] + 1
                
          if(pa_result == '2b'):
            runs_before = away_runs
            if (third_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==third_base, away_box_score['R'] + 1, away_box_score['R'])
              if(home_pitcher_type == 'starter'):
                home_pitcher_box_score['R'] = home_pitcher_box_score['R'] + 1
              third_base = ''
            if (second_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==second_base, away_box_score['R'] + 1, away_box_score['R'])
              if(home_pitcher_type == 'starter'):
                home_pitcher_box_score['R'] = home_pitcher_box_score['R'] + 1
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
            if(home_pitcher_type == 'starter'):
                home_pitcher_box_score['H'] = home_pitcher_box_score['H'] + 1
            
          if(pa_result == '3b'):
            runs_before = away_runs
            if (third_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==third_base, away_box_score['R'] + 1, away_box_score['R'])   
              if(home_pitcher_type == 'starter'):
                home_pitcher_box_score['R'] = home_pitcher_box_score['R'] + 1
              third_base = ''
            if (second_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==second_base, away_box_score['R'] + 1, away_box_score['R'])
              if(home_pitcher_type == 'starter'):
                home_pitcher_box_score['R'] = home_pitcher_box_score['R'] + 1
              second_base = ''
            if (first_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==first_base, away_box_score['R'] + 1, away_box_score['R'])
              if(home_pitcher_type == 'starter'):
                home_pitcher_box_score['R'] = home_pitcher_box_score['R'] + 1
              first_base = ''
            third_base = away_lineup.at[away_batter,"name"]
            runs_diff = away_runs - runs_before
            away_box_score['PA'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['PA'] + 1, away_box_score['PA'])
            away_box_score['H'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['H'] + 1, away_box_score['H'])
            away_box_score['Triple'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['Triple'] + 1, away_box_score['Triple'])
            away_box_score['RBI'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['RBI'] + runs_diff, away_box_score['RBI'])                                                                                      
            if(home_pitcher_type == 'starter'):
                home_pitcher_box_score['H'] = home_pitcher_box_score['H'] + 1
            
          if(pa_result == 'hr'):
            runs_before = away_runs
            if (third_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==third_base, away_box_score['R'] + 1, away_box_score['R']) 
              if(home_pitcher_type == 'starter'):
                home_pitcher_box_score['R'] = home_pitcher_box_score['R'] + 1
              third_base = ''
            if (second_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==second_base, away_box_score['R'] + 1, away_box_score['R'])
              if(home_pitcher_type == 'starter'):
                home_pitcher_box_score['R'] = home_pitcher_box_score['R'] + 1
              second_base = ''
            if (first_base != ''):
              away_runs = away_runs + 1
              away_box_score['R'] = np.where(away_box_score['Name']==first_base, away_box_score['R'] + 1, away_box_score['R']) 
              if(home_pitcher_type == 'starter'):
                home_pitcher_box_score['R'] = home_pitcher_box_score['R'] + 1
              first_base = ''
            away_runs = away_runs + 1
            away_box_score['R'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['R'] + 1, away_box_score['R'])
            if(home_pitcher_type == 'starter'):
                home_pitcher_box_score['R'] = home_pitcher_box_score['R'] + 1
            runs_diff = away_runs - runs_before
            away_box_score['PA'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['PA'] + 1, away_box_score['PA'])
            away_box_score['H'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['H'] + 1, away_box_score['H'])
            away_box_score['HR'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['Triple'] + 1, away_box_score['Triple'])
            away_box_score['RBI'] = np.where(away_box_score['Name']==away_lineup.at[away_batter,"name"], away_box_score['RBI'] + runs_diff, away_box_score['RBI'])                                                                                      
            if(home_pitcher_type == 'starter'):
                home_pitcher_box_score['H'] = home_pitcher_box_score['H'] + 1
          
          if(home_pitcher_type == 'starter'):  
             home_starter_pc = home_starter_pc + home_pitcher.at[0,"Pit/PA"] 
          if(home_pitcher_type == 'starter' and home_starter_pc > home_pitcher.at[0,"Pit/GS"]):
             home_pitcher_type = 'bullpen'                                      
          
          if (away_batter == 8):
            away_batter = 0
          else:
            away_batter = away_batter + 1
      
            
      half = 'bottom'
##      if (inning == 9 and half == 'bottom' and (home_runs > away_runs)):
##          break
      if (half == 'bottom'):
        outs = 0
        first_base = ''
        second_base = ''
        third_base = ''
        while (outs < 3):
          pa_result = at_bat(away_pitcher,away_bullpen,away_bullpen_usage,away_pitcher_type,pandas.DataFrame(home_lineup.iloc[home_batter]).T.reset_index(drop = True))
          
          if(pa_result == 'so'):
            outs = outs + 1
            home_box_score['PA'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['PA'] + 1, home_box_score['PA'])
            if(away_pitcher_type == 'starter'):
              away_pitcher_box_score['K'] = away_pitcher_box_score['K'] + 1
              away_pitcher_box_score['IP'] = away_pitcher_box_score['IP'] + (1/3)
            
          if(pa_result == 'bo'):
            outs = outs + 1
            home_box_score['PA'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['PA'] + 1, home_box_score['PA'])
            if(away_pitcher_type == 'starter'):
              away_pitcher_box_score['IP'] = away_pitcher_box_score['IP'] + (1/3)
          
          if(pa_result == 'bb'):
            runs_before = home_runs                                  
            if (third_base != '' and second_base != '' and first_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==third_base, home_box_score['R'] + 1, home_box_score['R'])
              if(away_pitcher_type == 'starter'):
                away_pitcher_box_score['R'] = away_pitcher_box_score['R'] + 1
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
            if(away_pitcher_type == 'starter'):
                away_pitcher_box_score['BB'] = away_pitcher_box_score['BB'] + 1
            
          if(pa_result == '1b'):
            runs_before = home_runs
            if (third_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==third_base, home_box_score['R'] + 1, home_box_score['R'])
              if(away_pitcher_type == 'starter'):
                away_pitcher_box_score['R'] = away_pitcher_box_score['R'] + 1
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
            if(away_pitcher_type == 'starter'):
                away_pitcher_box_score['H'] = away_pitcher_box_score['H'] + 1
            
          if(pa_result == '2b'):
            runs_before = home_runs
            if (third_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==third_base, home_box_score['R'] + 1, home_box_score['R'])
              if(away_pitcher_type == 'starter'):
                away_pitcher_box_score['R'] = away_pitcher_box_score['R'] + 1
              third_base = ''
            if (second_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==second_base, home_box_score['R'] + 1, home_box_score['R'])
              if(away_pitcher_type == 'starter'):
                away_pitcher_box_score['R'] = away_pitcher_box_score['R'] + 1
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
            if(away_pitcher_type == 'starter'):
                away_pitcher_box_score['H'] = away_pitcher_box_score['H'] + 1
            
          if(pa_result == '3b'):
            runs_before = home_runs
            if (third_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==third_base, home_box_score['R'] + 1, home_box_score['R'])
              if(away_pitcher_type == 'starter'):
                away_pitcher_box_score['R'] = away_pitcher_box_score['R'] + 1
              third_base = ''
            if (second_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==second_base, home_box_score['R'] + 1, home_box_score['R'])
              if(away_pitcher_type == 'starter'):
                away_pitcher_box_score['R'] = away_pitcher_box_score['R'] + 1
              second_base = ''
            if (first_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==first_base, home_box_score['R'] + 1, home_box_score['R']) 
              if(away_pitcher_type == 'starter'):
                away_pitcher_box_score['R'] = away_pitcher_box_score['R'] + 1
              first_base = ''
            third_base = home_lineup.at[home_batter,"name"]
            runs_diff = home_runs - runs_before
            home_box_score['PA'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['PA'] + 1, home_box_score['PA'])
            home_box_score['H'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['H'] + 1, home_box_score['H'])
            home_box_score['Triple'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['Triple'] + 1, home_box_score['Triple'])
            home_box_score['RBI'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['RBI'] + runs_diff, home_box_score['RBI'])                                                                                      
            if(away_pitcher_type == 'starter'):
                away_pitcher_box_score['H'] = away_pitcher_box_score['H'] + 1
            
          if(pa_result == 'hr'):
            runs_before = home_runs
            if (third_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==third_base, home_box_score['R'] + 1, home_box_score['R']) 
              if(away_pitcher_type == 'starter'):
                away_pitcher_box_score['R'] = away_pitcher_box_score['R'] + 1
              third_base = ''
            if (second_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==second_base, home_box_score['R'] + 1, home_box_score['R']) 
              if(away_pitcher_type == 'starter'):
                away_pitcher_box_score['R'] = away_pitcher_box_score['R'] + 1
              second_base = ''
            if (first_base != ''):
              home_runs = home_runs + 1
              home_box_score['R'] = np.where(home_box_score['Name']==first_base, home_box_score['R'] + 1, home_box_score['R'])
              if(away_pitcher_type == 'starter'):
                away_pitcher_box_score['R'] = away_pitcher_box_score['R'] + 1
              first_base = ''
            home_runs = home_runs + 1
            home_box_score['R'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['R'] + 1, home_box_score['R'])
            runs_diff = home_runs - runs_before
            home_box_score['PA'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['PA'] + 1, home_box_score['PA'])
            home_box_score['H'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['H'] + 1, home_box_score['H'])
            home_box_score['HR'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['Triple'] + 1, home_box_score['Triple'])
            home_box_score['RBI'] = np.where(home_box_score['Name']==home_lineup.at[home_batter,"name"], home_box_score['RBI'] + runs_diff, home_box_score['RBI'])       
            if(away_pitcher_type == 'starter'):
                away_pitcher_box_score['H'] = away_pitcher_box_score['H'] + 1
          if(away_pitcher_type == 'starter'):
            away_starter_pc = away_starter_pc + away_pitcher.at[0,"Pit/PA"]
          if (away_pitcher_type == 'starter' and away_starter_pc > away_pitcher.at[0,"Pit/GS"]):
              away_pitcher_type = 'bullpen'

          if (home_batter == 8):
            home_batter = 0
          else:
            home_batter = home_batter + 1
        half = 'top'
        inning = inning + 1
    
    return(away_box_score, home_box_score, away_pitcher_box_score, home_pitcher_box_score)  
  
start = timeit.default_timer()

#DATA SCRAPING
#
# scrape Steamer projection files

batter_steamer = pandas.read_csv("steamer_batter_2018.csv")
pitcher_steamer = pandas.read_csv("steamer_pitcher_2018.csv")

dummy_hitter_pitcher = pandas.read_excel("DummyHitter.xlsx", sheetname = "DummyHitter")
bullpens = pandas.read_excel("Bullpens.xlsx", sheetname = "Bullpens")
bullpens_usage = pandas.read_excel("Bullpens.xlsx", sheetname = "BullpensUsage")
starter_pitch_counts = pandas.read_excel("PitchCount.xlsx",sheetname = "Starters")
per_at_bat_pitch_counts = pandas.read_excel("PitchCount.xlsx",sheetname = "Pitches")


#
#
# pull lineups from Rotogrinders

res = requests.get('https://rotogrinders.com/lineups/mlb?date=2018-10-17&site=draftkings')
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

res2 = requests.get('https://rotogrinders.com/lineups/mlb?date=2018-10-17&site=draftkings')
soup2 = bs4.BeautifulSoup(res2.text, 'lxml')

list3 = []

for i in soup2.select('.shrt'):
    list3.append(i.text)
    
teams = pandas.DataFrame(list3)
teams[0] = np.where(teams[0]== 'WAS', 'WSN', teams[0])

res3 = requests.get('https://rotogrinders.com/lineups/mlb?date=2018-10-17&site=draftkings')
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
lineups_merged['kL'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['SOL'][1],lineups_merged['kL'])
lineups_merged['1bL'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['1bL'][0],lineups_merged['1bL'])
lineups_merged['1bL'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['1bL'][1],lineups_merged['1bL'])
lineups_merged['2bL'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['2bL'][0],lineups_merged['2bL'])
lineups_merged['2bL'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['2bL'][1],lineups_merged['2bL'])
lineups_merged['3bL'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['3bL'][0],lineups_merged['3bL'])
lineups_merged['3bL'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['3bL'][1],lineups_merged['3bL'])
lineups_merged['hrL'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['HRL'][0],lineups_merged['hrL'])
lineups_merged['hrL'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['HRL'][1],lineups_merged['hrL'])
lineups_merged['boL'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['BOL'][0],lineups_merged['boL'])
lineups_merged['boL'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['BOL'][1],lineups_merged['boL'])
lineups_merged['bbR'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['BBR'][0],lineups_merged['bbR'])
lineups_merged['bbR'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['BBR'][1],lineups_merged['bbR'])
lineups_merged['kR'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['SOR'][0],lineups_merged['kR'])
lineups_merged['kR'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['SOR'][1],lineups_merged['kR'])
lineups_merged['1bR'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['1bR'][0],lineups_merged['1bR'])
lineups_merged['1bR'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['1bR'][1],lineups_merged['1bR'])
lineups_merged['2bR'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['2bR'][0],lineups_merged['2bR'])
lineups_merged['2bR'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['2bR'][1],lineups_merged['2bR'])
lineups_merged['3bR'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['3bR'][0],lineups_merged['3bR'])
lineups_merged['3bR'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['3bR'][1],lineups_merged['3bR'])
lineups_merged['hrR'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['HRR'][0],lineups_merged['hrR'])
lineups_merged['hrR'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['HRR'][1],lineups_merged['hrR'])
lineups_merged['boR'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'L'), dummy_hitter_pitcher['BOR'][0],lineups_merged['boR'])
lineups_merged['boR'] = np.where((lineups_merged['mlbamid'].isnull()) & (lineups_merged['Bats'] == 'R'), dummy_hitter_pitcher['BOR'][1],lineups_merged['boR'])

merge_2 = pitcher_steamer[["name","mlbamid"]].drop_duplicates()

pitchers = pitchers.merge(merge_2, on = ["name"], how = "left")
pitchers["vRCode"] = "SP-0-vR-" + pitchers['mlbamid'].astype(str).replace('\.0', '', regex=True)
pitchers["vLCode"] = "SP-0-vL-" + pitchers['mlbamid'].astype(str).replace('\.0', '', regex=True)

pitchers = pitchers.merge(pitcher_steamer[["m_id", "BB", "K", "Single", "Double", "Triple", "HR", "BO"]], left_on = ["vRCode"], right_on = ["m_id"], how = "left")
pitchers = pitchers.rename(index=str, columns={"BB" : "bbR", "K" : "kR", "Single" : "1bR", "Double" : "2bR", "Triple" : "3bR", "HR" : "hrR", "BO" : "boR"})
pitchers = pitchers.merge(pitcher_steamer[["m_id", "BB", "K", "Single", "Double", "Triple", "HR", "BO"]], left_on = ["vLCode"], right_on = ["m_id"], how = "left")
pitchers = pitchers.rename(index=str, columns={"BB" : "bbL", "K" : "kL", "Single" : "1bL", "Double" : "2bL", "Triple" : "3bL", "HR" : "hrL", "BO" : "boL"})
per_at_bat_pitch_counts = per_at_bat_pitch_counts[['Name','Pit/PA']]
starter_pitch_counts = starter_pitch_counts[['Name','Pit/GS']]
per_at_bat_pitch_counts['Name'] = per_at_bat_pitch_counts['Name'].apply(lambda x: difflib.get_close_matches(x, merge_2['name']))
per_at_bat_pitch_counts = per_at_bat_pitch_counts[per_at_bat_pitch_counts.Name.astype(bool)]
per_at_bat_pitch_counts = per_at_bat_pitch_counts.reset_index(drop=True)
per_at_bat_pitch_counts['Name'] = [item[0] for item in per_at_bat_pitch_counts['Name']]
pitchers = pitchers.merge(per_at_bat_pitch_counts, left_on = ["name"], right_on = ["Name"], how = "left")
pitchers = pitchers.drop_duplicates(subset = ['name'])

starter_pitch_counts['Name'] = starter_pitch_counts['Name'].apply(lambda x: difflib.get_close_matches(x, merge_2['name']))
starter_pitch_counts = starter_pitch_counts[starter_pitch_counts.Name.astype(bool)]
starter_pitch_counts = starter_pitch_counts.reset_index(drop=True)
starter_pitch_counts['Name'] = [item[0] for item in starter_pitch_counts['Name']]
pitchers = pitchers.merge(starter_pitch_counts, left_on = ["name"], right_on = ["Name"], how = "left")
pitchers = pitchers.drop_duplicates(subset = ['name'])
pitchers = pitchers.drop('Name_x',axis = 1)
pitchers = pitchers.drop('Name_y',axis = 1)

stop = timeit.default_timer()
print('Data Manipulation Time:' + stop - start)
n = 9  #chunk row size
list_lineups = [lineups_merged[i:i+n] for i in range(0,lineups_merged.shape[0],n)]  

away_lineup, home_lineup, away_pitcher, home_pitcher = set_lineups(0)
results = at_bat(home_pitcher,pandas.DataFrame(away_lineup.iloc[0]).T.reset_index(drop = True))
print(results)

game_summary = pandas.DataFrame(columns=['Away Team', 'Home Team', 'Home Odds', 'Home Pythag Odds', 'Away Runs', 'Home Runs', 'Total Runs'])

start = timeit.default_timer()
if len(teams) >= 2:                                               
  away_box_score_total_1, home_box_score_total_1,away_pitcher_box_score_total_1, home_pitcher_box_score_total_1, home_win_odds_1, home_pythagwin_odds_1, away_runs_scored_1, home_runs_scored_1, total_runs_scored_1 = game_repeater(1000,0,teams[0][0],teams[0][1])
  game_summary.loc[0] = [teams[0][0], teams[0][1], home_win_odds_1, home_pythagwin_odds_1, away_runs_scored_1, home_runs_scored_1, total_runs_scored_1]
  
if len(teams) >= 4:                                               
  away_box_score_total_2, home_box_score_total_2,away_pitcher_box_score_total_2, home_pitcher_box_score_total_2, home_win_odds_2, home_pythagwin_odds_2, away_runs_scored_2, home_runs_scored_2, total_runs_scored_2 = game_repeater(1000,2,teams[0][2],teams[0][3])
  game_summary.loc[1] = [teams[0][2], teams[0][3], home_win_odds_2, home_pythagwin_odds_2, away_runs_scored_2, home_runs_scored_2, total_runs_scored_2]
  
if len(teams) >= 6:                                               
  away_box_score_total_3, home_box_score_total_3,away_pitcher_box_score_total_3, home_pitcher_box_score_total_3, home_win_odds_3, home_pythagwin_odds_3, away_runs_scored_3, home_runs_scored_3, total_runs_scored_3 = game_repeater(1000,4,teams[0][4],teams[0][5])
  game_summary.loc[2] = [teams[0][4], teams[0][5], home_win_odds_3, home_pythagwin_odds_3, away_runs_scored_3, home_runs_scored_3, total_runs_scored_3]
  
if len(teams) >= 8:                                               
  away_box_score_total_4, home_box_score_total_4,away_pitcher_box_score_total_4, home_pitcher_box_score_total_4, home_win_odds_4, home_pythagwin_odds_4, away_runs_scored_4, home_runs_scored_4, total_runs_scored_4 = game_repeater(1000,6,teams[0][6],teams[0][7])
  game_summary.loc[3] = [teams[0][6], teams[0][7], home_win_odds_4, home_pythagwin_odds_4, away_runs_scored_4, home_runs_scored_4, total_runs_scored_4]
  
if len(teams) >= 10:                                               
  away_box_score_total_5, home_box_score_total_5,away_pitcher_box_score_total_5, home_pitcher_box_score_total_5, home_win_odds_5, home_pythagwin_odds_5, away_runs_scored_5, home_runs_scored_5, total_runs_scored_5 = game_repeater(1000,8,teams[0][8],teams[0][9])
  game_summary.loc[4] = [teams[0][8], teams[0][9], home_win_odds_5, home_pythagwin_odds_5, away_runs_scored_5, home_runs_scored_5, total_runs_scored_5]
  
if len(teams) >= 12:                                               
  away_box_score_total_6, home_box_score_total_6,away_pitcher_box_score_total_6, home_pitcher_box_score_total_6, home_win_odds_6, home_pythagwin_odds_6, away_runs_scored_6, home_runs_scored_6, total_runs_scored_6 = game_repeater(1000,10,teams[0][10],teams[0][11])
  game_summary.loc[5] = [teams[0][10], teams[0][11], home_win_odds_6, home_pythagwin_odds_6, away_runs_scored_6, home_runs_scored_6, total_runs_scored_6]
  
if len(teams) >= 14:                                               
  away_box_score_total_7, home_box_score_total_7,away_pitcher_box_score_total_7, home_pitcher_box_score_total_7, home_win_odds_7, home_pythagwin_odds_7, away_runs_scored_7, home_runs_scored_7, total_runs_scored_7 = game_repeater(1000,12,teams[0][12],teams[0][13])
  game_summary.loc[6] = [teams[0][12], teams[0][13], home_win_odds_7, home_pythagwin_odds_7, away_runs_scored_7, home_runs_scored_7, total_runs_scored_7]
  
if len(teams) >= 16:                                               
  away_box_score_total_8, home_box_score_total_8,away_pitcher_box_score_total_8, home_pitcher_box_score_total_8, home_win_odds_8, home_pythagwin_odds_8, away_runs_scored_8, home_runs_scored_8, total_runs_scored_8 = game_repeater(1000,14,teams[0][14],teams[0][15])
  game_summary.loc[7] = [teams[0][14], teams[0][15], home_win_odds_8, home_pythagwin_odds_8, away_runs_scored_8, home_runs_scored_1, total_runs_scored_8]
  
if len(teams) >= 18:                                               
  away_box_score_total_9, home_box_score_total_9,away_pitcher_box_score_total_9, home_pitcher_box_score_total_9, home_win_odds_9, home_pythagwin_odds_9, away_runs_scored_9, home_runs_scored_9, total_runs_scored_9 = game_repeater(1000,16,teams[0][16],teams[0][17])
  game_summary.loc[8] = [teams[0][16], teams[0][17], home_win_odds_9, home_pythagwin_odds_9, away_runs_scored_9, home_runs_scored_9, total_runs_scored_9]
  
if len(teams) >= 20:                                               
  away_box_score_total_10, home_box_score_total_10,away_pitcher_box_score_total_10, home_pitcher_box_score_total_10, home_win_odds_10, home_pythagwin_odds_10, away_runs_scored_10, home_runs_scored_10, total_runs_scored_10 = game_repeater(1000,18,teams[0][18],teams[0][19])
  game_summary.loc[9] = [teams[0][18], teams[0][19], home_win_odds_10, home_pythagwin_odds_10, away_runs_scored_10, home_runs_scored_10, total_runs_scored_10]
  
if len(teams) >= 22:                                               
  away_box_score_total_11, home_box_score_total_11,away_pitcher_box_score_total_11, home_pitcher_box_score_total_11, home_win_odds_11, home_pythagwin_odds_11, away_runs_scored_11, home_runs_scored_11, total_runs_scored_11 = game_repeater(1000,20,teams[0][20],teams[0][21])
  game_summary.loc[10] = [teams[0][21], teams[0][20], home_win_odds_11, home_pythagwin_odds_11, away_runs_scored_11, home_runs_scored_11, total_runs_scored_11]
  
if len(teams) >= 24:                                               
  away_box_score_total_12, home_box_score_total_12, away_pitcher_box_score_total_12, home_pitcher_box_score_total_12, home_win_odds_12, home_pythagwin_odds_12, away_runs_scored_12, home_runs_scored_12, total_runs_scored_12 = game_repeater(1000,22,teams[0][22],teams[0][23])
  game_summary.loc[11] = [teams[0][22], teams[0][23], home_win_odds_12, home_pythagwin_odds_12, away_runs_scored_12, home_runs_scored_12, total_runs_scored_12]
  
if len(teams) >= 26:                                               
  away_box_score_total_13, home_box_score_total_13, away_pitcher_box_score_total_13, home_pitcher_box_score_total_13, home_win_odds_13, home_pythagwin_odds_13, away_runs_scored_13, home_runs_scored_13, total_runs_scored_13 = game_repeater(1000,24,teams[0][24],teams[0][25])
  game_summary.loc[12] = [teams[0][24], teams[0][25], home_win_odds_13, home_pythagwin_odds_13, away_runs_scored_13, home_runs_scored_13, total_runs_scored_13]
  
if len(teams) >= 28:                                               
  away_box_score_total_14, home_box_score_total_14, away_pitcher_box_score_total_14, home_pitcher_box_score_total_14, home_win_odds_14, home_pythagwin_odds_14, away_runs_scored_14, home_runs_scored_14, total_runs_scored_14 = game_repeater(1000,26,teams[0][26],teams[0][27])
  game_summary.loc[13] = [teams[0][26], teams[0][27], home_win_odds_14, home_pythagwin_odds_14, away_runs_scored_14, home_runs_scored_14, total_runs_scored_14]
  
if len(teams) >= 30:                                               
  away_box_score_total_15, home_box_score_total_15, away_pitcher_box_score_total_15, home_pitcher_box_score_total_15, home_win_odds_15, home_pythagwin_odds_15, away_runs_scored_15, home_runs_scored_15, total_runs_scored_15 = game_repeater(1000,28,teams[0][28],teams[0][29])
  game_summary.loc[14] = [teams[0][28], teams[0][29], home_win_odds_15, home_pythagwin_odds_15, away_runs_scored_15, home_runs_scored_15, total_runs_scored_15]
  
if len(teams) >= 32:                                               
  away_box_score_total_16, home_box_score_total_16, away_pitcher_box_score_total_16, home_pitcher_box_score_total_16, home_win_odds_16, home_pythagwin_odds_16, away_runs_scored_16, home_runs_scored_16, total_runs_scored_16 = game_repeater(1000,30,teams[0][30],teams[0][31])
  game_summary.loc[15] = [teams[0][30], teams[0][31], home_win_odds_16, home_pythagwin_odds_16, away_runs_scored_16, home_runs_scored_16, total_runs_scored_16]
  
if len(teams) >= 34:                                               
  away_box_score_total_17, home_box_score_total_17, away_pitcher_box_score_total_17, home_pitcher_box_score_total_17, home_win_odds_17, home_pythagwin_odds_17, away_runs_scored_17, home_runs_scored_17, total_runs_scored_17 = game_repeater(1000,32,teams[0][32],teams[0][33])
  game_summary.loc[16] = [teams[0][32], teams[0][33], home_win_odds_17, home_pythagwin_odds_17, away_runs_scored_17, home_runs_scored_17, total_runs_scored_17]
  
if len(teams) >= 36:                                               
  away_box_score_total_18, home_box_score_total_18, away_pitcher_box_score_total_18, home_pitcher_box_score_total_18, home_win_odds_18, home_pythagwin_odds_18, away_runs_scored_18, home_runs_scored_18, total_runs_scored_18 = game_repeater(1000,34,teams[0][34],teams[0][35])
  game_summary.loc[17] = [teams[0][34], teams[0][35], home_win_odds_18, home_pythagwin_odds_18, away_runs_scored_18, home_runs_scored_18, total_runs_scored_18]
  
if len(teams) >= 38:                                               
  away_box_score_total_19, home_box_score_total_19, away_pitcher_box_score_total_19, home_pitcher_box_score_total_19, home_win_odds_19, home_pythagwin_odds_19, away_runs_scored_19, home_runs_scored_19, total_runs_scored_19 = game_repeater(1000,36,teams[0][36],teams[0][37])
  game_summary.loc[18] = [teams[0][36], teams[0][37], home_win_odds_19, home_pythagwin_odds_19, away_runs_scored_19, home_runs_scored_19, total_runs_scored_19]
  
if len(teams) >= 40:                                               
  away_box_score_total_20, home_box_score_total_20, away_pitcher_box_score_total_20, home_pitcher_box_score_total_20, home_win_odds_20, home_pythagwin_odds_20, away_runs_scored_20, home_runs_scored_20, total_runs_scored_20 = game_repeater(1000,38,teams[0][38],teams[0][39])
  game_summary.loc[19] = [teams[0][38], teams[0][39], home_win_odds_20, home_pythagwin_odds_20, away_runs_scored_20, home_runs_scored_20, total_runs_scored_20]

  
stop = timeit.default_timer()

print('Sim Time:' + stop - start)

