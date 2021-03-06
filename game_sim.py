### league averages 2018 only
league_1B = 26322 / 185139
league_2B = 8264 / 185139
league_3B = 847 / 185139
league_HR = 5585 / 185139
league_BB = 15686 / 185139
league_K = 41207 / 185139
league_BO = 1 - league_1B - league_2B - league_3B - league_HR - league_BB - league_K

### baserunning data
single_1Bto2B = 157 / 245
single_1Bto3B = 84 / 245
single_1BtoOUT = 1 - single_1Bto2B - single_1Bto3B
single1B_results = ["second_base", "third_base", "out"]
single1B_probs = [single_1Bto2B, single_1Bto3B, single_1BtoOUT]


double_1Bto3B = 35 / 69
double_1BtoH = 33 / 69
double_1BtoOUT = 1 - double_1Bto3B - double_1BtoH
double1B_results = ["third_base", "score", "out"]
double1B_probs = [double_1Bto3B, double_1BtoH, double_1BtoOUT]

single_2Bto3B = 44 / 130
single_2BtoH = 81 / 130
single_2BtoOUT = 1 - single_2Bto3B - single_2BtoH
single2B_results = ["third_base", "score", "out"]
single2B_probs = [single_2Bto3B, single_2BtoH, single_2BtoOUT]






