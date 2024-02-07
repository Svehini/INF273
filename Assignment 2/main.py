from infoGetter import *
from feasabilityChecker import *
from totalCost import *
from randomizer import *
import time

files = ['Call_7_Vehicle_3.txt', 'Call_18_Vehicle_5.txt', 'Call_35_Vehicle_7.txt', 
         'Call_80_Vehicle_20.txt', 'Call_130_Vehicle_40.txt', 'Call_300_Vehicle_90.txt']

# files = ['Call_7_Vehicle_3.txt']

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
        if bestSolution != "Nan":
            imp = round((100*(initCost-bestSolution) / initCost), 4)
            end = time.time()

            line = ("##########################################################################################\n")
            probInfo = (f"Problem: {filename}\nBest cost: {bestSolution}\n")
            initSol = (f"Initial cost: {initCost}\n")
            timeUsed = (f"Time used: {end-start}\n")
            improvement = (f"Improvement: {imp}%\n")
            roundScore.append(line); roundScore.append(probInfo); roundScore.append(initSol); 
            roundScore.append(improvement); roundScore.append(timeUsed); roundScore.append(line); roundScore.append("\n")
    if roundScore != []:
        numSol.append(roundScore)
    else: numSol = []

with open("bestSolutions.txt", "w") as f:
    for n in range(0, len(numSol)):
        f.write(f"ROUND {n+1}\n")
        for m in numSol[n]:
            f.write(m)

print("Done!")
