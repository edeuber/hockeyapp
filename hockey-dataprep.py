# -*- coding: utf-8 -*-
"""
Created on Tue May 24 18:30:02 2022

@author: deube
"""

import pandas as pd
import numpy as np
from io import BytesIO
from csv import writer 
import csv
import itertools

rawData2011 = pd.read_csv('shots_2011.csv')
rawData2012 = pd.read_csv('shots_2012.csv')
rawData2013 = pd.read_csv('shots_2013.csv')
rawData2014 = pd.read_csv('shots_2014.csv')
rawData2015 = pd.read_csv('shots_2015.csv')
rawData2016 = pd.read_csv('shots_2016.csv')
rawData2017 = pd.read_csv('shots_2017.csv')
rawData2018 = pd.read_csv('shots_2018.csv')
rawData2019 = pd.read_csv('shots_2019.csv')
rawData2020 = pd.read_csv('shots_2020.csv')
rawData2021 = pd.read_csv('shots_2021.csv')

rawData = pd.DataFrame()
rawData = rawData.append(rawData2011)
rawData = rawData.append(rawData2012)
rawData = rawData.append(rawData2013)
rawData = rawData.append(rawData2014)
rawData = rawData.append(rawData2015)
rawData = rawData.append(rawData2016)
rawData = rawData.append(rawData2017)
rawData = rawData.append(rawData2018)
rawData = rawData.append(rawData2019)
rawData = rawData.append(rawData2020)
rawData = rawData.append(rawData2021)

goalsOnly = rawData[rawData['goal'] == 1]
goalsOnly = goalsOnly[goalsOnly['isPlayoffGame'] == 0]

refinedData = goalsOnly[['game_id','period','awayTeamGoals','homeTeamGoals', 'isHomeTeam']].copy()

homeScore = []
awayScore = []

for record in range(len(refinedData)):
    
    
    if refinedData.iloc[record,4] == 1:  ##this sees if it is a home goal
        homeGoals = refinedData.iloc[record,3] + 1 #if so add score to home goal tally

        if record == 0:
            awayGoals = 0
        else:
            #check if it is a new game
            if refinedData.iloc[record,0] != refinedData.iloc[record-1,0]:
                awayGoals = 0
            else:
                awayGoals = awayScore[record-1]

        homeScore.append(homeGoals)
        awayScore.append(awayGoals)
    else:
        awayGoals = refinedData.iloc[record,2] + 1
        
        if record == 0:
            homeGoals = 0
        else:
            #check if it is a new game
            if refinedData.iloc[record,0] != refinedData.iloc[record-1,0]:
                homeGoals = 0
            else:
                homeGoals = homeScore[record-1]        
        
        homeScore.append(homeGoals)
        awayScore.append(awayGoals)


#games = refinedData['game_id'].unique()

refinedData["HomeScore"] = homeScore
refinedData["AwayScore"] = awayScore


##Now we need to determine final reg scores
gameIds = []
finalHome = []
finalAway = []
period = []
isOvertime = []

for record in range(len(refinedData)):
    if record == len(refinedData)-1:
        print("here")
        print(record)
        if refinedData.iloc[record,1] >= 4:
            gameIds.append(refinedData.iloc[record,0])
            
            #The score was tied at the end of reg. It went to OT. I want scores at end of reg
            if refinedData.iloc[record,5] > refinedData.iloc[record,6]:
                finalHome.append(refinedData.iloc[record,5]-1)
                finalAway.append(refinedData.iloc[record,6])
            else:
                finalHome.append(refinedData.iloc[record,5])
                finalAway.append(refinedData.iloc[record,6]-1)
            
            period.append(refinedData.iloc[record,1])
            isOvertime.append(1)
        else:
            gameIds.append(refinedData.iloc[record,0])
            finalHome.append(refinedData.iloc[record,5])
            finalAway.append(refinedData.iloc[record,6])
            period.append(refinedData.iloc[record,1])
            isOvertime.append(0)
        break
    if refinedData.iloc[record,0] != refinedData.iloc[record+1,0]:
        if refinedData.iloc[record,1] >= 4:
            gameIds.append(refinedData.iloc[record,0])
            
            #The score was tied at the end of reg. It went to OT. I want scores at end of reg
            if refinedData.iloc[record,5] > refinedData.iloc[record,6]:
                finalHome.append(refinedData.iloc[record,5]-1)
                finalAway.append(refinedData.iloc[record,6])
            else:
                finalHome.append(refinedData.iloc[record,5])
                finalAway.append(refinedData.iloc[record,6]-1)
            
            period.append(refinedData.iloc[record,1])
            isOvertime.append(1)
        else:
            gameIds.append(refinedData.iloc[record,0])
            finalHome.append(refinedData.iloc[record,5])
            finalAway.append(refinedData.iloc[record,6])
            period.append(refinedData.iloc[record,1])
            isOvertime.append(0)

        
resultsdf = pd.DataFrame()
resultsdf["GameId"] = gameIds
resultsdf["HomeScore"] = finalHome
resultsdf["AwayScore"] = finalAway
resultsdf["Period"] = period
resultsdf["OT"] = isOvertime

##Now we need to determine scores going into the the third period
gameIds = []
secondHome = []
secondAway = []

for record in range(len(refinedData)):
    gameId = refinedData.iloc[record,0]
    
    if gameId not in gameIds:
        #Check to see if there was no scoring in the 3rd (last goal was in 1st or 2nd). This will be score going into 2nd and final score
        x = resultsdf.loc[resultsdf['GameId']==gameId] #Getting final score of game id in current iteration
        if x.iloc[0,3] == 1 or x.iloc[0,3] == 2:
            gameIds.append(refinedData.iloc[record,0])
            secondHome.append(x.iloc[0,1])
            secondAway.append(x.iloc[0,2])
        
    if gameId not in gameIds: #Normal game with goals scored in all 3 peridos
        if (refinedData.iloc[record,1] == 3 and refinedData.iloc[record-1,1] != 3) and refinedData.iloc[record,0] == refinedData.iloc[record-1,0]:
                gameIds.append(refinedData.iloc[record-1,0])
                secondHome.append(refinedData.iloc[record-1,5])
                secondAway.append(refinedData.iloc[record-1,6])
      
    if gameId not in gameIds: #No goals were scored in periods 1 and 2 but there were goals in 3
        if refinedData.iloc[record,1] == 3 and refinedData.iloc[record,0] != refinedData.iloc[record-1,0]:
                gameIds.append(refinedData.iloc[record,0])
                secondHome.append(0)
                secondAway.append(0)                
      
    if gameId not in gameIds: #first and only goal was scored in overtime
        if refinedData.iloc[record,1] >= 4  and refinedData.iloc[record,0] != refinedData.iloc[record-1,0]:
                gameIds.append(refinedData.iloc[record,0])
                secondHome.append(0)
                secondAway.append(0)
    
    if gameId not in gameIds: #No goals in third but there were goals in first or second and it went to overtime
        if (refinedData.iloc[record,1] >= 4 and refinedData.iloc[record-1,1] != 3)  and refinedData.iloc[record,0] == refinedData.iloc[record-1,0]:
                gameIds.append(refinedData.iloc[record-1,0])
                secondHome.append(refinedData.iloc[record-1,5])
                secondAway.append(refinedData.iloc[record-1,6])
    
                
seconddf = pd.DataFrame()
seconddf["GameId"] = gameIds
seconddf["HomeScore"] = secondHome
seconddf["AwayScore"] = secondAway

##Now we need to see how well we would do!!!
##resultsdf.iloc[0,1] ##home
##resultsdf.iloc[0,2] ##away