def game_sim(away_team, home_team, away_lineup, home_lineup, away_pitcher, home_pitcher):
    inning = 1
    half = 'top'
    away_batter = 0
    home_batter = 0
    away_runs = 0
    home_runs = 0
    
    while (inning < 2):
      if (half == 'top'):
        outs = 0
        first_base = ''
        second_base = ''
        third_base = ''
        while (outs < 3):
          pa_result = at_bat(home_pitcher, pd.DataFrame(away_lineup.iloc[away_batter]).T.reset_index(drop = True))
          
          if(pa_result == 'k'):
            outs = outs + 1
            
          if(pa_result == 'bo'):
            outs = outs + 1
            
          if(pa_result == 'bb'):
            runs_before = away_runs                                  
            if (third_base != '' and second_base != '' and first_base != ''):
              away_runs = away_runs + 1
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

          if(pa_result == '1b'):
            runs_before = away_runs
            if (third_base != ''):
              away_runs = away_runs + 1
              third_base = ''
            if (second_base != ''):
                if (np.random.choice(single2B_results, 1, p = single2B_probs) == "third_base"):
                    third_base = second_base
                    second_base = ''
                if (np.random.choice(single2B_results, 1, p = single2B_probs) == "score"):
                    away_runs = away_runs + 1
                    second_base = ''
                else:
                    outs = outs + 1
                    second_base = ''
            if (first_base != ''):
                if (np.random.choice(single1B_results, 1, p = single1B_probs) == "second_base"):
                    second_base = first_base
                    first_base = ''
                if (np.random.choise(single1B_results, 1, p = single1B_probs) == "third_base"):
                    third_base = first_base
                    first_base = ''
                else:
                    outs = outs + 1
                    first_base = ''
            first_base = away_lineup.at[away_batter,"name"]
            runs_diff = away_runs - runs_before
                           
          if(pa_result == '2b'):
            runs_before = away_runs
            if (third_base != ''):
              away_runs = away_runs + 1
              third_base = ''
            if (second_base != ''):
              away_runs = away_runs + 1
              second_base = ''
            if (first_base != ''):
              if (np.random.choice(double1B_results, 1, p = double1B_probs) == "third_base"):
                  third_base = first_base
              if (np.random.choice(double1B_results, 1, p = double1B_probs) == "score"):
                  away_runs = away_runs + 1
                  first_base = ''
              else:
                  outs = outs + 1
                  first_base = ''
            second_base = away_lineup.at[away_batter,"name"]
            runs_diff = away_runs - runs_before

          if(pa_result == '3b'):
            runs_before = away_runs
            if (third_base != ''):
              away_runs = away_runs + 1
              third_base = ''
            if (second_base != ''):
              away_runs = away_runs + 1
              second_base = ''
            if (first_base != ''):
              away_runs = away_runs + 1
              first_base = ''
            third_base = away_lineup.at[away_batter,"name"]
            runs_diff = away_runs - runs_before
            
          if(pa_result == 'hr'):
            runs_before = away_runs
            if (third_base != ''):
              away_runs = away_runs + 1
              third_base = ''
            if (second_base != ''):
              away_runs = away_runs + 1
              second_base = ''
            if (first_base != ''):
              away_runs = away_runs + 1
              first_base = ''
            away_runs = away_runs + 1
            runs_diff = away_runs - runs_before
          
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
          pa_result = at_bat(home_pitcher, pd.DataFrame(away_lineup.iloc[away_batter]).T.reset_index(drop = True))
          
          if(pa_result == 'k'):
            outs = outs + 1
            
          if(pa_result == 'bo'):
            outs = outs + 1
          
          if(pa_result == 'bb'):
            runs_before = home_runs                                  
            if (third_base != '' and second_base != '' and first_base != ''):
              home_runs = home_runs + 1
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
            
          if(pa_result == '1b'):
            runs_before = home_runs
            if (third_base != ''):
              home_runs = home_runs + 1
              third_base = ''
            if (second_base != ''):
              if (np.random.choice(single2B_results, 1, p = single2B_probs) == "third_base"):
                    third_base = second_base
                    second_base = ''
              if (np.random.choice(single2B_results, 1, p = single2B_probs) == "score"):
                    home_runs = home_runs + 1
                    second_base = ''
              else:
                    outs = outs + 1
                    second_base = ''
            if (first_base != ''):
              if (np.random.choice(single1B_results, 1, p = single1B_probs) == "second_base"):
                    second_base = first_base
                    first_base = ''
              if (np.random.choise(single1B_results, 1, p = single1B_probs) == "third_base"):
                    third_base = first_base
                    first_base = ''
              else:
                    outs = outs + 1
                    first_base = ''
            first_base = home_lineup.at[home_batter,"name"]
            runs_diff = home_runs - runs_before
            
          if(pa_result == '2b'):
            runs_before = home_runs
            if (third_base != ''):
              home_runs = home_runs + 1
              third_base = ''
            if (second_base != ''):
              home_runs = home_runs + 1
              second_base = ''
            if (first_base != ''):
                if (np.random.choice(double1B_results, 1, p = double1B_probs) == "third_base"):
                  third_base = first_base
                if (np.random.choice(double1B_results, 1, p = double1B_probs) == "score"):
                  away_runs = away_runs + 1
                  first_base = ''
                else:
                  outs = outs + 1
                  first_base = ''
            second_base = home_lineup.at[home_batter,"name"]
            runs_diff = home_runs - runs_before
            
          if(pa_result == '3b'):
            runs_before = home_runs
            if (third_base != ''):
              home_runs = home_runs + 1
              third_base = ''
            if (second_base != ''):
              home_runs = home_runs + 1
              second_base = ''
            if (first_base != ''):
              home_runs = home_runs + 1
              first_base = ''
            third_base = home_lineup.at[home_batter,"name"]
            runs_diff = home_runs - runs_before
            
          if(pa_result == 'hr'):
            runs_before = home_runs
            if (third_base != ''):
              home_runs = home_runs + 1
              third_base = ''
            if (second_base != ''):
              home_runs = home_runs + 1
              second_base = ''
            if (first_base != ''):
              home_runs = home_runs + 1
              first_base = ''
            home_runs = home_runs + 1
            runs_diff = home_runs - runs_before

          if (home_batter == 8):
            home_batter = 0
          else:
            home_batter = home_batter + 1
        half = 'top'
        inning = inning + 1
    
    return(??????)    
