
from infoGetter import *
from feasabilityChecker import *
from totalCost import *
from randomizer import *
from localSearch import *
import time


def runnerFunc(files, rounds, repeats, type):
    allObjectives = {}; allTimes = {}; allInitCosts = {}; actualSolutions = {}
    numSol = []
    for runde in range(rounds):
        roundScore = []
        for filename in files:
            start = time.time()
            filePath = os.getcwd() + '/CodePart/test_cases/' + filename
            data = problemData(filePath)
            if type == "Random":
                bestSolution, initCost, theSolution = randoFunc(filePath, data, repeats)
            elif type == "Local":
                bestSolution, initCost, theSolution = localSearchFunc(filePath, data, repeats)
            else:
                return f"Type {type} is not supported!"
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

            allInitCosts[filename] = initCost
            if filename not in allObjectives.keys():
                if bestSolution != "Nan":
                    allObjectives[filename] = [bestSolution]
                    actualSolutions[filename] = theSolution
                else:
                    allObjectives[filename] = [initCost]
                    actualSolutions[filename] = theSolution
            else:
                if bestSolution != "Nan":
                    tempSols = allObjectives[filename]
                    tempSols.append(bestSolution)
                    allObjectives[filename] = tempSols
                    if bestSolution == min(allObjectives[filename]):
                        actualSolutions[filename] = theSolution
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


    # This part is just for the txt file 
    avgObjectives = []
    avgTimes = []
    bestImps = []
    actualSolutionsList = []

    for key, value in allObjectives.items():
        avgObjectives.append(f"problem: {key}\nAverage best cost: {sum(value)/rounds}\nBest objective: {min(value)}\n")
        thisInitCost = allInitCosts[key]
        bestImps.append(f"Best improvement is: {round((100*(thisInitCost-min(value)) / thisInitCost), 4)}%\n\n")
    for key, value in allTimes.items():
        avgTimes.append(f"Average time is: {sum(value)/rounds}\n")
    for key, value in actualSolutions.items():
        actualSolutionsList.append(f"Actual Solution: {value}\n\n")


    with open("bestSolutions.txt", "w") as f:
        for i in range(len(avgObjectives)):
            f.write(avgObjectives[i])
            f.write(avgTimes[i])
            f.write(bestImps[i])
            f.write(actualSolutionsList[i])
        for n in range(0, len(numSol)):
            f.write(f"ROUND {n+1}\n")
            for m in numSol[n]:
                f.write(m)
    return (f"Done!")