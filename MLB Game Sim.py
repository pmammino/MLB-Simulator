import pandas as pd
import time
import random

lineup = pd.read_csv("MLB Lineup Sim Tool.csv")
away_team = "DET"
home_team = "PIT"
away_lineup = {1: {'id': lineup.iloc[0, 0], 'x1b': lineup.iloc[0, 1], 'x2b': lineup.iloc[0, 2], 'x3b': lineup.iloc[0, 3], 'xhr': lineup.iloc[0, 4], 'xk': lineup.iloc[0, 5], 'xbb': lineup.iloc[0, 6], 'xout': lineup.iloc[0, 7]},
               2: {'id': lineup.iloc[1, 0], 'x1b': lineup.iloc[1, 1], 'x2b': lineup.iloc[1, 2], 'x3b': lineup.iloc[1, 3], 'xhr': lineup.iloc[1, 4], 'xk': lineup.iloc[1, 5], 'xbb': lineup.iloc[1, 6], 'xout': lineup.iloc[1, 7]},
               3: {'id': lineup.iloc[2, 0], 'x1b': lineup.iloc[2, 1], 'x2b': lineup.iloc[2, 2], 'x3b': lineup.iloc[2, 3], 'xhr': lineup.iloc[2, 4], 'xk': lineup.iloc[2, 5], 'xbb': lineup.iloc[2, 6], 'xout': lineup.iloc[2, 7]},
               4: {'id': lineup.iloc[3, 0], 'x1b': lineup.iloc[3, 1], 'x2b': lineup.iloc[3, 2], 'x3b': lineup.iloc[3, 3], 'xhr': lineup.iloc[3, 4], 'xk': lineup.iloc[3, 5], 'xbb': lineup.iloc[3, 6], 'xout': lineup.iloc[3, 7]},
               5: {'id': lineup.iloc[4, 0], 'x1b': lineup.iloc[4, 1], 'x2b': lineup.iloc[4, 2], 'x3b': lineup.iloc[4, 3], 'xhr': lineup.iloc[4, 4], 'xk': lineup.iloc[4, 5], 'xbb': lineup.iloc[4, 6], 'xout': lineup.iloc[4, 7]},
               6: {'id': lineup.iloc[5, 0], 'x1b': lineup.iloc[5, 1], 'x2b': lineup.iloc[5, 2], 'x3b': lineup.iloc[5, 3], 'xhr': lineup.iloc[5, 4], 'xk': lineup.iloc[5, 5], 'xbb': lineup.iloc[5, 6], 'xout': lineup.iloc[5, 7]},
               7: {'id': lineup.iloc[6, 0], 'x1b': lineup.iloc[6, 1], 'x2b': lineup.iloc[6, 2], 'x3b': lineup.iloc[6, 3], 'xhr': lineup.iloc[6, 4], 'xk': lineup.iloc[6, 5], 'xbb': lineup.iloc[6, 6], 'xout': lineup.iloc[6, 7]},
               8: {'id': lineup.iloc[7, 0], 'x1b': lineup.iloc[7, 1], 'x2b': lineup.iloc[7, 2], 'x3b': lineup.iloc[7, 3], 'xhr': lineup.iloc[7, 4], 'xk': lineup.iloc[7, 5], 'xbb': lineup.iloc[7, 6], 'xout': lineup.iloc[7, 7]},
               9: {'id': lineup.iloc[8, 0], 'x1b': lineup.iloc[8, 1], 'x2b': lineup.iloc[8, 2], 'x3b': lineup.iloc[8, 3], 'xhr': lineup.iloc[8, 4], 'xk': lineup.iloc[8, 5], 'xbb': lineup.iloc[8, 6], 'xout': lineup.iloc[8, 7]}
}
home_lineup = {1: {'id': lineup.iloc[10, 0], 'x1b': lineup.iloc[10, 1], 'x2b': lineup.iloc[10, 2], 'x3b': lineup.iloc[10, 3], 'xhr': lineup.iloc[10, 4], 'xk': lineup.iloc[10, 5], 'xbb': lineup.iloc[10, 6], 'xout': lineup.iloc[10, 7]},
               2: {'id': lineup.iloc[11, 0], 'x1b': lineup.iloc[11, 1], 'x2b': lineup.iloc[11, 2], 'x3b': lineup.iloc[11, 3], 'xhr': lineup.iloc[11, 4], 'xk': lineup.iloc[11, 5], 'xbb': lineup.iloc[11, 6], 'xout': lineup.iloc[11, 7]},
               3: {'id': lineup.iloc[12, 0], 'x1b': lineup.iloc[12, 1], 'x2b': lineup.iloc[12, 2], 'x3b': lineup.iloc[12, 3], 'xhr': lineup.iloc[12, 4], 'xk': lineup.iloc[12, 5], 'xbb': lineup.iloc[12, 6], 'xout': lineup.iloc[12, 7]},
               4: {'id': lineup.iloc[13, 0], 'x1b': lineup.iloc[13, 1], 'x2b': lineup.iloc[13, 2], 'x3b': lineup.iloc[13, 3], 'xhr': lineup.iloc[13, 4], 'xk': lineup.iloc[13, 5], 'xbb': lineup.iloc[13, 6], 'xout': lineup.iloc[13, 7]},
               5: {'id': lineup.iloc[14, 0], 'x1b': lineup.iloc[14, 1], 'x2b': lineup.iloc[14, 2], 'x3b': lineup.iloc[14, 3], 'xhr': lineup.iloc[14, 4], 'xk': lineup.iloc[14, 5], 'xbb': lineup.iloc[14, 6], 'xout': lineup.iloc[14, 7]},
               6: {'id': lineup.iloc[15, 0], 'x1b': lineup.iloc[15, 1], 'x2b': lineup.iloc[15, 2], 'x3b': lineup.iloc[15, 3], 'xhr': lineup.iloc[15, 4], 'xk': lineup.iloc[15, 5], 'xbb': lineup.iloc[15, 6], 'xout': lineup.iloc[15, 7]},
               7: {'id': lineup.iloc[16, 0], 'x1b': lineup.iloc[16, 1], 'x2b': lineup.iloc[16, 2], 'x3b': lineup.iloc[16, 3], 'xhr': lineup.iloc[16, 4], 'xk': lineup.iloc[16, 5], 'xbb': lineup.iloc[16, 6], 'xout': lineup.iloc[16, 7]},
               8: {'id': lineup.iloc[17, 0], 'x1b': lineup.iloc[17, 1], 'x2b': lineup.iloc[17, 2], 'x3b': lineup.iloc[17, 3], 'xhr': lineup.iloc[17, 4], 'xk': lineup.iloc[17, 5], 'xbb': lineup.iloc[17, 6], 'xout': lineup.iloc[17, 7]},
               9: {'id': lineup.iloc[18, 0], 'x1b': lineup.iloc[18, 1], 'x2b': lineup.iloc[18, 2], 'x3b': lineup.iloc[18, 3], 'xhr': lineup.iloc[18, 4], 'xk': lineup.iloc[18, 5], 'xbb': lineup.iloc[18, 6], 'xout': lineup.iloc[18, 7]}
}
### league averages 2019 only
league_1B = 11299 / 81633
league_2B = 3676 / 81633
league_3B = 330 / 81633
league_HR = 2888 / 81633
league_BB = 7438 / 81633
league_K = 18610 / 81633
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