def runSim(seconddf,resultsdf,bet,money,payout):

    wins = []
    total = []
    games = []
    check = []
    money = money
    bet = bet
    totalBet = bet * 7

    for record in range(len(seconddf)):
    
    
         i = 0
         diff = seconddf.iloc[record,1] - seconddf.iloc[record,2] #Postive means home is winning
         homeOrg = seconddf.iloc[record,1]
         awayOrg = seconddf.iloc[record,2]
         homefinal = resultsdf.iloc[record,1]
         awayfinal = resultsdf.iloc[record,2]
    
        
         if diff == 0: #Game is tied  
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 2
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 0
             away4 = awayOrg + 2
             #No goals
             home5 = homeOrg + 3
             away5 = awayOrg + 1
             #No goals
             home6 = homeOrg + 1
             away6 = awayOrg + 3
             #No goals
             home7 = homeOrg + 2
             away7 = awayOrg + 2
             
        ##ONE GOAL GAME
         if diff == 1: #Home is winning by 1
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 0
             away2 = awayOrg + 2
             #No goals
             home3 = homeOrg + 2
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 1
             away5 = awayOrg + 2
             #No goals
             home6 = homeOrg + 2
             away6 = awayOrg + 1
             #No goals
             home7 = homeOrg + 1
             away7 = awayOrg + 0
             
         if diff == -1: #Home is losing by 1
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 0
             away2 = awayOrg + 2
             #No goals
             home3 = homeOrg + 2
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 1
             away5 = awayOrg + 2
             #No goals
             home6 = homeOrg + 2
             away6 = awayOrg + 1
             #No goals
             home7 = homeOrg + 1
             away7 = awayOrg + 0
    
        ##TWO GOAL GAME
         if diff == 2: #Home is winning by 2
             #No goals
             home1 = homeOrg + 1
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 2
             away2 = awayOrg + 0
             #No goals
             home3 = homeOrg + 1
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 2
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 0
             away5 = awayOrg + 2
             #No goals
             home6 = homeOrg + 0
             away6 = awayOrg + 1
             #No goals
             home7 = homeOrg + 2
             away7 = awayOrg + 2
             
         if diff == -2: #Home is losing by 2
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 2
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 2
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 2
             away5 = awayOrg + 0
             #No goals
             home6 = homeOrg + 1
             away6 = awayOrg + 0
             #No goals
             home7 = homeOrg + 2
             away7 = awayOrg + 1
             
        ##THREE GOAL GAME
         if diff == 3: #Home is winning by 3
             #No goals
             home1 = homeOrg + 1
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 2
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 2
             away5 = awayOrg + 2
             #No goals
             home6 = homeOrg + 0
             away6 = awayOrg + 1
             #No goals
             home7 = homeOrg + 0
             away7 = awayOrg + 2
             
         if diff == -3: #Home is losing by 3
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 2
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 1
             away5 = awayOrg + 2
             #No goals
             home6 = homeOrg + 1
             away6 = awayOrg + 0
             #No goals
             home7 = homeOrg + 2
             away7 = awayOrg + 2
             
        ##FOUR GOAL GAME
         if diff >= 4: #Home is winning by 4 or more
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 0
             #No goals
             home3 = homeOrg + 1
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 0
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 2
             away5 = awayOrg + 1
             #No goals
             home6 = homeOrg + 1
             away6 = awayOrg + 2
             #No goals
             home7 = homeOrg + 2
             away7 = awayOrg + 0
             
         if diff <= -4: #Home is losing by 4 or more
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 2
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 0
             away4 = awayOrg + 2
             #No goals
             home5 = homeOrg + 1
             away5 = awayOrg + 0
             #No goals
             home6 = homeOrg + 1
             away6 = awayOrg + 2
             #No goals
             home7 = homeOrg + 2
             away7 = awayOrg + 0
     
        ##Determine results
         if diff != 1 and diff != 0:     
             if homefinal == home1 and awayfinal ==away1:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[0]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "1")
                i = 1
                
             if homefinal == home2 and awayfinal ==away2:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[1]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "2")
                i = 1
            
             if homefinal == home3 and awayfinal ==away3:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[2]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "3")
                i = 1
        
             if homefinal == home4 and awayfinal ==away4:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[3]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "4")
                i = 1
                
             if homefinal == home5 and awayfinal ==away5:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[4]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "5")
                i = 1
            
             if homefinal == home6 and awayfinal ==away6:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[5]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "6")
                i = 1  
    
                
             if homefinal == home7 and awayfinal ==away7:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[6]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "7")
                i = 1
                
             if i == 0:
                #print("You lost money big dumb!!")
                #print("Loss. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money - totalBet
                #print(str(money))
                wins.append(0)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "Loss")
                #print("\n")
         #else:
             #print("SKIPPED BECAUSE DIFF WAS ONE")
             #print("\n")

    return money, wins, total    
                
    games.append(seconddf.iloc[record,0])
    

     
final = pd.DataFrame()
final["Game ID"] = gameIds
final["2nd Home"] = secondHome
final["2nd Away"] = secondAway
final["Final Home"] = finalHome
final["Final Away"] = finalAway
#final["Win?"] = wins


                

##Determining the most likely third period goal scoring for each going into second situation
scoreline = []
homeAway = []
difference = []
negGames = []

for record in range(len(seconddf)):

     i = 0
     diff = seconddf.iloc[record,1] - seconddf.iloc[record,2] #Postive means home is winning
     homeOrg = seconddf.iloc[record,1]
     awayOrg = seconddf.iloc[record,2]
     homefinal = resultsdf.iloc[record,1]
     awayfinal = resultsdf.iloc[record,2]
     
     homeGoals = homefinal - homeOrg
     awayGoals = awayfinal - awayOrg

     if diff == 2:
        scoreline.append(str(homeGoals) + " to " + str(awayGoals))
        homeAway.append("Home")
        difference.append(2)
        
     if diff == -2:
        scoreline.append(str(homeGoals)  + " to " + str(awayGoals))
        homeAway.append("Away")
        difference.append(2)
        
     if diff == 3:
        scoreline.append(str(homeGoals)  + " to " +str(awayGoals))
        homeAway.append("Home")
        difference.append(3)
        
     if diff == -3:
        scoreline.append(str(homeGoals)  + " to " + str(awayGoals))
        homeAway.append("Away")
        difference.append(3)
        
     if diff >= 4:
        scoreline.append(str(homeGoals)  + " to " + str(awayGoals))
        homeAway.append("Home")
        difference.append(4)
         
     if diff <= -4:
        scoreline.append(str(homeGoals)  + " to " + str(awayGoals))
        homeAway.append("Away")
        difference.append(4)
        
     if awayGoals == -1:
        negGames.append(resultsdf.iloc[record,0])
        
analysis = pd.DataFrame() 
analysis["Difference"] = difference
analysis["Third Score"] = scoreline
analysis["Team that was winning"] = homeAway
analysis.to_csv("analysis - Past 10 Years.csv")


##This section is dedicated to determining winnable ranges for the odds of each category 1-7



 
#itemindex = np.where(bets == 8)

#itemindex[0][0]
#2.00,2.5,3.0,3.5,4,4.5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,11,12]
ranges = np.array([0.00,0.5,1.0,1.5,2.00,2.5,3.0,3.5,4,6,7,8,10,15,18])
bets = np.array([1.5,3.00,4.00,5.00,5.00,5.00,6.00])
allBets = []
for constant in range(len(bets)):
    i = 0
    while(i < len(ranges)):
        currentConstant = bets[constant] + ranges[i]
        print("\n")
        print("Current Constant: " + str(currentConstant))
        constantIndex = np.where(bets == currentConstant)   
        newBetArray = bets.copy()
        newBetArray[constant] = currentConstant
        for bet in range(len(bets)):
            currentChange = bets[bet]
            itemindex = np.where(bets == currentChange)

            for itr in range(len(ranges)):
                newestBetArray = newBetArray.copy()
                newestBetArray = newestBetArray + ranges[itr]
                newestBetArray[constant] = currentConstant
                for itr in range(len(ranges)):
                    betArray = newestBetArray.copy()
                    change = ranges[itr]
                    newBet = currentChange + change
                    if bet != constant:
                        #print("New Bet Value: " + str(newBet))
                        betArray[bet] = newBet
                        betArrayList = betArray.tolist()
                        if betArrayList not in allBets:
                            allBets.append(betArrayList)
                            print(betArrayList)  
                        else:
                            print("ALREADY IN LIST")
        print("--------WE HAVE FINISHED AN ITERATION--------------")                    
        i = i + 1
   


##Determine the bet ranges that actually make money. We will want to bet on those.          
i = 0
moneys = []
moneyValues = []
for payout in allBets:
    i = i + 1
    x = runSim(seconddf,resultsdf,25,2000,payout)
    print(i)
    print(x[0])
    print(payout)
    print("\n")
    if x[0] > 2000:
        print("You made money! It was:    " + str(x[0]))
        moneys.append(payout)
        moneyValues.append(x[0])

moneyDf = pd.DataFrame(moneys)
moneyDf["Money"] = moneyValues
moneyDf.to_csv("In_the_money2.csv")


#Read in winning payout combinations
winners = pd.read_csv("In_the_money2.csv")

##This is where we check to see if the payouts for a particular game fall within our acceptable range
payout1 = 6.44
payout2 = 11.18
payout3 = 11.56
payout4 = 5.56
payout5 = 8.87
payout6 = 5.46
payout7 = 9.68


i = 0
##Checking first
pCheck = winners[winners['0'] <= payout1]
if len(pCheck) > 0:
    print("First payout good")
    pCheck = pCheck[(pCheck['1'] <= payout2) & (pCheck['2'] <= payout3) | (pCheck['2'] <= payout2) & (pCheck['1'] <= payout3)]
    
    ##Checking second and third
    if len(pCheck) > 0:
        print("2nd and 3rd payout good")
        pCheck = pCheck[(pCheck['3'] <= payout4) & (pCheck['4'] <= payout5) | (pCheck['4'] <= payout4) & (pCheck['3'] <= payout5)] 
        
        #Checking fourth and fifth
        if len(pCheck) > 0:
            print("4th and 5th payout good")
            pCheck = pCheck[(pCheck['5'] <= payout6) & (pCheck['6'] <= payout7) | (pCheck['6'] <= payout6) & (pCheck['5'] <= payout7)] 

            #Checking sixth and seventh
            if len(pCheck) > 0:
                print("6th and 7th payout good.Let's ride.")
                print("You should bet on this game!!")
                i = 1
            else:
                print("6th and 7th payout too low")
        else:
            print("4th and 5th payout too low")
    else:
        print("2nd and 3rd payout too low")    
else:
    print("First payout too low")
                



##Method 2
payout1 = 6
payout2 = 6
payout3 = 6
payout4 = 11
payout5 = 21.5
payout6 = 6
payout7 = 11

pCheck = winners[(winners['0'] <= payout1) & (winners['1'] <= payout2) | (winners['1'] <= payout1) & (winners['0'] <= payout2)]
if len(pCheck) > 0:
    print("First payout good")
    pCheck = pCheck[(pCheck['1'] <= payout2) & (pCheck['2'] <= payout3) & (pCheck['3'] <= payout4) |
                    (pCheck['1'] <= payout2) & (pCheck['3'] <= payout3) & (pCheck['2'] <= payout4) |
                    (pCheck['2'] <= payout2) & (pCheck['1'] <= payout3) & (pCheck['3'] <= payout4) |
                    (pCheck['2'] <= payout2) & (pCheck['3'] <= payout3) & (pCheck['1'] <= payout4) |
                    (pCheck['3'] <= payout2) & (pCheck['2'] <= payout3) & (pCheck['1'] <= payout4) |
                    (pCheck['3'] <= payout2) & (pCheck['1'] <= payout3) & (pCheck['2'] <= payout4)]
    
    ##Checking 2-4
    if len(pCheck) > 0:
        print("1-4 payouts good")
        pCheck = pCheck[(pCheck['4'] <= payout5) & (pCheck['5'] <= payout6) & (pCheck['6'] <= payout7) |
                        (pCheck['4'] <= payout5) & (pCheck['6'] <= payout6) & (pCheck['5'] <= payout7) |
                        (pCheck['5'] <= payout5) & (pCheck['4'] <= payout6) & (pCheck['6'] <= payout7) |
                        (pCheck['5'] <= payout5) & (pCheck['6'] <= payout6) & (pCheck['4'] <= payout7) |
                        (pCheck['6'] <= payout5) & (pCheck['5'] <= payout6) & (pCheck['4'] <= payout7) |
                        (pCheck['6'] <= payout5) & (pCheck['4'] <= payout6) & (pCheck['5'] <= payout7)]
        #Checking 5-7
        if len(pCheck) > 0:
            print("5-7 payouts good. Let's ride.")
            print("You should bet on this game!!")

        else:
            print("5-7 payout too low")
    else:
        print("1-4 payout too low")    
