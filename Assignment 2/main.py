from infoGetter import *
from feasabilityChecker import *
from totalCost import *
from randomizer import *
import time

files = ['Call_7_Vehicle_3.txt', 'Call_18_Vehicle_5.txt', 'Call_35_Vehicle_7.txt', 
         'Call_80_Vehicle_20.txt', 'Call_130_Vehicle_40.txt', 'Call_300_Vehicle_90.txt']

# files = ['Call_7_Vehicle_3.txt', 'Call_18_Vehicle_5.txt']

allObjectives = {}; allTimes = {}; allInitCosts = []
numSol = []
repeats = 10000
rounds = 10
for rund in range(rounds):
    roundScore = []
    for filename in files:
        start = time.time()
        filePath = os.getcwd() + '/Assignment 2/test_cases/' + filename
        data = problemData(filePath)
        bestSolution, initCost = randoFunc(filePath, data, repeats)
        end = time.time()
        if bestSolution != "Nan":
            imp = round((100*(initCost-bestSolution) / initCost), 4)
        else:
            imp = 0
            bestSolution = "Nan"
        line = ("##########################################################################################\n")
        probInfo = (f"Problem: {filename}\nBest cost: {bestSolution}\n")
        initSol = (f"Initial cost: {initCost}\n")
        timeUsed = (f"Time used: {end-start}\n")
        improvement = (f"Improvement: {imp}%\n")
        roundScore.append(line); roundScore.append(probInfo); roundScore.append(initSol); 
        roundScore.append(improvement); roundScore.append(timeUsed); roundScore.append(line); roundScore.append("\n")
        if rund == 1:
            allInitCosts.append(initCost)

        if filename not in allObjectives.keys():
            if bestSolution != "Nan":
                allObjectives[filename] = [bestSolution]
            else:
                allObjectives[filename] = [initCost]
        else:
            if bestSolution != "Nan":
                tempSols = allObjectives[filename]
                tempSols.append(bestSolution)
                allObjectives[filename] = tempSols
            else:
                tempSols = allObjectives[filename]
                tempSols.append(initCost)
                allObjectives[filename] = tempSols

        if filename not in allTimes.keys():
            t = end-start
            allTimes[filename] = [t]
        else:
            t = end-start
            tempSols = allTimes[filename]
            tempSols.append(t)
            allTimes[filename] = tempSols

    if roundScore != []:
        numSol.append(roundScore)
    else:
        numSol.append("THERE WERE NO SOLUTIONS THIS ROUND!")

avgObjectives = []
avgTimes = []
bestImps = []

for key, value in allObjectives.items():
    avgObjectives.append(f"problem: {key}\nAverage best cost: {sum(value)/10}\nBest objective: {min(value)}\n")
    thisInitCost = allInitCosts.pop(0)
    bestImps.append(f"Best improvement is: {round((100*(thisInitCost-min(value)) / thisInitCost), 4)}\n\n")
for key, value in allTimes.items():
    avgTimes.append(f"Average time is: {sum(value)/10}\n")

with open("bestSolutions.txt", "w") as f:
    for i in range(len(avgObjectives)):
        f.write(avgObjectives[i])
        f.write(avgTimes[i])
        f.write(bestImps[i])
    for n in range(0, len(numSol)):
        f.write(f"ROUND {n+1}\n")
        for m in numSol[n]:
            f.write(m)

print("Done!")
