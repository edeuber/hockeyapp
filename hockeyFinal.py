import pandas as pd
import numpy as np
from io import BytesIO
from csv import writer 
import csv
import itertools


def runAnalysis(odds1,odds2,odds3,odds4,odds5,line,bet):

    ####################
    ##Analysis of Bets##
    ####################
    oneResults = pd.read_csv('1_Bet_Data_Refined.csv')
    twoResults = pd.read_csv('2_Bet_Data_Refined.csv')
    threeResults = pd.read_csv('3_Bet_Data_Refined.csv')
    fourResults = pd.read_csv('4_Bet_Data_Refined.csv')
    fiveResults = pd.read_csv('5_Bet_Data_Refined.csv')
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

    return result1, result2, result3, result4, result5, percent1, percent2, percent3, percent4, percent5, ev1, ev2, ev3, ev4, ev5


def expectedValue(odds1, odds2, odds3, odds4, odds5, line, bet):
    
    ev1 = 0
    ev2 = 0
    ev3 = 0
    ev4 = 0
    ev5 = 0
    
    
    if line == "2H":
        probs = getProbs(line)
        outcome1 = probs[1]
        outcome2 = probs[3]
        outcome3 = probs[5]
        outcome4 = probs[7]
        outcome5 = probs[9]
        
        ev1 = outcome1 * (bet * odds1) + (1 - outcome1) * -bet
        ev2 = outcome1 * ((bet * odds1)-bet) + outcome2 * ((bet * odds2)-bet) + (1 - outcome1 - outcome2) * (-bet * 2)
        ev3 = outcome1 * ((bet * odds1)-(bet*2)) + outcome2 * ((bet * odds2)-(bet*2)) + outcome3 * ((bet * odds3)-(bet*2)) + (1 - outcome1 - outcome2 - outcome3) * (-bet * 3)
        ev4 = outcome1 * ((bet * odds1)-(bet*3)) + outcome2 * ((bet * odds2)-(bet*3)) + outcome3 * ((bet * odds3)-(bet*3)) + outcome4 * ((bet * odds4)-(bet*3)) + (1 - outcome1 - outcome2 - outcome3 - outcome4) * (-bet * 4)
        ev5 = outcome1 * ((bet * odds1)-(bet*4)) + outcome2 * ((bet * odds2)-(bet*4)) + outcome3 * ((bet * odds3)-(bet*4)) + outcome4 * ((bet * odds4)-(bet*4)) + outcome5 * ((bet * odds5)-(bet*4)) + (1 - outcome1 - outcome2 - outcome3 - outcome4 - outcome5) * (-bet * 5)

    if line == "2A":
        probs = getProbs(line)
        outcome1 = probs[1]
        outcome2 = probs[3]
        outcome3 = probs[5]
        outcome4 = probs[7]
        outcome5 = probs[9]
        
        ev1 = outcome1 * (bet * odds1) + (1 - outcome1) * -bet
        ev2 = outcome1 * ((bet * odds1)-bet) + outcome2 * ((bet * odds2)-bet) + (1 - outcome1 - outcome2) * (-bet * 2)
        ev3 = outcome1 * ((bet * odds1)-(bet*2)) + outcome2 * ((bet * odds2)-(bet*2)) + outcome3 * ((bet * odds3)-(bet*2)) + (1 - outcome1 - outcome2 - outcome3) * (-bet * 3)
        ev4 = outcome1 * ((bet * odds1)-(bet*3)) + outcome2 * ((bet * odds2)-(bet*3)) + outcome3 * ((bet * odds3)-(bet*3)) + outcome4 * ((bet * odds4)-(bet*3)) + (1 - outcome1 - outcome2 - outcome3 - outcome4) * (-bet * 4)
        ev5 = outcome1 * ((bet * odds1)-(bet*4)) + outcome2 * ((bet * odds2)-(bet*4)) + outcome3 * ((bet * odds3)-(bet*4)) + outcome4 * ((bet * odds4)-(bet*4)) + outcome5 * ((bet * odds5)-(bet*4)) + (1 - outcome1 - outcome2 - outcome3 - outcome4 - outcome5) * (-bet * 5)
      
    
    if line == "3H":
        probs = getProbs(line)
        outcome1 = probs[1]
        outcome2 = probs[3]
        outcome3 = probs[5]
        outcome4 = probs[7]
        outcome5 = probs[9]
        
        ev1 = outcome1 * (bet * odds1) + (1 - outcome1) * -bet
        ev2 = outcome1 * ((bet * odds1)-bet) + outcome2 * ((bet * odds2)-bet) + (1 - outcome1 - outcome2) * (-bet * 2)
        ev3 = outcome1 * ((bet * odds1)-(bet*2)) + outcome2 * ((bet * odds2)-(bet*2)) + outcome3 * ((bet * odds3)-(bet*2)) + (1 - outcome1 - outcome2 - outcome3) * (-bet * 3)
        ev4 = outcome1 * ((bet * odds1)-(bet*3)) + outcome2 * ((bet * odds2)-(bet*3)) + outcome3 * ((bet * odds3)-(bet*3)) + outcome4 * ((bet * odds4)-(bet*3)) + (1 - outcome1 - outcome2 - outcome3 - outcome4) * (-bet * 4)
        ev5 = outcome1 * ((bet * odds1)-(bet*4)) + outcome2 * ((bet * odds2)-(bet*4)) + outcome3 * ((bet * odds3)-(bet*4)) + outcome4 * ((bet * odds4)-(bet*4)) + outcome5 * ((bet * odds5)-(bet*4)) + (1 - outcome1 - outcome2 - outcome3 - outcome4 - outcome5) * (-bet * 5)


    if line == "3A":
        probs = getProbs(line)
        outcome1 = probs[1]
        outcome2 = probs[3]
        outcome3 = probs[5]
        outcome4 = probs[7]
        outcome5 = probs[9]
        
        ev1 = outcome1 * (bet * odds1) + (1 - outcome1) * -bet
        ev2 = outcome1 * ((bet * odds1)-bet) + outcome2 * ((bet * odds2)-bet) + (1 - outcome1 - outcome2) * (-bet * 2)
        ev3 = outcome1 * ((bet * odds1)-(bet*2)) + outcome2 * ((bet * odds2)-(bet*2)) + outcome3 * ((bet * odds3)-(bet*2)) + (1 - outcome1 - outcome2 - outcome3) * (-bet * 3)
        ev4 = outcome1 * ((bet * odds1)-(bet*3)) + outcome2 * ((bet * odds2)-(bet*3)) + outcome3 * ((bet * odds3)-(bet*3)) + outcome4 * ((bet * odds4)-(bet*3)) + (1 - outcome1 - outcome2 - outcome3 - outcome4) * (-bet * 4)
        ev5 = outcome1 * ((bet * odds1)-(bet*4)) + outcome2 * ((bet * odds2)-(bet*4)) + outcome3 * ((bet * odds3)-(bet*4)) + outcome4 * ((bet * odds4)-(bet*4)) + outcome5 * ((bet * odds5)-(bet*4)) + (1 - outcome1 - outcome2 - outcome3 - outcome4 - outcome5) * (-bet * 5)


    if line == "4H":
        probs = getProbs(line)
        outcome1 = probs[1]
        outcome2 = probs[3]
        outcome3 = probs[5]
        outcome4 = probs[7]
        outcome5 = probs[9]
        
        ev1 = outcome1 * (bet * odds1) + (1 - outcome1) * -bet
        ev2 = outcome1 * ((bet * odds1)-bet) + outcome2 * ((bet * odds2)-bet) + (1 - outcome1 - outcome2) * (-bet * 2)
        ev3 = outcome1 * ((bet * odds1)-(bet*2)) + outcome2 * ((bet * odds2)-(bet*2)) + outcome3 * ((bet * odds3)-(bet*2)) + (1 - outcome1 - outcome2 - outcome3) * (-bet * 3)
        ev4 = outcome1 * ((bet * odds1)-(bet*3)) + outcome2 * ((bet * odds2)-(bet*3)) + outcome3 * ((bet * odds3)-(bet*3)) + outcome4 * ((bet * odds4)-(bet*3)) + (1 - outcome1 - outcome2 - outcome3 - outcome4) * (-bet * 4)
        ev5 = outcome1 * ((bet * odds1)-(bet*4)) + outcome2 * ((bet * odds2)-(bet*4)) + outcome3 * ((bet * odds3)-(bet*4)) + outcome4 * ((bet * odds4)-(bet*4)) + outcome5 * ((bet * odds5)-(bet*4)) + (1 - outcome1 - outcome2 - outcome3 - outcome4 - outcome5) * (-bet * 5)

    
    if line == "4A":
        probs = getProbs(line)
        outcome1 = probs[1]
        outcome2 = probs[3]
        outcome3 = probs[5]
        outcome4 = probs[7]
        outcome5 = probs[9]
        
        ev1 = outcome1 * (bet * odds1) + (1 - outcome1) * -bet
        ev2 = outcome1 * ((bet * odds1)-bet) + outcome2 * ((bet * odds2)-bet) + (1 - outcome1 - outcome2) * (-bet * 2)
        ev3 = outcome1 * ((bet * odds1)-(bet*2)) + outcome2 * ((bet * odds2)-(bet*2)) + outcome3 * ((bet * odds3)-(bet*2)) + (1 - outcome1 - outcome2 - outcome3) * (-bet * 3)
        ev4 = outcome1 * ((bet * odds1)-(bet*3)) + outcome2 * ((bet * odds2)-(bet*3)) + outcome3 * ((bet * odds3)-(bet*3)) + outcome4 * ((bet * odds4)-(bet*3)) + (1 - outcome1 - outcome2 - outcome3 - outcome4) * (-bet * 4)
        ev5 = outcome1 * ((bet * odds1)-(bet*4)) + outcome2 * ((bet * odds2)-(bet*4)) + outcome3 * ((bet * odds3)-(bet*4)) + outcome4 * ((bet * odds4)-(bet*4)) + outcome5 * ((bet * odds5)-(bet*4)) + (1 - outcome1 - outcome2 - outcome3 - outcome4 - outcome5) * (-bet * 5)

    return ev1, ev2, ev3, ev4, ev5


def getProbs(scenario = "2H"):

    ################################
    ##Get Likelihoods for Scenario##
    ################################
    probs = pd.read_csv('Likelihoods.csv')
    probs = probs[probs['Key'] == scenario]
    
    score1 = probs.iloc[0,4]
    like1 = probs.iloc[0,5]
    
    score2 = probs.iloc[1,4]
    like2 = probs.iloc[1,5]
    
    score3 = probs.iloc[2,4]
    like3 = probs.iloc[2,5]
    
    score4 = probs.iloc[3,4]
    like4 = probs.iloc[3,5]
    
    score5 = probs.iloc[4,4]
    like5 = probs.iloc[4,5]
    
    return score1, like1, score2, like2, score3, like3, score4, like4, score5, like5



    
    
    
    
    