else:
    print("First and second payout too low")




 
###I am testing for only 4 bets down here 
           
def runSim4(seconddf,resultsdf,bet,money,payout):

    wins = []
    total = []
    games = []
    check = []
    money = money
    bet = bet
    totalBet = bet * 4

    for record in range(500,1500):
    
    
         i = 0
         diff = seconddf.iloc[record,1] - seconddf.iloc[record,2] #Postive means home is winning
         homeOrg = seconddf.iloc[record,1]
         awayOrg = seconddf.iloc[record,2]
         homefinal = resultsdf.iloc[record,1]
         awayfinal = resultsdf.iloc[record,2]
    
        
         if diff == 0: #Game is tied  
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 2
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 0
             away4 = awayOrg + 2
             #No goals

             
        ##ONE GOAL GAME
         if diff == 1: #Home is winning by 1
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 0
             away2 = awayOrg + 2
             #No goals
             home3 = homeOrg + 2
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 1
             #No goals

             
         if diff == -1: #Home is losing by 1
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 0
             #No goals
             home3 = homeOrg + 1
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 2
             #No goals
             #home5 = homeOrg + 1
             #away5 = awayOrg + 2
             #No goals
             #home6 = homeOrg + 2
             #away6 = awayOrg + 1
             #No goals
             #home7 = homeOrg + 1
             #away7 = awayOrg + 0
    
        ##TWO GOAL GAME
         if diff == 2: #Home is winning by 2
             #No goals
             home1 = homeOrg + 1
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 2
             away4 = awayOrg + 1
             #No goals

             
         if diff == -2: #Home is losing by 2
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 0
             #No goals
             home3 = homeOrg + 1
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 2
             #No goals

        ##THREE GOAL GAME
         if diff == 3: #Home is winning by 3
             #No goals
             home1 = homeOrg + 1
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 0
             away4 = awayOrg + 1
             #No goals

             
         if diff == -3: #Home is losing by 3
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 0
             #No goals

             
        ##FOUR GOAL GAME
         if diff >= 4: #Home is winning by 4 or more
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 0
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 1
             #No goals

             
         if diff <= -4: #Home is losing by 4 or more
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 0
             #No goals

     
        ##Determine results
         if diff != 1 and diff != 0:     
             if homefinal == home1 and awayfinal ==away1:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[0]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "1")
                i = 1
                
             if homefinal == home2 and awayfinal ==away2:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[1]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "2")
                i = 1
            
             if homefinal == home3 and awayfinal ==away3:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[2]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "3")
                i = 1
        
             if homefinal == home4 and awayfinal ==away4:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[3]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "4")
                i = 1
                
                
             if i == 0:
                #print("You lost money big dumb!!")
                #print("Loss. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money - totalBet
                #print(str(money))
                wins.append(0)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "Loss")
                #print("\n")
         #else:
             #print("SKIPPED BECAUSE DIFF WAS ONE")
             #print("\n")

    return money, wins, total    



ranges = np.array([0.00,0.5,1.0,1.5,2.00,2.5,3.0,3.5,4,5,6])
bets = np.array([3.00,3.00,4.00,5.00])
allBets = []
for constant in range(len(bets)):
    i = 0
    while(i < len(ranges)):
        currentConstant = bets[constant] + ranges[i]
        print("\n")
        print("Current Constant: " + str(currentConstant))
        constantIndex = np.where(bets == currentConstant)   
        newBetArray = bets.copy()
        newBetArray[constant] = currentConstant
        for bet in range(len(bets)):
            currentChange = bets[bet]
            itemindex = np.where(bets == currentChange)

            for itr in range(len(ranges)):
                newestBetArray = newBetArray.copy()
                newestBetArray = newestBetArray + ranges[itr]
                newestBetArray[constant] = currentConstant
                for itr in range(len(ranges)):
                    betArray = newestBetArray.copy()
                    change = ranges[itr]
                    newBet = currentChange + change
                    if bet != constant:
                        #print("New Bet Value: " + str(newBet))
                        betArray[bet] = newBet
                        betArrayList = betArray.tolist()
                        if betArrayList not in allBets:
                            allBets.append(betArrayList)
                            print(betArrayList)  
                        else:
                            print("ALREADY IN LIST")
        print("--------WE HAVE FINISHED AN ITERATION--------------")                    
        i = i + 1
   


##Determine the bet ranges that actually make money. We will want to bet on those.          
i = 0
moneys = []
moneyValues = []
for payout in allBets:
    i = i + 1
    x = runSim4(seconddf,resultsdf,25,2000,payout)
    print(i)
    print(x[0])
    print(payout)
    print("\n")
    if x[0] > 2000:
        print("You made money! It was:    " + str(x[0]))
        moneys.append(payout)
        moneyValues.append(x[0])

moneyDf = pd.DataFrame(moneys)
moneyDf["Money"] = moneyValues
moneyDf.to_csv("In_the_money - 4 Bets.csv")


##
##
##
####################3##
##This is for only 2 Bets
ranges = np.array([0.00,0.5,1.0,1.5,2.0,2.5])
bets = np.array([4.00,4.00])
allBets = []
for constant in range(len(bets)):
    i = 0
    while(i < len(ranges)):
        currentConstant = bets[constant] + ranges[i]
        print("\n")
        print("Current Constant: " + str(currentConstant))
        constantIndex = np.where(bets == currentConstant)   
        newBetArray = bets.copy()
        newBetArray[constant] = currentConstant
        for bet in range(len(bets)):
            currentChange = bets[bet]
            itemindex = np.where(bets == currentChange)

            for itr in range(len(ranges)):
                newestBetArray = newBetArray.copy()
                newestBetArray = newestBetArray + ranges[itr]
                newestBetArray[constant] = currentConstant
                for itr in range(len(ranges)):
                    betArray = newestBetArray.copy()
                    change = ranges[itr]
                    newBet = currentChange + change
                    if bet != constant:
                        #print("New Bet Value: " + str(newBet))
                        betArray[bet] = newBet
                        betArrayList = betArray.tolist()
                        if betArrayList not in allBets:
                            allBets.append(betArrayList)
                            print(betArrayList)  
                        else:
                            print("ALREADY IN LIST")
        print("--------WE HAVE FINISHED AN ITERATION--------------")                    
        i = i + 1
        
        
def runSim2(seconddf,resultsdf,bet,money,payout):

    wins = []
    total = []
    games = []
    check = []
    money = money
    bet = bet
    totalBet = bet * 2

    for record in range(500,1500):
    
    
         i = 0
         diff = seconddf.iloc[record,1] - seconddf.iloc[record,2] #Postive means home is winning
         homeOrg = seconddf.iloc[record,1]
         awayOrg = seconddf.iloc[record,2]
         homefinal = resultsdf.iloc[record,1]
         awayfinal = resultsdf.iloc[record,2]
    
        
         if diff == 0: #Game is tied  
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals


             
        ##ONE GOAL GAME
         if diff == 1: #Home is winning by 1
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 0
             away2 = awayOrg + 2
             #No goals


             
         if diff == -1: #Home is losing by 1
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 0
             away2 = awayOrg + 2
             #No goals

    
        ##TWO GOAL GAME
         if diff == 2: #Home is winning by 2
             #No goals
             home1 = homeOrg + 1
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals

             
         if diff == -2: #Home is losing by 2
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 0
             #No goals


        ##THREE GOAL GAME
         if diff == 3: #Home is winning by 3
             #No goals
             home1 = homeOrg + 1
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals


             
         if diff == -3: #Home is losing by 3
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals

             
        ##FOUR GOAL GAME
         if diff >= 4: #Home is winning by 4 or more
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 0
             #No goals


             
         if diff <= -4: #Home is losing by 4 or more
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals


     
        ##Determine results
         if diff != 1 and diff != 0:     
             if homefinal == home1 and awayfinal ==away1:
                print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[0]) + bet) - totalBet
                print(str(money))
                print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "1")
                i = 1
                
             if homefinal == home2 and awayfinal ==away2:
                print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[1]) + bet) - totalBet
                print(str(money))
                print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "2")
                i = 1
            
                
                
             if i == 0:
                print("You lost money big dumb!!")
                print("Loss. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money - totalBet
                print(str(money))
                wins.append(0)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "Loss")
                print("\n")
         #else:
             #print("SKIPPED BECAUSE DIFF WAS ONE")
             #print("\n")

    return money, wins, total    

i = 0
moneys = []
moneyValues = []
for payout in allBets:
    i = i + 1
    x = runSim2(seconddf,resultsdf,25,2000,payout)
    print(i)
    print(x[0])
    print(payout)
    print("\n")
    if x[0] > 2000:
        print("You made money! It was:    " + str(x[0]))
        moneys.append(payout)
        moneyValues.append(x[0])