sac_fly = 1175 / 1235
sac_fly_no = 1 - sac_fly
sac_fly_results = ["score", "nothing"]
sac_fly_probs = [sac_fly, sac_fly_no]
  

# setting up game sim
away_outs = 0
home_outs = 0
first = 0
second = 0
third = 0
home = 0

away_runs = 0
away_runs_previous = 0
runs = 0
runs_previous = 0
home_runs = 0
away_order = 1
home_order = 1

away_wins = 0
home_wins = 0
ties = 0



innings = 5
num_sims = 100000
x = random.randint(0,100000)
y = (innings * 3) * num_sims

# half inning which calculates runs and interates until there are 3 outs
# half inning which calculates runs and interates until there are 3 outs
start_time = time.time()

while away_outs < y or home_outs < y:
      
    if away_outs < y:
        
        if x <= away_lineup[away_order]['xout']:
            away_outs = away_outs + 1
            x = random.randint(0,100000)
            if away_outs % 3 == 0:
                first = 0
                second = 0
                third = 0
            if away_outs % (innings * 3) == 0:
                away_order = 1
                
                away_runs_game = away_runs - away_runs_previous
                away_runs_previous = away_runs
       
        elif x > away_lineup[away_order]['xout'] and x < away_lineup[away_order]['xbb']:
            if first == 0 and second == 0 and third == 0:
                first = 1
            elif first == 0 and third == 0 and second == 1:
                first = 1
            elif first == 0 and second == 0 and third == 1:
                first = 1
            elif second == 0 and third == 0 and first == 1:
                second = 1
            elif second == 1 and third == 1 and first == 0:
                first = 1
            elif first == 1 and third == 1 and second == 0:
                second = 1
            elif first == 1 and second == 1 and third == 0:
                third = 1
            else:
                away_runs = away_runs + 1
            x = random.randint(0,100000)
        elif x > away_lineup[away_order]['xbb'] and x < away_lineup[away_order]['x1b']:
            if first == 0  and second == 0 and third == 0:
                first = 1
            elif first == 0 and third == 0 and second == 1:
                first = 1
                second = 0
                away_runs = away_runs + 1
            elif first == 0 and second == 0 and third == 1:
                first = 1
                third = 0
                away_runs = away_runs + 1
            elif second == 0 and third == 0 and first == 1:
                second = 1
            elif second == 1 and third == 1 and first == 0:
                first = 1
                second = 0
                third = 0
                away_runs = away_runs + 2
            elif first == 1 and third == 1 and second == 0:
                second = 1
                third = 0
                away_runs = away_runs + 1
            elif first == 1 and second == 1 and third == 0:
                away_runs = away_runs + 1
            else:
                third = 0
                away_runs = away_runs + 2
            x = random.randint(0,100000)
        elif x > away_lineup[away_order]['x1b'] and x < away_lineup[away_order]['x2b']: 
            if first == 0 and second == 0 and third == 0:
                second = 1
            elif first == 0 and third == 0 and second == 1:
                away_runs = away_runs + 1
            elif first == 0 and second == 0 and third == 1:
                second = 1
                third = 0
                away_runs = away_runs + 1
            elif second == 0 and third == 0 and first == 1:
                first = 0
                second = 1
                third = 1
            elif second == 1 and third == 1 and first == 0:
                third = 0
                away_runs = away_runs + 2
            elif first == 1 and third == 1 and second == 0:
                first = 0
                second = 1
                away_runs = away_runs + 1
            elif first == 1 and second == 1 and third == 0:
                first = 0
                third = 1
                away_runs = away_runs + 1
            elif first == 1 and second == 1 and third == 1:
                first = 0
                away_runs = away_runs + 2
            x = random.randint(0,100000)
        elif x > away_lineup[away_order]['x2b'] and x < away_lineup[away_order]['x3b']: 
            if first == 0 and second and third == 0:
                third = 1
            elif first == 0 and third == 0 and second == 1:
                second = 0
                third = 1
                away_runs = away_runs + 1
            elif first == 0 and second == 0 and third == 1:
                away_runs = away_runs + 1
            elif second == 0 and third == 0 and first == 1:
                first = 0
                third = 1
                away_runs = away_runs + 1
            elif second == 1 and third == 1 and first == 0:
                second = 0  
                away_runs = away_runs + 2
            elif first == 1 and third == 1 and second == 0:
                first = 0
                away_runs = away_runs + 2
            elif first == 1 and second == 1 and third == 0:
                third = 1
                second = 0
                first = 0
                away_runs = away_runs + 2
            else:
                first = 0
                second = 0
                away_runs = away_runs + 3
            x = random.randint(0,100000)            
        else:
            if first == 0 and second == 0 and third == 0:
                away_runs = away_runs + 1
            elif first == 0 and third == 0 and second == 1:
                second = 0
                away_runs = away_runs + 2
            elif first == 0 and second == 0 and third == 1:
                third = 0
                away_runs = away_runs + 2
            elif second == 0 and third == 0 and first == 1:
                first = 0
                away_runs = away_runs + 2
            elif second == 1 and third == 1 and first == 0:
                second = 0
                third = 0
                away_runs = away_runs + 3
            elif first == 1 and third == 1 and second == 0:
                first = 0
                third = 0
                away_runs = away_runs + 3
            elif first == 1 and second == 1 and third == 0:
                first = 0
                second = 0
                away_runs = away_runs + 3
            else:
                first = 0
                second = 0
                third = 0
                away_runs = away_runs + 4
        x = random.randint(0,100000)
        away_order = away_order + 1
        if away_order == 10:
            away_order = 1
      
    if home_outs < y:
         
        if x <= home_lineup[home_order]['xout']:
            home_outs = home_outs + 1
            x = random.randint(0,100000)
            if home_outs % 3 == 0:
                first = 0
                second = 0
                third = 0
            if home_outs % (innings * 3) == 0:
                home_order = 1
                
                runs_game = runs - runs_previous
                runs_previous = runs
       
        elif x > home_lineup[home_order]['xout'] and x < home_lineup[home_order]['xbb']:
            if first == 0 and second == 0 and third == 0:
                first = 1
            elif first == 0 and third == 0 and second == 1:
                first = 1
            elif first == 0 and second == 0 and third == 1:
                first = 1
            elif second == 0 and third == 0 and first == 1:
                second = 1
            elif second == 1 and third == 1 and first == 0:
                first = 1
            elif first == 1 and third == 1 and second == 0:
                second = 1
            elif first == 1 and second == 1 and third == 0:
                third = 1
            else:
                runs = runs + 1
            x = random.randint(0,100000)
        elif x > home_lineup[home_order]['xbb'] and x < home_lineup[home_order]['x1b']:
            if first == 0  and second == 0 and third == 0:
                first = 1
            elif first == 0 and third == 0 and second == 1:
                first = 1
                second = 0
                runs = runs + 1
            elif first == 0 and second == 0 and third == 1:
                first = 1
                third = 0
                runs = runs + 1
            elif second == 0 and third == 0 and first == 1:
                second = 1
            elif second == 1 and third == 1 and first == 0:
                first = 1
                second = 0
                third = 0
                runs = runs + 2
            elif first == 1 and third == 1 and second == 0:
                second = 1
                third = 0
                runs = runs + 1
            elif first == 1 and second == 1 and third == 0:
                runs = runs + 1
            else:
                third = 0
                runs = runs + 2
            x = random.randint(0,100000)
        elif x > home_lineup[home_order]['x1b'] and x < home_lineup[home_order]['x2b']: 
            if first == 0 and second == 0 and third == 0:
                second = 1
            elif first == 0 and third == 0 and second == 1:
                runs = runs + 1
            elif first == 0 and second == 0 and third == 1:
                second = 1
                third = 0
                runs = runs + 1
            elif second == 0 and third == 0 and first == 1:
                first = 0
                second = 1
                third = 1
            elif second == 1 and third == 1 and first == 0:
                third = 0
                runs = runs + 2
            elif first == 1 and third == 1 and second == 0:
                first = 0
                second = 1
                runs = runs + 1
            elif first == 1 and second == 1 and third == 0:
                first = 0
                third = 1
                runs = runs + 1
            elif first == 1 and second == 1 and third == 1:
                first = 0
                runs = runs + 2
            x = random.randint(0,100000)
        elif x > home_lineup[home_order]['x2b'] and x < home_lineup[home_order]['x3b']: 
            if first == 0 and second and third == 0:
                third = 1
            elif first == 0 and third == 0 and second == 1:
                second = 0
                third = 1
                runs = runs + 1
            elif first == 0 and second == 0 and third == 1:
                runs = runs + 1
            elif second == 0 and third == 0 and first == 1:
                first = 0
                third = 1
                runs = runs + 1
            elif second == 1 and third == 1 and first == 0:
                second = 0  
                runs = runs + 2
            elif first == 1 and third == 1 and second == 0:
                first = 0
                runs = runs + 2
            elif first == 1 and second == 1 and third == 0:
                third = 1
                second = 0
                first = 0
                runs = runs + 2
            else:
                first = 0
                second = 0
                runs = runs + 3
            x = random.randint(0,100000)            
        else:
            if first == 0 and second == 0 and third == 0:
                runs = runs + 1
            elif first == 0 and third == 0 and second == 1:
                second = 0
                runs = runs + 2
            elif first == 0 and second == 0 and third == 1:
                third = 0
                runs = runs + 2
            elif second == 0 and third == 0 and first == 1:
                first = 0
                runs = runs + 2
            elif second == 1 and third == 1 and first == 0:
                second = 0
                third = 0
                runs = runs + 3
            elif first == 1 and third == 1 and second == 0:
                first = 0
                third = 0
                runs = runs + 3
            elif first == 1 and second == 1 and third == 0:
                first = 0
                second = 0
                runs = runs + 3
            else:
                first = 0
                second = 0
                third = 0
                runs = runs + 4
        home_runs = runs
        x = random.randint(0,100000)
        home_order = home_order + 1
        if home_order == 10:
            home_order = 1
        
        if away_outs % (innings * 3) == 0 and home_outs % (innings * 3) == 0:
            if runs_game > away_runs_game:
                home_wins = home_wins + 1
            if runs_game < away_runs_game:
                away_wins = away_wins + 1
            else:
                ties = ties + 1
            

