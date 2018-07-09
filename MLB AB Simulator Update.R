# mockaustin last updated 7/9/18 by paul
# mlb full game sim

library(rvest)
library(plyr)
library(tidyr)
library(data.table)
library(tm)

time_start <- proc.time()

## pull lineups from rotworld

starter_scraper <- function(num){
  url <- "http://www.rotoworld.com/mlb/dailyLineups"
  starters <- url %>%
    read_html() %>%
    html_nodes(xpath= paste('//*[@id="cp1_lineups"]/div[',num,']/table[1]')) %>%
    html_table()
  starters <- starters[[1]]
  starters <- starters[2,c(2,5)]
  starters <- separate(data = starters, col = X2, into = c("Name.A", "Handedness.A"),sep = "\\(")
  starters <- separate(data = starters, col = Handedness.A, into = c("Handedness.A", "Salary.A"),sep = "\\)")
  starters <- separate(data = starters, col = X5, into = c("Name.H", "Handedness.H"),sep = "\\(")
  starters <- separate(data = starters, col = Handedness.H, into = c("Handedness.H", "Salary.H"),sep = "\\)")
  return(starters)
}

away_scraper <- function(num){
  url <- "http://www.rotoworld.com/mlb/dailyLineups"
  away_lineup <- url %>%
    read_html() %>%
    html_nodes(xpath= paste('//*[@id="cp1_lineups"]/div[',num,']/table[2]')) %>%
    html_table()
  away_lineup <- away_lineup[[1]]
  away_lineup <- away_lineup <- away_lineup[,c(3,4,5,6,7)]
  return(away_lineup)
}

home_scraper <- function(num){
  url <- "http://www.rotoworld.com/mlb/dailyLineups"
  home_lineup <- url %>%
    read_html() %>%
    html_nodes(xpath= paste('//*[@id="cp1_lineups"]/div[',num,']/table[3]')) %>%
    html_table()
  home_lineup <- home_lineup[[1]]
  home_lineup <- home_lineup <- home_lineup[,c(3,4,5,6,7)]
  return(home_lineup)
}