moneyDf = pd.DataFrame(moneys)
moneyDf["Money"] = moneyValues
moneyDf.to_csv("In_the_money - 2 Bets.csv")



##There is a lot going on above. I am going to take lines 1-189 where we got the data and combine into one df
##I am going to select a random sample of 1000 games and see how often a certain payout is profitable in the sample
##I want to do this with 1 bet, 2 bets, 3 bets and 4 bets

combined = pd.concat([resultsdf,seconddf],axis=1)


    

#The below methods only uses the combined df (gamesdf) unlike the previous versions of this method above


###########################
##This is for only 1 Bet##
###########################
def runSimSample1(gamesdf,bet,money,payout):

    wins = []
    total = []
    check = []
    money = money
    bet = bet
    totalBet = bet

    for record in range(len(gamesdf)):
    
    
         i = 0
         diff = gamesdf.iloc[record,6] - gamesdf.iloc[record,7] #Postive means home is winning
         homeOrg = gamesdf.iloc[record,6]
         awayOrg = gamesdf.iloc[record,7]
         homefinal = gamesdf.iloc[record,1]
         awayfinal = gamesdf.iloc[record,2]
    
        
         if diff == 0: #Game is tied  
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0



             
        ##ONE GOAL GAME
         if diff == 1: #Home is winning by 1
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1



             
         if diff == -1: #Home is losing by 1
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals

    
        ##TWO GOAL GAME
         if diff == 2: #Home is winning by 2
             #No goals
             home1 = homeOrg + 1
             away1 = awayOrg + 0
             #No goal

             
         if diff == -2: #Home is losing by 2
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals


        ##THREE GOAL GAME
         if diff == 3: #Home is winning by 3
             #No goals
             home1 = homeOrg + 1
             away1 = awayOrg + 0
             #No goals



             
         if diff == -3: #Home is losing by 3
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals


             
        ##FOUR GOAL GAME
         if diff >= 4: #Home is winning by 4 or more
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals



             
         if diff <= -4: #Home is losing by 4 or more
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0



     
        ##Determine results
         if diff != 1 and diff != 0:     
             if homefinal == home1 and awayfinal ==away1:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(gamesdf.iloc[record,0]) + " " + "1")
                i = 1
                

                
             if i == 0:
                #print("You lost money big dumb!!")
                #print("Loss. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money - totalBet
                #print(str(money))
                wins.append(0)
                total.append(1)
                check.append(str(gamesdf.iloc[record,0]) + " " + "Loss")
                #print("\n")
         #else:
             #print("SKIPPED BECAUSE DIFF WAS ONE")
             #print("\n")

    return money, wins, total    


def runSimSample2(gamesdf,bet,money,payout):

    wins = []
    total = []
    check = []
    money = money
    bet = bet
    totalBet = bet * 2

    for record in range(len(gamesdf)):
    
    
         i = 0
         diff = gamesdf.iloc[record,6] - gamesdf.iloc[record,7] #Postive means home is winning
         homeOrg = gamesdf.iloc[record,6]
         awayOrg = gamesdf.iloc[record,7]
         homefinal = gamesdf.iloc[record,1]
         awayfinal = gamesdf.iloc[record,2]
    
        
         if diff == 0: #Game is tied  
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals


             
        ##ONE GOAL GAME
         if diff == 1: #Home is winning by 1
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 0
             away2 = awayOrg + 2
             #No goals


             
         if diff == -1: #Home is losing by 1
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 0
             away2 = awayOrg + 2
             #No goals

    
        ##TWO GOAL GAME
         if diff == 2: #Home is winning by 2
             #No goals
             home1 = homeOrg + 1
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals

             
         if diff == -2: #Home is losing by 2
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 0
             #No goals


        ##THREE GOAL GAME
         if diff == 3: #Home is winning by 3
             #No goals
             home1 = homeOrg + 1
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals


             
         if diff == -3: #Home is losing by 3
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals

             
        ##FOUR GOAL GAME
         if diff >= 4: #Home is winning by 4 or more
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 0
             #No goals


             
         if diff <= -4: #Home is losing by 4 or more
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals


     
        ##Determine results
         if diff != 1 and diff != 0:     
             if homefinal == home1 and awayfinal ==away1:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[0]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(gamesdf.iloc[record,0]) + " " + "1")
                i = 1
                
             if homefinal == home2 and awayfinal ==away2:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[1]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(gamesdf.iloc[record,0]) + " " + "2")
                i = 1
            
                
                
             if i == 0:
                #print("You lost money big dumb!!")
                #print("Loss. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money - totalBet
                #print(str(money))
                wins.append(0)
                total.append(1)
                check.append(str(gamesdf.iloc[record,0]) + " " + "Loss")
                #print("\n")
         #else:
             #print("SKIPPED BECAUSE DIFF WAS ONE")
             #print("\n")

    return money, wins, total    

############
###3 Bets###
############
def runSimSample3(gamesdf,bet,money,payout):

    wins = []
    total = []
    check = []
    money = money
    bet = bet
    totalBet = bet * 3

    for record in range(len(gamesdf)):
    
    
         i = 0
         diff = gamesdf.iloc[record,6] - gamesdf.iloc[record,7] #Postive means home is winning
         homeOrg = gamesdf.iloc[record,6]
         awayOrg = gamesdf.iloc[record,7]
         homefinal = gamesdf.iloc[record,1]
         awayfinal = gamesdf.iloc[record,2]
    
        
         if diff == 0: #Game is tied  
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 2
             away3 = awayOrg + 0
             #No goals
             #home4 = homeOrg + 0
             #away4 = awayOrg + 2
             #No goals

             
        ##ONE GOAL GAME
         if diff == 1: #Home is winning by 1
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 0
             away2 = awayOrg + 2
             #No goals
             home3 = homeOrg + 2
             away3 = awayOrg + 0
             #No goals
             #home4 = homeOrg + 1
             #away4 = awayOrg + 1
             #No goals

             
         if diff == -1: #Home is losing by 1
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 0
             #No goals
             home3 = homeOrg + 1
             away3 = awayOrg + 1
             #No goals
             #home4 = homeOrg + 1
             #away4 = awayOrg + 2
             #No goals
             #home5 = homeOrg + 1
             #away5 = awayOrg + 2
             #No goals
             #home6 = homeOrg + 2
             #away6 = awayOrg + 1
             #No goals
             #home7 = homeOrg + 1
             #away7 = awayOrg + 0
    
        ##TWO GOAL GAME
         if diff == 2: #Home is winning by 2
             #No goals
             home1 = homeOrg + 1
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 1
             #No goals
             #home4 = homeOrg + 2
             #away4 = awayOrg + 1
             #No goals

             
         if diff == -2: #Home is losing by 2
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 0
             #No goals
             home3 = homeOrg + 1
             away3 = awayOrg + 1
             #No goals
             #home4 = homeOrg + 1
             #away4 = awayOrg + 2
             #No goals

        ##THREE GOAL GAME
         if diff == 3: #Home is winning by 3
             #No goals
             home1 = homeOrg + 1
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 0
             #No goals
             #home4 = homeOrg + 0
             #away4 = awayOrg + 1
             #No goals

             
         if diff == -3: #Home is losing by 3
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 0
             #No goals
             #home4 = homeOrg + 1
             #away4 = awayOrg + 0
             #No goals

             
        ##FOUR GOAL GAME
         if diff >= 4: #Home is winning by 4 or more
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 0
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 1
             #No goals
             #home4 = homeOrg + 1
             #away4 = awayOrg + 1
             #No goals

             
         if diff <= -4: #Home is losing by 4 or more
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 1
             #No goals
             #home4 = homeOrg + 1
             #away4 = awayOrg + 0
             #No goals


     
        ##Determine results
         if diff != 1 and diff != 0:     
             if homefinal == home1 and awayfinal ==away1:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[0]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(gamesdf.iloc[record,0]) + " " + "1")
                i = 1
                
             if homefinal == home2 and awayfinal ==away2:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[1]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(gamesdf.iloc[record,0]) + " " + "2")
                i = 1
            
             if homefinal == home3 and awayfinal ==away3:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[2]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "3")
                i = 1
                
             if i == 0:
                #print("You lost money big dumb!!")
                #print("Loss. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money - totalBet
                #print(str(money))
                wins.append(0)
                total.append(1)
                check.append(str(gamesdf.iloc[record,0]) + " " + "Loss")
                #print("\n")
         #else:
             #print("SKIPPED BECAUSE DIFF WAS ONE")
             #print("\n")

    return money, wins, total