hfa = .153
away_rpg = round((away_runs / num_sims) - (hfa / 2), 4)
home_rpg = round((home_runs / num_sims) + (hfa / 2), 4)
total_rpg = round((away_runs + home_runs) / num_sims, 4)
away_win = round(away_rpg ** 1.83 / ((away_rpg ** 1.83) + (home_rpg ** 1.83)), 4)
home_win = round(1 - away_win, 4)
away_win_count = away_wins
home_win_count = home_wins

if away_win > .5:
    away_ml = round(away_win / (1 - away_win) * -100, 0)
else:
    away_ml = round((1 - away_win) / away_win * 100, 0)

if home_win > .5:
    home_ml = round(home_win / (1 - home_win) * -100, 0)
else:
    home_ml = round((1 - home_win) / home_win * 100, 0)

if innings == 9:
    print("Full game results...")
if innings == 5:
    print("First five results...")
else:
    print("First inning results...")
        
if away_outs or home_outs == y:
    print(str(away_team) + ' - ' + str(away_win) + ' % / ' + str(away_ml) + ' / ' + str(away_rpg) + ' runs')
    
if away_outs or home_outs == y:
    print(str(home_team) + ' - ' + str(home_win) + ' % / ' + str(home_ml) + ' / ' + str(home_rpg) + ' runs')
    print('Total - ' + str(total_rpg))

clock = (time.time() - start_time)

if clock >= 60:
    print("The simulation took " + str(round(clock / 60, 4)) + " minutes to complete.")
else:
    print("The " + str(num_sims) + " simulations took " + str(round(clock, 4)) + " seconds to complete.")