away_team <- function(game)
{
starters <- starter_scraper(game)
home_lineup <- home_scraper(game) 
away_lineup <- away_scraper(game)

# scrape steamer projection files

batter_steamer <- read.csv("steamer_batter_2018.csv")
pitcher_steamer <- read.csv("steamer_pitcher_2018.csv")

# read today's mlb lineups

df <- read.csv("MLB Lineups Today.csv")

# pulling away leadoff batter and home starting pitcher


at_bat <- function(batter)
{
away_batter <- data.frame(away_lineup[batter,1], stringsAsFactors = FALSE)
colnames(away_batter) <- "player"
home_pitcher <- data.frame(starters[1,4], stringsAsFactors = FALSE)
home_pitcher <- data.frame(lapply(home_pitcher, trimws), stringsAsFactors = FALSE)
colnames(home_pitcher) <- "player"

# parsing data frame for home pitcher with all play outcomes by split

Throws <- rep(NA, 1)

home_pitcher <- data.frame(home_pitcher, Throws)
home_pitcher$Throws <- pitcher_steamer$Throws[match(home_pitcher$player, pitcher_steamer$name)]

mlbamid <- rep(NA, 1)

home_pitcher <- data.frame(home_pitcher, mlbamid)
home_pitcher$mlbamid <- pitcher_steamer$mlbamid[match(home_pitcher$player, pitcher_steamer$name)]


home_pitcher$vLcode <- paste("SP", "1", "vL", home_pitcher$mlbamid, sep= "-")
home_pitcher$vRcode <- paste("SP", "1", "vR", home_pitcher$mlbamid, sep= "-")

vL1B <- rep(NA, 1)

home_pitcher <- data.frame(home_pitcher, vL1B)
home_pitcher$vL1B <- pitcher_steamer$Single[match(home_pitcher$vLcode, pitcher_steamer$m_id)]

vL2B <- rep(NA, 1)

home_pitcher <- data.frame(home_pitcher, vL2B)
home_pitcher$vL2B <- pitcher_steamer$Double[match(home_pitcher$vLcode, pitcher_steamer$m_id)]

vL3B <- rep(NA, 1)

home_pitcher <- data.frame(home_pitcher, vL3B)
home_pitcher$vL3B <- pitcher_steamer$Triple[match(home_pitcher$vLcode, pitcher_steamer$m_id)]


vLHR <- rep(NA, 1)

home_pitcher <- data.frame(home_pitcher, vLHR)
home_pitcher$vLHR <- pitcher_steamer$HR[match(home_pitcher$vLcode, pitcher_steamer$m_id)]

vLBB <- rep(NA, 1)

home_pitcher <- data.frame(home_pitcher, vLBB)
home_pitcher$vLBB <- pitcher_steamer$BB[match(home_pitcher$vLcode, pitcher_steamer$m_id)]

vLSO <- rep(NA, 1)

home_pitcher <- data.frame(home_pitcher, vLSO)
home_pitcher$vLSO <- pitcher_steamer$K[match(home_pitcher$vLcode, pitcher_steamer$m_id)]

vLBO <- rep(NA, 1)

home_pitcher <- data.frame(home_pitcher, vLBO)
home_pitcher$vLBO <- pitcher_steamer$BO[match(home_pitcher$vLcode, pitcher_steamer$m_id)]

vR1B <- rep(NA, 1)

home_pitcher <- data.frame(home_pitcher, vR1B)
home_pitcher$vR1B <- pitcher_steamer$Single[match(home_pitcher$vRcode, pitcher_steamer$m_id)]

vR2B <- rep(NA, 1)

home_pitcher <- data.frame(home_pitcher, vR2B)
home_pitcher$vR2B <- pitcher_steamer$Double[match(home_pitcher$vRcode, pitcher_steamer$m_id)]

vR3B <- rep(NA, 1)

home_pitcher <- data.frame(home_pitcher, vR3B)
home_pitcher$vR3B <- pitcher_steamer$Triple[match(home_pitcher$vRcode, pitcher_steamer$m_id)]


vRHR <- rep(NA, 1)

home_pitcher <- data.frame(home_pitcher, vRHR)
home_pitcher$vRHR <- pitcher_steamer$HR[match(home_pitcher$vRcode, pitcher_steamer$m_id)]

vRBB <- rep(NA, 1)

home_pitcher <- data.frame(home_pitcher, vRBB)
home_pitcher$vRBB <- pitcher_steamer$BB[match(home_pitcher$vRcode, pitcher_steamer$m_id)]

vRSO <- rep(NA, 1)

home_pitcher <- data.frame(home_pitcher, vRSO)
home_pitcher$vRSO <- pitcher_steamer$K[match(home_pitcher$vRcode, pitcher_steamer$m_id)]

vRBO <- rep(NA, 1)

home_pitcher <- data.frame(home_pitcher, vRBO)
home_pitcher$vRBO <- pitcher_steamer$BO[match(home_pitcher$vRcode, pitcher_steamer$m_id)]

# done parsing pitcher play outcomes by split

# parsing data frame for away batter with all play outcomes by split

bats <- rep(NA, 1)

away_batter <- data.frame(away_batter, bats)
away_batter$bats <- batter_steamer$bats[match(away_batter$player, batter_steamer$name)]


mlbamid <- rep(NA, 1)
away_batter <- data.frame(away_batter, mlbamid)
away_batter$mlbamid <- batter_steamer$mlbamid[match(away_batter$player, batter_steamer$name)]

away_batter$vLcode <- paste("1", "vL", away_batter$mlbamid, sep= "-")
away_batter$vRcode <- paste("1", "vR", away_batter$mlbamid, sep= "-")

vL1B <- rep(NA, 1)

away_batter <- data.frame(away_batter, vL1B)
away_batter$vL1B <- batter_steamer$Single[match(away_batter$vLcode, batter_steamer$m_id)]

vL2B <- rep(NA, 1)

away_batter <- data.frame(away_batter, vL2B)
away_batter$vL2B <- batter_steamer$Double[match(away_batter$vLcode, batter_steamer$m_id)]

vL3B <- rep(NA, 1)

away_batter <- data.frame(away_batter, vL3B)
away_batter$vL3B <- batter_steamer$Triple[match(away_batter$vLcode, batter_steamer$m_id)]


vLHR <- rep(NA, 1)

away_batter <- data.frame(away_batter, vLHR)
away_batter$vLHR <- batter_steamer$HR[match(away_batter$vLcode, batter_steamer$m_id)]

vLBB <- rep(NA, 1)

away_batter <- data.frame(away_batter, vLBB)
away_batter$vLBB <- batter_steamer$BB[match(away_batter$vLcode, batter_steamer$m_id)]

vLSO <- rep(NA, 1)

away_batter <- data.frame(away_batter, vLSO)
away_batter$vLSO <- batter_steamer$K[match(away_batter$vLcode, batter_steamer$m_id)]

vLBO <- rep(NA, 1)

away_batter <- data.frame(away_batter, vLBO)
away_batter$vLBO <- batter_steamer$BO[match(away_batter$vLcode, batter_steamer$m_id)]

vR1B <- rep(NA, 1)

away_batter <- data.frame(away_batter, vR1B)
away_batter$vR1B <- batter_steamer$Single[match(away_batter$vRcode, batter_steamer$m_id)]

vR2B <- rep(NA, 1)

away_batter <- data.frame(away_batter, vR2B)
away_batter$vR2B <- batter_steamer$Double[match(away_batter$vRcode, batter_steamer$m_id)]

vR3B <- rep(NA, 1)

away_batter <- data.frame(away_batter, vR3B)
away_batter$vR3B <- batter_steamer$Triple[match(away_batter$vRcode, batter_steamer$m_id)]


vRHR <- rep(NA, 1)

away_batter <- data.frame(away_batter, vRHR)
away_batter$vRHR <- batter_steamer$HR[match(away_batter$vRcode, batter_steamer$m_id)]

vRBB <- rep(NA, 1)

away_batter <- data.frame(away_batter, vRBB)
away_batter$vRBB <- batter_steamer$BB[match(away_batter$vRcode, batter_steamer$m_id)]

vRSO <- rep(NA, 1)

away_batter <- data.frame(away_batter, vRSO)
away_batter$vRSO <- batter_steamer$K[match(away_batter$vRcode, batter_steamer$m_id)]

vRBO <- rep(NA, 1)

away_batter <- data.frame(away_batter, vRBO)
away_batter$vRBO <- batter_steamer$BO[match(away_batter$vRcode, batter_steamer$m_id)]

if(home_pitcher$Throw == "R") {
  batter_p1b <- away_batter$vR1B
  batter_p2b <- away_batter$vR2B
  batter_p3b <- away_batter$vR3B
  batter_phr <- away_batter$vRHR
  batter_pbb <- away_batter$vRBB
  batter_pso <- away_batter$vRSO
  batter_pbo <- away_batter$vRBO
  
} else {
  batter_p1b <- away_batter$vL1B
  batter_p2b <- away_batter$vL2B
  batter_p3b <- away_batter$vL3B
  batter_phr <- away_batter$vLHR
  batter_pbb <- away_batter$vLBB
  batter_pso <- away_batter$vLSO
  batter_pbo <- away_batter$vLBO
} 

if(away_batter$bats == "R") {
  pitcher_p1b <- home_pitcher$vR1B
  pitcher_p2b <- home_pitcher$vR2B
  pitcher_p3b <- home_pitcher$vR3B
  pitcher_phr <- home_pitcher$vRHR
  pitcher_pbb <- home_pitcher$vRBB
  pitcher_pso <- home_pitcher$vRSO
  pitcher_pbo <- home_pitcher$vRBO
} else {
  pitcher_p1b <- home_pitcher$vR1B
  pitcher_p2b <- home_pitcher$vR2B
  pitcher_p3b <- home_pitcher$vR3B
  pitcher_phr <- home_pitcher$vRHR
  pitcher_pbb <- home_pitcher$vRBB
  pitcher_pso <- home_pitcher$vRSO
  pitcher_pbo <- home_pitcher$vRBO
}

league_p1b <- .152056268409
league_p2b <- .045140889455
league_p3b <- .004727358249
league_phr <- .026802180461
league_pbb <- .081558771793
league_pso <- .198009085542
league_pbo <- .491705446091


# basic odds ratio calculator

odds1b <- ((batter_p1b / (1 - batter_p1b)) * 
           (pitcher_p1b / (1 - pitcher_p1b)) / 
           (league_p1b / (1 - league_p1b)))

odds2b <- ((batter_p2b / (1 - batter_p2b)) * 
           (pitcher_p2b / (1 - pitcher_p2b)) / 
           (league_p2b / (1 - league_p2b)))

odds3b <- ((batter_p3b / (1 - batter_p3b)) * 
           (pitcher_p3b / (1 - pitcher_p3b)) / 
           (league_p3b / (1 - league_p3b)))

oddshr <- ((batter_phr / (1 - batter_phr)) * 
           (pitcher_phr / (1 - pitcher_phr)) / 
           (league_phr / (1 - league_phr)))

oddsbb <- ((batter_pbb / (1 - batter_pbb)) * 
           (pitcher_pbb / (1 - pitcher_pbb)) / 
           (league_pbb / (1 - league_pbb)))

oddsso <- ((batter_pso / (1 - batter_pso)) * 
           (pitcher_pso / (1 - pitcher_pso)) / 
           (league_pso / (1 - league_pso)))

oddsbo <- ((batter_pbo / (1 - batter_pbo)) * 
           (pitcher_pbo / (1 - pitcher_pbo)) / 
           (league_pbo / (1 - league_pbo)))

# turn odds from odds calculator into probabilities

p1b <- odds1b / (odds1b + 1)
p2b <- odds2b / (odds2b + 1)
p3b <- odds3b / (odds3b + 1)
phr <- oddshr / (oddshr + 1)
pbb <- oddsbb / (oddsbb + 1)
pso <- oddsso / (oddsso + 1)
pbo <- oddsbo / (oddsbo + 1)
total <- p1b +
  p2b +
  p3b +
  phr +
  pbb +
  pso +
  pbo

# normalize probabilites to equal 1

np1b <- p1b / total
np2b <- p2b / total
np3b <- p3b / total
nphr <- phr / total
npbb <- pbb / total
npso <- pso / total
npbo <- pbo / total


xPA <- as.data.frame(rbind(np1b,
                           np2b,
                           np3b,
                           nphr,
                           npbb,
                           npso,
                           npbo
                           )
)

xPA$outcome <- c("1b", "2b", "3b", "hr", "bb", "so", "bo")


colnames(xPA) <- c("prob", "outcome")


PA_list <- c("1b", "2b", "3b", "hr", "bb", "so", "bo")

sim_PA <- as.data.frame(sample(xPA$prob, 1, replace = TRUE, prob = c(xPA$prob)))
colnames(sim_PA) <- "PA_result"

sim_PA_result <- as.data.frame(xPA$outcome[match(sim_PA$PA_result, xPA$prob)])
colnames(sim_PA_result) <- "result"
return(sim_PA_result)
}




## Inning Simulation ##
test <- function()
{
while (inning < 9) 
{
outs <- 0
first_base <- 0
second_base <- 0
third_base <- 0
while (outs < 3)
{
sim_PA_result <- at_bat(batter)

if(sim_PA_result[1,1] == 'bo' | sim_PA_result[1,1] == 'so')
{
  outs <- outs + 1
  box_score$PAs[batter] <- box_score$PAs[batter] + 1
}

if(sim_PA_result[1,1] == 'bb')
{
  runs_before <- runs
  if (third_base == 1 && second_base == 1)
  {
    runs <- runs + 1
    third_base <- 1
  }
  if (second_base == 1 && first_base == 1)
  {
    third_base <- 1
  }
  if (first_base == 1)
  {
    second_base <- 1
  }
  first_base <- 1
  runs_diff <- runs - runs_before
  box_score$PAs[batter] <- box_score$PAs[batter] + 1
  box_score$BB[batter] <- box_score$BB[batter] + 1
  box_score$RBI[batter] <- box_score$RBI[batter] + runs_diff
  }

if(sim_PA_result[1,1] == '1b')
{
  runs_before <- runs
  if (third_base == 1)
  {
    runs <- runs + 1
    third_base <- 0
  }
  if (second_base == 1)
  {
    third_base <- 1
  }
  if (first_base == 1)
  {
    second_base <- 1
  }
  first_base <- 1
  runs_diff <- runs - runs_before
  box_score$PAs[batter] <- box_score$PAs[batter] + 1
  box_score$Hits[batter] <- box_score$Hits[batter] + 1
  box_score$Single[batter] <- box_score$Single[batter] + 1
  box_score$RBI[batter] <- box_score$RBI[batter] + runs_diff
}

if(sim_PA_result[1,1] == '2b')
{
  runs_before <- runs
  if (third_base == 1)
  {
    runs <- runs + 1
    third_base <- 0
  }
  if (second_base == 1)
  {
    runs <- runs + 1
  }
  if (first_base == 1)
  {
    third_base <- 1
    first_base <- 0
  }
  second_base <- 1
  runs_diff <- runs - runs_before
  box_score$PAs[batter] <- box_score$PAs[batter] + 1
  box_score$Hits[batter] <- box_score$Hits[batter] + 1
  box_score$Double[batter] <- box_score$Double[batter] + 1
  box_score$RBI[batter] <- box_score$RBI[batter] + runs_diff
  
}

if(sim_PA_result[1,1] == '3b')
{
  runs_before <- runs
  if (third_base == 1)
  {
    runs <- runs + 1
    third_base <- 0
  }
  if (second_base == 1)
  {
    runs <- runs + 1
    second_base <- 0
  }
  if (first_base == 1)
  {
    runs <- runs + 1
    first_base <- 0
  }
  third_base <- 1
  runs_diff <- runs - runs_before
  box_score$PAs[batter] <- box_score$PAs[batter] + 1
  box_score$Hits[batter] <- box_score$Hits[batter] + 1
  box_score$Triple[batter] <- box_score$Triple[batter] + 1
  box_score$RBI[batter] <- box_score$RBI[batter] + runs_diff
}
if(sim_PA_result[1,1] == 'hr')
{
  runs_before <- runs
  if (third_base == 1)
  {
    runs <- runs + 1
    third_base <- 0
  }
  if (second_base == 1)
  {
    runs <- runs + 1
    second_base <- 0
  }
  if (first_base == 1)
  {
    runs <- runs + 1
    first_base <- 0
  }
  runs <- runs + 1
  runs_diff <- runs - runs_before
  box_score$PAs[batter] <- box_score$PAs[batter] + 1
  box_score$Hits[batter] <- box_score$Hits[batter] + 1
  box_score$HR[batter] <- box_score$HR[batter] + 1
  box_score$RBI[batter] <- box_score$RBI[batter] + runs_diff
}
if (batter == 9) {
  batter <- 1
} else {
  batter <- batter + 1
}
inning_state <- data.frame(c(outs, runs, first_base, second_base, third_base))
colnames(inning_state) <- "Results"
rownames(inning_state) <- c("Outs", "Runs", "First Base", "Second Base", "Third Base")
}
inning <- inning + 1
}
batter = 1
runs <- 0
inning <- 1
return(box_score)
}

##mean_box_score <- replicate(100, test())

box_score_total <- data.frame(PAs = integer(9),
                        Hits = integer(9),
                        BB = integer(9),
                        Single = integer(9),
                        Double = integer(9),
                        Triple = integer(9),
                        HR = integer(9),
                        Runs = integer(9),
                        RBI = integer(9))
i <- 0
while (i < 1000)
{
  batter = 1
  runs <- 0
  inning <- 1
  box_score <- data.frame(Name = character(9),
                          PAs = integer(9),
                          Hits = integer(9),
                          BB = integer(9),
                          Single = integer(9),
                          Double = integer(9),
                          Triple = integer(9),
                          HR = integer(9),
                          Runs = integer(9),
                          RBI = integer(9))
  box_score$Name <- away_lineup$Name
  box_score <- test()
  box_score_total <- box_score_total + box_score[,-1]
  i <- i + 1
}
box_score_total <- box_score_total/1000
box_score_total$Name <- box_score$Name
box_score_total <- box_score_total[,c(10,1:9)]
return(box_score_total)
}