############
###4 Bets###
############
def runSimSample4(gamesdf,bet,money,payout):

    wins = []
    total = []
    check = []
    money = money
    bet = bet
    totalBet = bet * len(payout)

    for record in range(len(gamesdf)):
    
    
         i = 0
         diff = gamesdf.iloc[record,6] - gamesdf.iloc[record,7] #Postive means home is winning
         homeOrg = gamesdf.iloc[record,6]
         awayOrg = gamesdf.iloc[record,7]
         homefinal = gamesdf.iloc[record,1]
         awayfinal = gamesdf.iloc[record,2]
    
        
         if diff == 0: #Game is tied  
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 2
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 0
             away4 = awayOrg + 2
             #No goals

             
        ##ONE GOAL GAME
         if diff == 1: #Home is winning by 1
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 0
             away2 = awayOrg + 2
             #No goals
             home3 = homeOrg + 2
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 1
             #No goals

             
         if diff == -1: #Home is losing by 1
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 0
             #No goals
             home3 = homeOrg + 1
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 2
             #No goals
             #home5 = homeOrg + 1
             #away5 = awayOrg + 2
             #No goals
             #home6 = homeOrg + 2
             #away6 = awayOrg + 1
             #No goals
             #home7 = homeOrg + 1
             #away7 = awayOrg + 0
    
        ##TWO GOAL GAME
         if diff == 2: #Home is winning by 2
             #No goals
             home1 = homeOrg + 1
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 2
             away4 = awayOrg + 1
             #No goals

             
         if diff == -2: #Home is losing by 2
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 0
             #No goals
             home3 = homeOrg + 1
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 2
             #No goals

        ##THREE GOAL GAME
         if diff == 3: #Home is winning by 3
             #No goals
             home1 = homeOrg + 1
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 0
             away4 = awayOrg + 1
             #No goals

             
         if diff == -3: #Home is losing by 3
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 0
             #No goals

             
        ##FOUR GOAL GAME
         if diff >= 4: #Home is winning by 4 or more
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 0
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 1
             #No goals

             
         if diff <= -4: #Home is losing by 4 or more
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 0
             #No goals


     
        ##Determine results
         if diff != 1 and diff != 0:     
             if homefinal == home1 and awayfinal ==away1:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[0]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(gamesdf.iloc[record,0]) + " " + "1")
                i = 1
                
             if homefinal == home2 and awayfinal ==away2:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[1]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(gamesdf.iloc[record,0]) + " " + "2")
                i = 1
            
             if homefinal == home3 and awayfinal ==away3:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[2]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "3")
                i = 1
                
             if homefinal == home4 and awayfinal ==away4:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[3]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "3")
                i = 1
                
             if i == 0:
                #print("You lost money big dumb!!")
                #print("Loss. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money - totalBet
                #print(str(money))
                wins.append(0)
                total.append(1)
                check.append(str(gamesdf.iloc[record,0]) + " " + "Loss")
                #print("\n")
         #else:
             #print("SKIPPED BECAUSE DIFF WAS ONE")
             #print("\n")

    return money, wins, total

############
###5 Bets###
############
def runSimSample5(gamesdf,bet,money,payout):

    wins = []
    total = []
    check = []
    money = money
    bet = bet
    totalBet = bet * len(payout)

    for record in range(len(gamesdf)):
    
    
         i = 0
         diff = gamesdf.iloc[record,6] - gamesdf.iloc[record,7] #Postive means home is winning
         homeOrg = gamesdf.iloc[record,6]
         awayOrg = gamesdf.iloc[record,7]
         homefinal = gamesdf.iloc[record,1]
         awayfinal = gamesdf.iloc[record,2]
    
        
         if diff == 0: #Game is tied  
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 2
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 0
             away4 = awayOrg + 2
             #No goals
             home5 = homeOrg + 3
             away5 = awayOrg + 1
             #No goals
             #home6 = homeOrg + 1
             #away6 = awayOrg + 3
             #No goals
             #home7 = homeOrg + 2
             #away7 = awayOrg + 2
             
        ##ONE GOAL GAME
         if diff == 1: #Home is winning by 1
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 0
             away2 = awayOrg + 2
             #No goals
             home3 = homeOrg + 2
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 1
             away5 = awayOrg + 2
             #No goals
             #home6 = homeOrg + 2
             #away6 = awayOrg + 1
             #No goals
             #home7 = homeOrg + 1
             #away7 = awayOrg + 0
             
         if diff == -1: #Home is losing by 1
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 0
             away2 = awayOrg + 2
             #No goals
             home3 = homeOrg + 2
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 1
             away5 = awayOrg + 2
             #No goals
             #home6 = homeOrg + 2
             #away6 = awayOrg + 1
             #No goals
             #home7 = homeOrg + 1
             #away7 = awayOrg + 0
    
        ##TWO GOAL GAME
         if diff == 2: #Home is winning by 2
             #No goals
             home1 = homeOrg + 1
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 2
             away2 = awayOrg + 0
             #No goals
             home3 = homeOrg + 1
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 2
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 0
             away5 = awayOrg + 2
             #No goals
             #home6 = homeOrg + 0
             #away6 = awayOrg + 1
             #No goals
             #home7 = homeOrg + 2
             #away7 = awayOrg + 2
             
         if diff == -2: #Home is losing by 2
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 2
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 2
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 2
             away5 = awayOrg + 0
             #No goals
             #home6 = homeOrg + 1
             #away6 = awayOrg + 0
             #No goals
             #home7 = homeOrg + 2
             #away7 = awayOrg + 1
             
        ##THREE GOAL GAME
         if diff == 3: #Home is winning by 3
             #No goals
             home1 = homeOrg + 1
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 2
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 2
             away5 = awayOrg + 2
             #No goals
             #home6 = homeOrg + 0
             #away6 = awayOrg + 1
             #No goals
             #home7 = homeOrg + 0
             #away7 = awayOrg + 2
             
         if diff == -3: #Home is losing by 3
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 2
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 1
             away5 = awayOrg + 2
             #No goals
             #home6 = homeOrg + 1
             #away6 = awayOrg + 0
             #No goals
             #home7 = homeOrg + 2
             #away7 = awayOrg + 2
             
        ##FOUR GOAL GAME
         if diff >= 4: #Home is winning by 4 or more
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 0
             #No goals
             home3 = homeOrg + 1
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 0
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 2
             away5 = awayOrg + 1
             #No goals
             #home6 = homeOrg + 1
             #away6 = awayOrg + 2
             #No goals
             #home7 = homeOrg + 2
             #away7 = awayOrg + 0
             
         if diff <= -4: #Home is losing by 4 or more
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 2
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 0
             away4 = awayOrg + 2
             #No goals
             home5 = homeOrg + 1
             away5 = awayOrg + 0
             #No goals
             #home6 = homeOrg + 1
             #away6 = awayOrg + 2
             #No goals
             #home7 = homeOrg + 2
             #away7 = awayOrg + 0


     
        ##Determine results
         if diff != 1 and diff != 0:     
             if homefinal == home1 and awayfinal ==away1:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[0]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(gamesdf.iloc[record,0]) + " " + "1")
                i = 1
                
             if homefinal == home2 and awayfinal ==away2:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[1]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(gamesdf.iloc[record,0]) + " " + "2")
                i = 1
            
             if homefinal == home3 and awayfinal ==away3:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[2]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "3")
                i = 1
                
             if homefinal == home4 and awayfinal ==away4:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[3]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "4")
                i = 1
                
             if homefinal == home5 and awayfinal ==away5:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[4]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "5")
                i = 1
                
             if i == 0:
                #print("You lost money big dumb!!")
                #print("Loss. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money - totalBet
                #print(str(money))
                wins.append(0)
                total.append(1)
                check.append(str(gamesdf.iloc[record,0]) + " " + "Loss")
                #print("\n")
         #else:
             #print("SKIPPED BECAUSE DIFF WAS ONE")
             #print("\n")

    return money, wins, total


############
###6 Bets###
############
def runSimSample6(gamesdf,bet,money,payout):

    wins = []
    total = []
    check = []
    money = money
    bet = bet
    totalBet = bet * len(payout)

    for record in range(len(gamesdf)):
    
    
         i = 0
         diff = gamesdf.iloc[record,6] - gamesdf.iloc[record,7] #Postive means home is winning
         homeOrg = gamesdf.iloc[record,6]
         awayOrg = gamesdf.iloc[record,7]
         homefinal = gamesdf.iloc[record,1]
         awayfinal = gamesdf.iloc[record,2]
    
        
         if diff == 0: #Game is tied  
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 2
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 0
             away4 = awayOrg + 2
             #No goals
             home5 = homeOrg + 3
             away5 = awayOrg + 1
             #No goals
             home6 = homeOrg + 1
             away6 = awayOrg + 3
             #No goals
             #home7 = homeOrg + 2
             #away7 = awayOrg + 2
             
        ##ONE GOAL GAME
         if diff == 1: #Home is winning by 1
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 0
             away2 = awayOrg + 2
             #No goals
             home3 = homeOrg + 2
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 1
             away5 = awayOrg + 2
             #No goals
             home6 = homeOrg + 2
             away6 = awayOrg + 1
             #No goals
             #home7 = homeOrg + 1
             #away7 = awayOrg + 0
             
         if diff == -1: #Home is losing by 1
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 0
             away2 = awayOrg + 2
             #No goals
             home3 = homeOrg + 2
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 1
             away5 = awayOrg + 2
             #No goals
             home6 = homeOrg + 2
             away6 = awayOrg + 1
             #No goals
             #home7 = homeOrg + 1
             #away7 = awayOrg + 0
    
        ##TWO GOAL GAME
         if diff == 2: #Home is winning by 2
             #No goals
             home1 = homeOrg + 1
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 2
             away2 = awayOrg + 0
             #No goals
             home3 = homeOrg + 1
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 2
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 0
             away5 = awayOrg + 2
             #No goals
             home6 = homeOrg + 0
             away6 = awayOrg + 1
             #No goals
             #home7 = homeOrg + 2
             #away7 = awayOrg + 2
             
         if diff == -2: #Home is losing by 2
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 2
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 2
             #No goals
             home4 = homeOrg + 1
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 2
             away5 = awayOrg + 0
             #No goals
             home6 = homeOrg + 1
             away6 = awayOrg + 0
             #No goals
             #home7 = homeOrg + 2
             #away7 = awayOrg + 1
             
        ##THREE GOAL GAME
         if diff == 3: #Home is winning by 3
             #No goals
             home1 = homeOrg + 1
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 2
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 2
             away5 = awayOrg + 2
             #No goals
             home6 = homeOrg + 0
             away6 = awayOrg + 1
             #No goals
             #home7 = homeOrg + 0
             #away7 = awayOrg + 2
             
         if diff == -3: #Home is losing by 3
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 0
             away3 = awayOrg + 0
             #No goals
             home4 = homeOrg + 2
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 1
             away5 = awayOrg + 2
             #No goals
             home6 = homeOrg + 1
             away6 = awayOrg + 0
             #No goals
             #home7 = homeOrg + 2
             #away7 = awayOrg + 2
             
        ##FOUR GOAL GAME
         if diff >= 4: #Home is winning by 4 or more
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 0
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 0
             #No goals
             home3 = homeOrg + 1
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 0
             away4 = awayOrg + 1
             #No goals
             home5 = homeOrg + 2
             away5 = awayOrg + 1
             #No goals
             home6 = homeOrg + 1
             away6 = awayOrg + 2
             #No goals
             #home7 = homeOrg + 2
             #away7 = awayOrg + 0
             
         if diff <= -4: #Home is losing by 4 or more
             #No goals
             home1 = homeOrg + 0
             away1 = awayOrg + 1
             #No goals
             home2 = homeOrg + 1
             away2 = awayOrg + 1
             #No goals
             home3 = homeOrg + 2
             away3 = awayOrg + 1
             #No goals
             home4 = homeOrg + 0
             away4 = awayOrg + 2
             #No goals
             home5 = homeOrg + 1
             away5 = awayOrg + 0
             #No goals
             home6 = homeOrg + 1
             away6 = awayOrg + 2
             #No goals
             #home7 = homeOrg + 2
             #away7 = awayOrg + 0


     
        ##Determine results
         if diff != 1 and diff != 0:     
             if homefinal == home1 and awayfinal ==away1:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[0]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(gamesdf.iloc[record,0]) + " " + "1")
                i = 1
                
             if homefinal == home2 and awayfinal ==away2:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[1]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(gamesdf.iloc[record,0]) + " " + "2")
                i = 1
            
             if homefinal == home3 and awayfinal ==away3:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[2]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "3")
                i = 1
                
             if homefinal == home4 and awayfinal ==away4:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[3]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "4")
                i = 1
                
             if homefinal == home5 and awayfinal ==away5:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[4]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "5")
                i = 1

             if homefinal == home6 and awayfinal ==away6:
                #print("Win. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money + ((bet * payout[4]) + bet) - totalBet
                #print(str(money))
                #print("\n")
                wins.append(1)
                total.append(1)
                check.append(str(seconddf.iloc[record,0]) + " " + "5")
                i = 1

                
             if i == 0:
                #print("You lost money big dumb!!")
                #print("Loss. Original Score: " + str(homeOrg) + " to " + str(awayOrg) + ". Final Score: " + str(homefinal) + " to " + str(awayfinal))
                money = money - totalBet
                #print(str(money))
                wins.append(0)
                total.append(1)
                check.append(str(gamesdf.iloc[record,0]) + " " + "Loss")
                #print("\n")
         #else:
             #print("SKIPPED BECAUSE DIFF WAS ONE")
             #print("\n")

    return money, wins, total


##Get bets for 1 bet

###1 Bets####
###########################
##This is for only 1 Bets##
###########################
allBets = np.array([1.50,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0])



##Run Simulation
payoutRecord1 = dict()

for el in allBets:
    payoutRecord1[str(el)] = 0

for i in range(50):
    
    sampleGames = combined.sample(n=1000)
    
    i = 0
    moneyPayouts = []
    moneyValues = []
    for payout in allBets:
        i = i + 1
        x = runSimSample1(sampleGames,25,2000,payout)
        #print(i)
        #print(x[0])
        #print(payout)
        #print("\n")
        if x[0] > 2000:
            print("You made money! It was:    " + str(x[0]))
            moneyPayouts.append(payout)
            moneyValues.append(x[0])
            payoutRecord1[str(payout)] = payoutRecord1[str(payout)] + 1
    
    moneyDf = pd.DataFrame(moneyPayouts)
    moneyDf["Money"] = moneyValues

{k: v for k, v in sorted(payoutRecord1.items(), key=lambda item: item[1])}



###2 Bets####
###########################
##This is for only 2 Bets##
###########################
betValues = [2,2,2.5,2.5,3,3,3.5,3.5,4,4,4.5,4.5,5,5,5.5,5.5,6,6,6.5,6.5,7,7,7.5,7.5,8,8,9,9,10,10]
allBets = list(itertools.permutations(betValues, 2))

finalBets = set(allBets)
allBets = list(finalBets)


payoutRecord2 = dict()

for el in allBets:
    payoutRecord2[str(el)] = 0

j = 1
for i in range(50):
    
    sampleGames = combined.sample(n=1000)
    i = 0
    moneyPayouts = []
    moneyValues = []
    for payout in allBets:
        i = i + 1
        x = runSimSample2(sampleGames,25,2000,payout)
        #print(i)
        #print(x[0])
        #print(payout)
        #print("\n")
        if x[0] > 2000:
            #print("You made money! It was:    " + str(x[0]))
            #print("The payout was " + str(payout))
            moneyPayouts.append(payout)
            moneyValues.append(x[0])
            payoutRecord2[str(payout)] = payoutRecord2[str(payout)] + 1
    
    print("End iteration: " + str(j))
    j = j+1

    
{k: v for k, v in sorted(payoutRecord2.items(), key=lambda item: item[1])}


###3 Bets####
###########################
##This is for only 3 Bets##
###########################
betValues = [2.5,2.5,2.5,3,3,3,3.5,3.5,3.5,4,4,4,4.5,4.5,4.5,5,5,5,5.5,5.5,5.5,6,6,6,7,7,7,8,8,8,9,9,9,10,10,10,11,11,11]
allBets = list(itertools.permutations(betValues, 3))

finalBets = set(allBets)
allBets = list(finalBets)


payoutRecord3 = dict()

for el in allBets:
    payoutRecord3[str(el)] = 0

j = 1
for i in range(50):
    
    sampleGames = combined.sample(n=1000)
    
    i = 0
    moneyPayouts = []
    moneyValues = []
    for payout in allBets:
        i = i + 1
        x = runSimSample3(sampleGames,25,2000,payout)
        #print(i)
        #print(x[0])
        #print(payout)
        #print("\n")
        if x[0] > 2000:
            #print("You made money! It was:    " + str(x[0]))
            #print("The payout was " + str(payout))
            moneyPayouts.append(payout)
            moneyValues.append(x[0])
            payoutRecord3[str(payout)] = payoutRecord3[str(payout)] + 1
    print("End iteration: " + str(j))
    j = j+1
    

    
{k: v for k, v in sorted(payoutRecord3.items(), key=lambda item: item[1])}


###4 Bets####
###########################
##This is for only 4 Bets##
###########################
betValues = [3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,10,10,10,10,12,12,12,12]
allBets = list(itertools.permutations(betValues, 4))

finalBets = set(allBets)
allBets = list(finalBets)

payoutRecord4 = dict()

for el in allBets:
    payoutRecord4[str(el)] = 0

j = 1
for i in range(50):
    
    sampleGames = combined.sample(n=1000)
    
    i = 0
    moneyPayouts = []
    moneyValues = []
    for payout in allBets:
        i = i + 1
        x = runSimSample4(sampleGames,25,2000,payout)
        #print(i)
        #print(x[0])
        #print(payout)
        #print("\n")
        if x[0] > 2000:
            #print("You made money! It was:    " + str(x[0]))
            #print("The payout was " + str(payout))
            moneyPayouts.append(payout)
            moneyValues.append(x[0])
            payoutRecord4[str(payout)] = payoutRecord4[str(payout)] + 1
    print("End iteration: " + str(j))
    j = j+1
    
    
{k: v for k, v in sorted(payoutRecord4.items(), key=lambda item: item[1])}


###5 Bets####
###########################
##This is for only 5 Bets##
###########################

betValues = [3,3,3,3,3,4,4,4,4,4,5,5,5,5,5,6,6,6,6,6,7,7,7,7,7,8,8,8,8,8,10,10,10,10,10,12,12,12,12,12]
allBets = list(itertools.permutations(betValues, 5))

finalBets = set(allBets)
allBets = list(finalBets)

payoutRecord5 = dict()

for el in allBets:
    payoutRecord5[str(el)] = 0

j = 1
for i in range(50):
    
    sampleGames = combined.sample(n=1000)
    
    i = 0
    moneyPayouts = []
    moneyValues = []
    for payout in allBets:
        i = i + 1
        x = runSimSample5(sampleGames,25,2000,payout)
        #print(i)
        #print(x[0])
        #print(payout)
        #print("\n")
        if x[0] > 2000:
            #print("You made money! It was:    " + str(x[0]))
            #print("The payout was " + str(payout))
            moneyPayouts.append(payout)
            moneyValues.append(x[0])
            payoutRecord5[str(payout)] = payoutRecord5[str(payout)] + 1
    print("End iteration: " + str(j))
    j = j+1    

    
{k: v for k, v in sorted(payoutRecord5.items(), key=lambda item: item[1])}



###6 Bets####
###########################
##This is for only 6 Bets##
###########################
betValues = [4,4,4,4,4,4,5,5,5,5,5,5,7,7,7,7,7,7,10,10,10,10,10,10]
allBets = list(itertools.permutations(betValues, 6))

betValues2 = [4,4,4,4,4,4,5,5,5,5,5,5,6,6,6,6,6,6,10,10,10,10,10,10]
allBets2 = list(itertools.permutations(betValues2, 6))

betValues3 = [4,4,4,4,4,4,5,5,5,5,5,5,8,8,8,8,8,8,9,9,9,9,9,9]
allBets3 = list(itertools.permutations(betValues3, 6))

betValues3 = [4,4,5,5,6,6,7,7,8,8,9,9,10,10,15,15]
allBets3 = list(itertools.permutations(betValues3, 6))

finalBets = set(allBets)
allBets = list(finalBets)

finalBets2 = set(allBets2)
allBets2 = list(finalBets2)

finalBets3 = set(allBets3)
allBets3 = list(finalBets3)

for bet in allBets2: allBets.append(bet)
for bet in allBets3: allBets.append(bet)