home_team <- function(game)
{
  starters <- starter_scraper(game)
  home_lineup <- home_scraper(game) 
  away_lineup <- away_scraper(game)
  
  # scrape steamer projection files
  
  batter_steamer <- read.csv("steamer_batter_2018.csv")
  pitcher_steamer <- read.csv("steamer_pitcher_2018.csv")
  
  # read today's mlb lineups
  
  df <- read.csv("MLB Lineups Today.csv")
  
  # pulling away leadoff batter and home starting pitcher
  
  
  at_bat <- function(batter)
  {
    home_batter <- data.frame(home_lineup[batter,1], stringsAsFactors = FALSE)
    colnames(home_batter) <- "player"
    away_pitcher <- data.frame(starters[1,1], stringsAsFactors = FALSE)
    away_pitcher <- data.frame(lapply(away_pitcher, trimws), stringsAsFactors = FALSE)
    colnames(home_pitcher) <- "player"
    
    # parsing data frame for home pitcher with all play outcomes by split
    
    Throws <- rep(NA, 1)
    
    away_pitcher <- data.frame(away_pitcher, Throws)
    away_pitcher$Throws <- pitcher_steamer$Throws[match(away_pitcher$player, pitcher_steamer$name)]
    
    mlbamid <- rep(NA, 1)
    
    away_pitcher <- data.frame(away_pitcher, mlbamid)
    away_pitcher$mlbamid <- pitcher_steamer$mlbamid[match(away_pitcher$player, pitcher_steamer$name)]
    
    
    away_pitcher$vLcode <- paste("SP", "1", "vL", away_pitcher$mlbamid, sep= "-")
    away_pitcher$vRcode <- paste("SP", "1", "vR", away_pitcher$mlbamid, sep= "-")
    
    vL1B <- rep(NA, 1)
    
    away_pitcher <- data.frame(away_pitcher, vL1B)
    away_pitcher$vL1B <- pitcher_steamer$Single[match(away_pitcher$vLcode, pitcher_steamer$m_id)]
    
    vL2B <- rep(NA, 1)
    
    away_pitcher <- data.frame(away_pitcher, vL2B)
    away_pitcher$vL2B <- pitcher_steamer$Double[match(away_pitcher$vLcode, pitcher_steamer$m_id)]
    
    vL3B <- rep(NA, 1)
    
    away_pitcher <- data.frame(away_pitcher, vL3B)
    away_pitcher$vL3B <- pitcher_steamer$Triple[match(away_pitcher$vLcode, pitcher_steamer$m_id)]
    
    
    vLHR <- rep(NA, 1)
    
    away_pitcher <- data.frame(away_pitcher, vLHR)
    away_pitcher$vLHR <- pitcher_steamer$HR[match(away_pitcher$vLcode, pitcher_steamer$m_id)]
    
    vLBB <- rep(NA, 1)
    
    away_pitcher <- data.frame(away_pitcher, vLBB)
    away_pitcher$vLBB <- pitcher_steamer$BB[match(away_pitcher$vLcode, pitcher_steamer$m_id)]
    
    vLSO <- rep(NA, 1)
    
    away_pitcher <- data.frame(away_pitcher, vLSO)
    away_pitcher$vLSO <- pitcher_steamer$K[match(away_pitcher$vLcode, pitcher_steamer$m_id)]
    
    vLBO <- rep(NA, 1)
    
    away_pitcher <- data.frame(away_pitcher, vLBO)
    away_pitcher$vLBO <- pitcher_steamer$BO[match(away_pitcher$vLcode, pitcher_steamer$m_id)]
    
    vR1B <- rep(NA, 1)
    
    away_pitcher <- data.frame(away_pitcher, vR1B)
    away_pitcher$vR1B <- pitcher_steamer$Single[match(away_pitcher$vRcode, pitcher_steamer$m_id)]
    
    vR2B <- rep(NA, 1)
    
    away_pitcher <- data.frame(away_pitcher, vR2B)
    away_pitcher$vR2B <- pitcher_steamer$Double[match(away_pitcher$vRcode, pitcher_steamer$m_id)]
    
    vR3B <- rep(NA, 1)
    
    away_pitcher <- data.frame(away_pitcher, vR3B)
    away_pitcher$vR3B <- pitcher_steamer$Triple[match(away_pitcher$vRcode, pitcher_steamer$m_id)]
    
    
    vRHR <- rep(NA, 1)
    
    away_pitcher <- data.frame(away_pitcher, vRHR)
    away_pitcher$vRHR <- pitcher_steamer$HR[match(away_pitcher$vRcode, pitcher_steamer$m_id)]
    
    vRBB <- rep(NA, 1)
    
    away_pitcher <- data.frame(away_pitcher, vRBB)
    away_pitcher$vRBB <- pitcher_steamer$BB[match(away_pitcher$vRcode, pitcher_steamer$m_id)]
    
    vRSO <- rep(NA, 1)
    
    away_pitcher <- data.frame(away_pitcher, vRSO)
    away_pitcher$vRSO <- pitcher_steamer$K[match(away_pitcher$vRcode, pitcher_steamer$m_id)]
    
    vRBO <- rep(NA, 1)
    
    away_pitcher <- data.frame(away_pitcher, vRBO)
    away_pitcher$vRBO <- pitcher_steamer$BO[match(away_pitcher$vRcode, pitcher_steamer$m_id)]
    
    # done parsing pitcher play outcomes by split
    
    # parsing data frame for away batter with all play outcomes by split
    
    bats <- rep(NA, 1)
    
    home_batter <- data.frame(home_batter, bats)
    home_batter$bats <- batter_steamer$bats[match(home_batter$player, batter_steamer$name)]
    
    
    mlbamid <- rep(NA, 1)
    home_batter <- data.frame(home_batter, mlbamid)
    home_batter$mlbamid <- batter_steamer$mlbamid[match(home_batter$player, batter_steamer$name)]
    
    home_batter$vLcode <- paste("1", "vL", home_batter$mlbamid, sep= "-")
    home_batter$vRcode <- paste("1", "vR", home_batter$mlbamid, sep= "-")
    
    vL1B <- rep(NA, 1)
    
    home_batter <- data.frame(home_batter, vL1B)
    home_batter$vL1B <- batter_steamer$Single[match(home_batter$vLcode, batter_steamer$m_id)]
    
    vL2B <- rep(NA, 1)
    
    home_batter <- data.frame(home_batter, vL2B)
    home_batter$vL2B <- batter_steamer$Double[match(home_batter$vLcode, batter_steamer$m_id)]
    
    vL3B <- rep(NA, 1)
    
    home_batter <- data.frame(home_batter, vL3B)
    home_batter$vL3B <- batter_steamer$Triple[match(home_batter$vLcode, batter_steamer$m_id)]
    
    
    vLHR <- rep(NA, 1)
    
    home_batter <- data.frame(home_batter, vLHR)
    home_batter$vLHR <- batter_steamer$HR[match(home_batter$vLcode, batter_steamer$m_id)]
    
    vLBB <- rep(NA, 1)
    
    home_batter <- data.frame(home_batter, vLBB)
    home_batter$vLBB <- batter_steamer$BB[match(home_batter$vLcode, batter_steamer$m_id)]
    
    vLSO <- rep(NA, 1)
    
    home_batter <- data.frame(home_batter, vLSO)
    home_batter$vLSO <- batter_steamer$K[match(home_batter$vLcode, batter_steamer$m_id)]
    
    vLBO <- rep(NA, 1)
    
    home_batter <- data.frame(home_batter, vLBO)
    home_batter$vLBO <- batter_steamer$BO[match(home_batter$vLcode, batter_steamer$m_id)]
    
    vR1B <- rep(NA, 1)
    
    home_batter <- data.frame(home_batter, vR1B)
    home_batter$vR1B <- batter_steamer$Single[match(home_batter$vRcode, batter_steamer$m_id)]
    
    vR2B <- rep(NA, 1)
    
    home_batter <- data.frame(home_batter, vR2B)
    home_batter$vR2B <- batter_steamer$Double[match(home_batter$vRcode, batter_steamer$m_id)]
    
    vR3B <- rep(NA, 1)
    
    home_batter <- data.frame(home_batter, vR3B)
    home_batter$vR3B <- batter_steamer$Triple[match(home_batter$vRcode, batter_steamer$m_id)]
    
    
    vRHR <- rep(NA, 1)
    
    home_batter <- data.frame(home_batter, vRHR)
    home_batter$vRHR <- batter_steamer$HR[match(home_batter$vRcode, batter_steamer$m_id)]
    
    vRBB <- rep(NA, 1)
    
    home_batter <- data.frame(home_batter, vRBB)
    home_batter$vRBB <- batter_steamer$BB[match(home_batter$vRcode, batter_steamer$m_id)]
    
    vRSO <- rep(NA, 1)
    
    home_batter <- data.frame(home_batter, vRSO)
    home_batter$vRSO <- batter_steamer$K[match(home_batter$vRcode, batter_steamer$m_id)]
    
    vRBO <- rep(NA, 1)
    
    home_batter <- data.frame(home_batter, vRBO)
    home_batter$vRBO <- batter_steamer$BO[match(home_batter$vRcode, batter_steamer$m_id)]
    
    if(away_pitcher$Throw == "R") {
      batter_p1b <- home_batter$vR1B
      batter_p2b <- home_batter$vR2B
      batter_p3b <- home_batter$vR3B
      batter_phr <- home_batter$vRHR
      batter_pbb <- home_batter$vRBB
      batter_pso <- home_batter$vRSO
      batter_pbo <- home_batter$vRBO
      
    } else {
      batter_p1b <- home_batter$vL1B
      batter_p2b <- home_batter$vL2B
      batter_p3b <- home_batter$vL3B
      batter_phr <- home_batter$vLHR
      batter_pbb <- home_batter$vLBB
      batter_pso <- home_batter$vLSO
      batter_pbo <- home_batter$vLBO
    } 
    
    if(home_batter$bats == "R") {
      pitcher_p1b <- home_pitcher$vR1B
      pitcher_p2b <- home_pitcher$vR2B
      pitcher_p3b <- home_pitcher$vR3B
      pitcher_phr <- home_pitcher$vRHR
      pitcher_pbb <- home_pitcher$vRBB
      pitcher_pso <- home_pitcher$vRSO
      pitcher_pbo <- home_pitcher$vRBO
    } else {
      pitcher_p1b <- home_pitcher$vR1B
      pitcher_p2b <- home_pitcher$vR2B
      pitcher_p3b <- home_pitcher$vR3B
      pitcher_phr <- home_pitcher$vRHR
      pitcher_pbb <- home_pitcher$vRBB
      pitcher_pso <- home_pitcher$vRSO
      pitcher_pbo <- home_pitcher$vRBO
    }
    
    league_p1b <- .152056268409
    league_p2b <- .045140889455
    league_p3b <- .004727358249
    league_phr <- .026802180461
    league_pbb <- .081558771793
    league_pso <- .198009085542
    league_pbo <- .491705446091
    
    
    # basic odds ratio calculator
    
    odds1b <- ((batter_p1b / (1 - batter_p1b)) * 
                 (pitcher_p1b / (1 - pitcher_p1b)) / 
                 (league_p1b / (1 - league_p1b)))
    
    odds2b <- ((batter_p2b / (1 - batter_p2b)) * 
                 (pitcher_p2b / (1 - pitcher_p2b)) / 
                 (league_p2b / (1 - league_p2b)))
    
    odds3b <- ((batter_p3b / (1 - batter_p3b)) * 
                 (pitcher_p3b / (1 - pitcher_p3b)) / 
                 (league_p3b / (1 - league_p3b)))
    
    oddshr <- ((batter_phr / (1 - batter_phr)) * 
                 (pitcher_phr / (1 - pitcher_phr)) / 
                 (league_phr / (1 - league_phr)))
    
    oddsbb <- ((batter_pbb / (1 - batter_pbb)) * 
                 (pitcher_pbb / (1 - pitcher_pbb)) / 
                 (league_pbb / (1 - league_pbb)))
    
    oddsso <- ((batter_pso / (1 - batter_pso)) * 
                 (pitcher_pso / (1 - pitcher_pso)) / 
                 (league_pso / (1 - league_pso)))
    
    oddsbo <- ((batter_pbo / (1 - batter_pbo)) * 
                 (pitcher_pbo / (1 - pitcher_pbo)) / 
                 (league_pbo / (1 - league_pbo)))
    
    # turn odds from odds calculator into probabilities
    
    p1b <- odds1b / (odds1b + 1)
    p2b <- odds2b / (odds2b + 1)
    p3b <- odds3b / (odds3b + 1)
    phr <- oddshr / (oddshr + 1)
    pbb <- oddsbb / (oddsbb + 1)
    pso <- oddsso / (oddsso + 1)
    pbo <- oddsbo / (oddsbo + 1)
    total <- p1b +
      p2b +
      p3b +
      phr +
      pbb +
      pso +
      pbo
    
    # normalize probabilites to equal 1
    
    np1b <- p1b / total
    np2b <- p2b / total
    np3b <- p3b / total
    nphr <- phr / total
    npbb <- pbb / total
    npso <- pso / total
    npbo <- pbo / total
    
    
    xPA <- as.data.frame(rbind(np1b,
                               np2b,
                               np3b,
                               nphr,
                               npbb,
                               npso,
                               npbo
    )
    )
    
    xPA$outcome <- c("1b", "2b", "3b", "hr", "bb", "so", "bo")
    
    
    colnames(xPA) <- c("prob", "outcome")
    
    
    PA_list <- c("1b", "2b", "3b", "hr", "bb", "so", "bo")
    
    sim_PA <- as.data.frame(sample(xPA$prob, 1, replace = TRUE, prob = c(xPA$prob)))
    colnames(sim_PA) <- "PA_result"
    
    sim_PA_result <- as.data.frame(xPA$outcome[match(sim_PA$PA_result, xPA$prob)])
    colnames(sim_PA_result) <- "result"
    return(sim_PA_result)
  }
  
  
  
  
  ## Inning Simulation ##
  test <- function()
  {
    while (inning < 9) 
    {
      outs <- 0
      first_base <- 0
      second_base <- 0
      third_base <- 0
      while (outs < 3)
      {
        sim_PA_result <- at_bat(batter)
        
        if(sim_PA_result[1,1] == 'bo' | sim_PA_result[1,1] == 'so')
        {
          outs <- outs + 1
          box_score$PAs[batter] <- box_score$PAs[batter] + 1
        }
        
        if(sim_PA_result[1,1] == 'bb')
        {
          runs_before <- runs
          if (third_base == 1 && second_base == 1)
          {
            runs <- runs + 1
            third_base <- 1
          }
          if (second_base == 1 && first_base == 1)
          {
            third_base <- 1
          }
          if (first_base == 1)
          {
            second_base <- 1
          }
          first_base <- 1
          runs_diff <- runs - runs_before
          box_score$PAs[batter] <- box_score$PAs[batter] + 1
          box_score$BB[batter] <- box_score$BB[batter] + 1
          box_score$RBI[batter] <- box_score$RBI[batter] + runs_diff
        }
        
        if(sim_PA_result[1,1] == '1b')
        {
          runs_before <- runs
          if (third_base == 1)
          {
            runs <- runs + 1
            third_base <- 0
          }
          if (second_base == 1)
          {
            third_base <- 1
          }
          if (first_base == 1)
          {
            second_base <- 1
          }
          first_base <- 1
          runs_diff <- runs - runs_before
          box_score$PAs[batter] <- box_score$PAs[batter] + 1
          box_score$Hits[batter] <- box_score$Hits[batter] + 1
          box_score$Single[batter] <- box_score$Single[batter] + 1
          box_score$RBI[batter] <- box_score$RBI[batter] + runs_diff
        }
        
        if(sim_PA_result[1,1] == '2b')
        {
          runs_before <- runs
          if (third_base == 1)
          {
            runs <- runs + 1
            third_base <- 0
          }
          if (second_base == 1)
          {
            runs <- runs + 1
          }
          if (first_base == 1)
          {
            third_base <- 1
            first_base <- 0
          }
          second_base <- 1
          runs_diff <- runs - runs_before
          box_score$PAs[batter] <- box_score$PAs[batter] + 1
          box_score$Hits[batter] <- box_score$Hits[batter] + 1
          box_score$Double[batter] <- box_score$Double[batter] + 1
          box_score$RBI[batter] <- box_score$RBI[batter] + runs_diff
          
        }
        
        if(sim_PA_result[1,1] == '3b')
        {
          runs_before <- runs
          if (third_base == 1)
          {
            runs <- runs + 1
            third_base <- 0
          }
          if (second_base == 1)
          {
            runs <- runs + 1
            second_base <- 0
          }
          if (first_base == 1)
          {
            runs <- runs + 1
            first_base <- 0
          }
          third_base <- 1
          runs_diff <- runs - runs_before
          box_score$PAs[batter] <- box_score$PAs[batter] + 1
          box_score$Hits[batter] <- box_score$Hits[batter] + 1
          box_score$Triple[batter] <- box_score$Triple[batter] + 1
          box_score$RBI[batter] <- box_score$RBI[batter] + runs_diff
        }
        if(sim_PA_result[1,1] == 'hr')
        {
          runs_before <- runs
          if (third_base == 1)
          {
            runs <- runs + 1
            third_base <- 0
          }
          if (second_base == 1)
          {
            runs <- runs + 1
            second_base <- 0
          }
          if (first_base == 1)
          {
            runs <- runs + 1
            first_base <- 0
          }
          runs <- runs + 1
          runs_diff <- runs - runs_before
          box_score$PAs[batter] <- box_score$PAs[batter] + 1
          box_score$Hits[batter] <- box_score$Hits[batter] + 1
          box_score$HR[batter] <- box_score$HR[batter] + 1
          box_score$RBI[batter] <- box_score$RBI[batter] + runs_diff
        }
        if (batter == 9) {
          batter <- 1
        } else {
          batter <- batter + 1
        }
        inning_state <- data.frame(c(outs, runs, first_base, second_base, third_base))
        colnames(inning_state) <- "Results"
        rownames(inning_state) <- c("Outs", "Runs", "First Base", "Second Base", "Third Base")
      }
      inning <- inning + 1
    }
    batter = 1
    runs <- 0
    inning <- 1
    return(box_score)
  }
  
  ##mean_box_score <- replicate(100, test())
  
  box_score_total <- data.frame(PAs = integer(9),
                                Hits = integer(9),
                                BB = integer(9),
                                Single = integer(9),
                                Double = integer(9),
                                Triple = integer(9),
                                HR = integer(9),
                                Runs = integer(9),
                                RBI = integer(9))
  i <- 0
  while (i < 1000)
  {
    batter = 1
    runs <- 0
    inning <- 1
    box_score <- data.frame(Name = character(9),
                            PAs = integer(9),
                            Hits = integer(9),
                            BB = integer(9),
                            Single = integer(9),
                            Double = integer(9),
                            Triple = integer(9),
                            HR = integer(9),
                            Runs = integer(9),
                            RBI = integer(9))
    box_score$Name <- away_lineup$Name
    box_score <- test()
    box_score_total <- box_score_total + box_score[,-1]
    i <- i + 1
  }
  box_score_total <- box_score_total/1000
  box_score_total$Name <- box_score$Name
  box_score_total <- box_score_total[,c(10,1:9)]
  return(box_score_total)
}


rangers <- away_team(4)
red_sox <- home_team(4)

##write.csv(sim_PA, "MLB Simulated AB.csv")

proc.time() - time_start 