payoutRecord6 = dict()

for el in allBets:
    payoutRecord6[str(el)] = 0

j = 1
for i in range(50):
    
    sampleGames = combined.sample(n=1000)
    
    i = 0
    moneyPayouts = []
    moneyValues = []
    for payout in allBets:
        i = i + 1
        x = runSimSample6(sampleGames,25,2000,payout)
        #print(i)
        #print(x[0])
        #print(payout)
        #print("\n")
        if x[0] > 2000:
            print("You made money! It was:    " + str(x[0]))
            print("The payout was " + str(payout))
            moneyPayouts.append(payout)
            moneyValues.append(x[0])
            payoutRecord6[str(payout)] = payoutRecord6[str(payout)] + 1
    print("End iteration: " + str(j))
    j = j+1    
    
{k: v for k, v in sorted(payoutRecord6.items(), key=lambda item: item[1])}



###Write data to csv files

with open('1 Bet Data.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in payoutRecord1.items():
       writer.writerow([key, value])
       
       
with open('2 Bet Data.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in payoutRecord2.items():
       writer.writerow([key, value])

       
with open('3 Bet Data.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in payoutRecord3.items():
       writer.writerow([key, value])
       
with open('4 Bet Data.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in payoutRecord4.items():
       writer.writerow([key, value])
       
with open('5 Bet Data.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in payoutRecord5.items():
       writer.writerow([key, value])      
       
with open('6 Bet Data.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in payoutRecord6.items():
       writer.writerow([key, value])


def runAnalysis(odds1,odds2,odds3,odds4,odds5,line,bet):

    ####################
    ##Analysis of Bets##
    ####################
    oneResults = pd.read_csv('1 Bet Data - Refined.csv')
    twoResults = pd.read_csv('2 Bet Data - Refined.csv')
    threeResults = pd.read_csv('3 Bet Data - Refined.csv')
    fourResults = pd.read_csv('4 Bet Data - Refined.csv')
    fiveResults = pd.read_csv('5 Bet Data - Refined.csv')
    #sixResults = pd.read_csv('6 Bet Data - Refined.csv')
    
    
    odds1 = odds1
    odds2 = odds2
    odds3 = odds3
    odds4 = odds4
    odds5 = odds5
    #odds6 = 5.68
    

    ev = expectedValue(odds1, odds2, odds3, odds4, odds5, line, bet)  
    ev1 = ev[0]
    ev2 = ev[1]
    ev3 = ev[2]
    ev4 = ev[3]
    ev5 = ev[4]
    #Look for 1 bet##
    ones = np.array(oneResults['Odds 1'])
    
    current1 = 0
    currentDiff = 100
    
    for odd in ones:
        diff = odds1 - odd
        if diff <= currentDiff and odd <= odds1:
            currentDiff = diff
            current1 = odd
            
    match1 = oneResults[(oneResults['Odds 1'] == current1)]
    result1 = match1.iloc[0,-1]
    percent1 = round(result1 / 50, 4) * 100
    
    
    print("The closet odds for 1 bet was " + str(current1) + " which resulted in: " + str(result1) + " wins (" + str(percent1) + "%)")
    print("The exptected value is " + str(ev1))
    print("\n") 
    
    ##################
    #Look for 2 bets##
    ##################
    
    ones = np.array(twoResults['Odds 1'])
    twos = np.array(twoResults['Odds 2'])
    
    current1 = 0
    current2 = 0
    currentDiff = 100
    
    for odd in ones:
        diff = odds1 - odd
        if diff <= currentDiff and odd <= odds1:
            currentDiff = diff
            current1 = odd
            
    if current1 == 0:
        current1 = ones.min()
    
    
    currentDiff = 100
            
    for odd in twos:
        diff = odds2 - odd
        if diff <= currentDiff and odd <= odds2:
            currentDiff = diff
            current2 = odd
    
    
    if current2 == 0:
        current2 = twos.min()
    
    
    match2 = twoResults[(twoResults['Odds 1'] == current1) & (twoResults['Odds 2'] == current2)]
    result2 = match2.iloc[0,-1]
    percent2 = round(result2 / 50, 4) * 100
    
    print("The closet odds for 2 bets was " + str(match2.iloc[0,0]) + ", " + str(match2.iloc[0,1]) + " which resulted in: " + str(result2) + " wins (" + str(percent2) + "%)")
    print("The exptected value is " + str(ev2))
    print("\n")   
    
    
    ##################
    #Look for 3 bets##
    ##################
    
    ones = np.array(threeResults['Odds 1'])
    twos = np.array(threeResults['Odds 2'])
    threes = np.array(threeResults['Odds 3'])
    
    current1 = 0
    current2 = 0
    current3 = 0
    currentDiff = 100
    
    for odd in ones:
        diff = odds1 - odd
        if diff <= currentDiff and odd <= odds1:
            currentDiff = diff
            current1 = odd
            
    if current1 == 0:
        current1 = ones.min()
    
    
    currentDiff = 100
            
    for odd in twos:
        diff = odds2 - odd
        if diff <= currentDiff and odd <= odds2:
            currentDiff = diff
            current2 = odd
    
    
    if current2 == 0:
        current2 = twos.min()
        
    
    currentDiff = 100
            
    for odd in threes:
        diff = odds3 - odd
        if diff <= currentDiff and odd <= odds3:
            currentDiff = diff
            current3 = odd
    
    
    if current3 == 0:
        current3 = threes.min()
    
    
    match3 = threeResults[(threeResults['Odds 1'] == current1) & (threeResults['Odds 2'] == current2) & (threeResults['Odds 3'] == current3)]
    result3 = match3.iloc[0,-1]
    percent3 = round(result3 / 50, 4) * 100
    
    print("The closet odds for 3 bets was " + str(match3.iloc[0,0]) + ", " + str(match3.iloc[0,1]) + ", " + str(match3.iloc[0,2]) + " which resulted in: " + str(result3) + " wins (" + str(percent3) + "%)")
    print("The exptected value is " + str(ev3))
    print("\n")   
    
    
    ##################
    #Look for 4 bets##
    ##################
    
    ones = np.array(fourResults['Odds 1'])
    twos = np.array(fourResults['Odds 2'])
    threes = np.array(fourResults['Odds 3'])
    fours = np.array(fourResults['Odds 4'])
    
    current1 = 0
    current2 = 0
    current3 = 0
    current4 = 0
    currentDiff = 100
    
    for odd in ones:
        diff = odds1 - odd
        if diff <= currentDiff and odd <= odds1:
            currentDiff = diff
            current1 = odd
            
    if current1 == 0:
        current1 = ones.min()
    
    
    currentDiff = 100
            
    for odd in twos:
        diff = odds2 - odd
        if diff <= currentDiff and odd <= odds2:
            currentDiff = diff
            current2 = odd
    
    
    if current2 == 0:
        current2 = twos.min()
        
    
    currentDiff = 100
            
    for odd in threes:
        diff = odds3 - odd
        if diff <= currentDiff and odd <= odds3:
            currentDiff = diff
            current3 = odd
    
    
    if current3 == 0:
        current3 = threes.min()
        
    
    currentDiff = 100
            
    for odd in fours:
        diff = odds4 - odd
        if diff <= currentDiff and odd <= odds4:
            currentDiff = diff
            current4 = odd
    
    
    if current4 == 0:
        current4 = fours.min()
    
    match4 = fourResults[(fourResults['Odds 1'] == current1) & (fourResults['Odds 2'] == current2) & (fourResults['Odds 3'] == current3) & (fourResults['Odds 4'] == current4)]
    result4 = match4.iloc[0,-1]
    percent4 = round(result4 / 50, 4) * 100
    
    print("The closet odds for 4 bets was " + str(match4.iloc[0,0]) + ", " + str(match4.iloc[0,1]) + ", " + str(match4.iloc[0,2])+ ", " + str(match4.iloc[0,3]) + " which resulted in: " + str(result4) + " wins (" + str(percent4) + "%)")
    print("The exptected value is " + str(ev4))
    print("\n")  
    
             
    ##################
    #Look for 5 bets##
    ##################
    
    ones = np.array(fiveResults['Odds 1'])
    twos = np.array(fiveResults['Odds 2'])
    threes = np.array(fiveResults['Odds 3'])
    fours = np.array(fiveResults['Odds 4'])
    fives = np.array(fiveResults['Odds 5'])
    
    current1 = 0
    current2 = 0
    current3 = 0
    current4 = 0
    current5 = 0
    currentDiff = 100
    
    for odd in ones:
        diff = odds1 - odd
        if diff <= currentDiff and odd <= odds1:
            currentDiff = diff
            current1 = odd
            
    if current1 == 0:
        current1 = ones.min()
    
    
    currentDiff = 100
            
    for odd in twos:
        diff = odds2 - odd
        if diff <= currentDiff and odd <= odds2:
            currentDiff = diff
            current2 = odd
    
    
    if current2 == 0:
        current2 = twos.min()
        
    
    currentDiff = 100
            
    for odd in threes:
        diff = odds3 - odd
        if diff <= currentDiff and odd <= odds3:
            currentDiff = diff
            current3 = odd
    
    
    if current3 == 0:
        current3 = threes.min()
        
    
    currentDiff = 100
            
    for odd in fours:
        diff = odds4 - odd
        if diff <= currentDiff and odd <= odds4:
            currentDiff = diff
            current4 = odd
    
    
    if current4 == 0:
        current4 = fours.min()
        
    
    currentDiff = 100
            
    for odd in fives:
        diff = odds5 - odd
        if diff <= currentDiff and odd <= odds5:
            currentDiff = diff
            current5 = odd
    
    
    if current5 == 0:
        current5 = fives.min()
    
    match5 = fiveResults[(fiveResults['Odds 1'] == current1) & (fiveResults['Odds 2'] == current2) & (fiveResults['Odds 3'] == current3) & (fiveResults['Odds 4'] == current4) & (fiveResults['Odds 5'] == current5)]
    result5 = match5.iloc[0,-1]
    percent5 = round(result5 / 50, 4) * 100
    
    print("The closet odds for 5 bets was " + str(match5.iloc[0,0]) + ", " + str(match5.iloc[0,1]) + ", " + str(match5.iloc[0,2])+ ", " + str(match5.iloc[0,3]) + ", " + str(match5.iloc[0,4]) + " which resulted in: " + str(result5) + " wins (" + str(percent5) + "%)")
    print("The exptected value is " + str(ev5))
    print("\n")  

    return match1, match2, match3, match4, match5, ev


def expectedValue(odds1, odds2, odds3, odds4, odds5, line, bet):
    
    if line == "2H":
        outcome1 = 0.2156
        outcome2 = 0.1378
        outcome3 = 0.1156
        outcome4 = 0.1156
        outcome5 = 0.0822
        
        ev1 = outcome1 * (bet * odds1) + (1 - outcome1) * -bet
        ev2 = outcome1 * ((bet * odds1)-bet) + outcome2 * ((bet * odds2)-bet) + (1 - outcome1 - outcome2) * (-bet * 2)
        ev3 = outcome1 * ((bet * odds1)-(bet*2)) + outcome2 * ((bet * odds2)-(bet*2)) + outcome3 * ((bet * odds3)-(bet*2)) + (1 - outcome1 - outcome2 - outcome3) * (-bet * 3)
        ev4 = outcome1 * ((bet * odds1)-(bet*3)) + outcome2 * ((bet * odds2)-(bet*3)) + outcome3 * ((bet * odds3)-(bet*3)) + outcome4 * ((bet * odds4)-(bet*3)) + (1 - outcome1 - outcome2 - outcome3 - outcome4) * (-bet * 4)
        ev5 = outcome1 * ((bet * odds1)-(bet*4)) + outcome2 * ((bet * odds2)-(bet*4)) + outcome3 * ((bet * odds3)-(bet*4)) + outcome4 * ((bet * odds4)-(bet*4)) + outcome5 * ((bet * odds5)-(bet*4)) + (1 - outcome1 - outcome2 - outcome3 - outcome4 - outcome5) * (-bet * 5)

    if line == "2A":
        outcome1 = 0.1891
        outcome2 = 0.1114
        outcome3 = 0.1010
        outcome4 = 0.1010
        outcome5 = 0.0959
        
        ev1 = outcome1 * (bet * odds1) + (1 - outcome1) * -bet
        ev2 = outcome1 * ((bet * odds1)-bet) + outcome2 * ((bet * odds2)-bet) + (1 - outcome1 - outcome2) * (-bet * 2)
        ev3 = outcome1 * ((bet * odds1)-(bet*2)) + outcome2 * ((bet * odds2)-(bet*2)) + outcome3 * ((bet * odds3)-(bet*2)) + (1 - outcome1 - outcome2 - outcome3) * (-bet * 3)
        ev4 = outcome1 * ((bet * odds1)-(bet*3)) + outcome2 * ((bet * odds2)-(bet*3)) + outcome3 * ((bet * odds3)-(bet*3)) + outcome4 * ((bet * odds4)-(bet*3)) + (1 - outcome1 - outcome2 - outcome3 - outcome4) * (-bet * 4)
        ev5 = outcome1 * ((bet * odds1)-(bet*4)) + outcome2 * ((bet * odds2)-(bet*4)) + outcome3 * ((bet * odds3)-(bet*4)) + outcome4 * ((bet * odds4)-(bet*4)) + outcome5 * ((bet * odds5)-(bet*4)) + (1 - outcome1 - outcome2 - outcome3 - outcome4 - outcome5) * (-bet * 5)
      
    
    if line == "3H":
        outcome1 = 0.2150
        outcome2 = 0.1700
        outcome3 = 0.09
        outcome4 = 0.085
        outcome5 = 0.065
        
        ev1 = outcome1 * (bet * odds1) + (1 - outcome1) * -bet
        ev2 = outcome1 * ((bet * odds1)-bet) + outcome2 * ((bet * odds2)-bet) + (1 - outcome1 - outcome2) * (-bet * 2)
        ev3 = outcome1 * ((bet * odds1)-(bet*2)) + outcome2 * ((bet * odds2)-(bet*2)) + outcome3 * ((bet * odds3)-(bet*2)) + (1 - outcome1 - outcome2 - outcome3) * (-bet * 3)
        ev4 = outcome1 * ((bet * odds1)-(bet*3)) + outcome2 * ((bet * odds2)-(bet*3)) + outcome3 * ((bet * odds3)-(bet*3)) + outcome4 * ((bet * odds4)-(bet*3)) + (1 - outcome1 - outcome2 - outcome3 - outcome4) * (-bet * 4)
        ev5 = outcome1 * ((bet * odds1)-(bet*4)) + outcome2 * ((bet * odds2)-(bet*4)) + outcome3 * ((bet * odds3)-(bet*4)) + outcome4 * ((bet * odds4)-(bet*4)) + outcome5 * ((bet * odds5)-(bet*4)) + (1 - outcome1 - outcome2 - outcome3 - outcome4 - outcome5) * (-bet * 5)


    if line == "3A":
        outcome1 = 0.2229
        outcome2 = 0.1627
        outcome3 = 0.1205
        outcome4 = 0.1084
        outcome5 = 0.0843
        
        ev1 = outcome1 * (bet * odds1) + (1 - outcome1) * -bet
        ev2 = outcome1 * ((bet * odds1)-bet) + outcome2 * ((bet * odds2)-bet) + (1 - outcome1 - outcome2) * (-bet * 2)
        ev3 = outcome1 * ((bet * odds1)-(bet*2)) + outcome2 * ((bet * odds2)-(bet*2)) + outcome3 * ((bet * odds3)-(bet*2)) + (1 - outcome1 - outcome2 - outcome3) * (-bet * 3)
        ev4 = outcome1 * ((bet * odds1)-(bet*3)) + outcome2 * ((bet * odds2)-(bet*3)) + outcome3 * ((bet * odds3)-(bet*3)) + outcome4 * ((bet * odds4)-(bet*3)) + (1 - outcome1 - outcome2 - outcome3 - outcome4) * (-bet * 4)
        ev5 = outcome1 * ((bet * odds1)-(bet*4)) + outcome2 * ((bet * odds2)-(bet*4)) + outcome3 * ((bet * odds3)-(bet*4)) + outcome4 * ((bet * odds4)-(bet*4)) + outcome5 * ((bet * odds5)-(bet*4)) + (1 - outcome1 - outcome2 - outcome3 - outcome4 - outcome5) * (-bet * 5)


    if line == "4H":
        outcome1 = 0.1724
        outcome2 = 0.1667
        outcome3 = 0.1379
        outcome4 = 0.1092
        outcome5 = 0.0575
        
        ev1 = outcome1 * (bet * odds1) + (1 - outcome1) * -bet
        ev2 = outcome1 * ((bet * odds1)-bet) + outcome2 * ((bet * odds2)-bet) + (1 - outcome1 - outcome2) * (-bet * 2)
        ev3 = outcome1 * ((bet * odds1)-(bet*2)) + outcome2 * ((bet * odds2)-(bet*2)) + outcome3 * ((bet * odds3)-(bet*2)) + (1 - outcome1 - outcome2 - outcome3) * (-bet * 3)
        ev4 = outcome1 * ((bet * odds1)-(bet*3)) + outcome2 * ((bet * odds2)-(bet*3)) + outcome3 * ((bet * odds3)-(bet*3)) + outcome4 * ((bet * odds4)-(bet*3)) + (1 - outcome1 - outcome2 - outcome3 - outcome4) * (-bet * 4)
        ev5 = outcome1 * ((bet * odds1)-(bet*4)) + outcome2 * ((bet * odds2)-(bet*4)) + outcome3 * ((bet * odds3)-(bet*4)) + outcome4 * ((bet * odds4)-(bet*4)) + outcome5 * ((bet * odds5)-(bet*4)) + (1 - outcome1 - outcome2 - outcome3 - outcome4 - outcome5) * (-bet * 5)

    
    if line == "4A":
        outcome1 = 0.19
        outcome2 = 0.13
        outcome3 = 0.13
        outcome4 = 0.11
        outcome5 = 0.11
        
        ev1 = outcome1 * (bet * odds1) + (1 - outcome1) * -bet
        ev2 = outcome1 * ((bet * odds1)-bet) + outcome2 * ((bet * odds2)-bet) + (1 - outcome1 - outcome2) * (-bet * 2)
        ev3 = outcome1 * ((bet * odds1)-(bet*2)) + outcome2 * ((bet * odds2)-(bet*2)) + outcome3 * ((bet * odds3)-(bet*2)) + (1 - outcome1 - outcome2 - outcome3) * (-bet * 3)
        ev4 = outcome1 * ((bet * odds1)-(bet*3)) + outcome2 * ((bet * odds2)-(bet*3)) + outcome3 * ((bet * odds3)-(bet*3)) + outcome4 * ((bet * odds4)-(bet*3)) + (1 - outcome1 - outcome2 - outcome3 - outcome4) * (-bet * 4)
        ev5 = outcome1 * ((bet * odds1)-(bet*4)) + outcome2 * ((bet * odds2)-(bet*4)) + outcome3 * ((bet * odds3)-(bet*4)) + outcome4 * ((bet * odds4)-(bet*4)) + outcome5 * ((bet * odds5)-(bet*4)) + (1 - outcome1 - outcome2 - outcome3 - outcome4 - outcome5) * (-bet * 5)

    return ev1, ev2, ev3, ev4, ev5