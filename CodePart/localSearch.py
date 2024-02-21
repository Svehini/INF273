
from feasabilityChecker import *
from totalCost import *
from infoGetter import *
from operatorFunc import *

def initialSolution(numOfVehicles, numOfCalls):
    initSol = []
    for i in range(numOfVehicles):
        initSol.append(0)
    for i in range(1, numOfCalls+1):
        initSol.append(i); initSol.append(i)
    return initSol

def localSearchFunc(filename, data, repeats):
    numOfVehicles = data['NumOfVehicles']
    numOfCalls = data["NumOfCalls"]

    initSol = initialSolution(numOfVehicles, numOfCalls)
    initSum = costFinder(initSol, data)

    bestSolution = initSol
    bestSum = initSum

    for i in range(repeats):
        newSol = reInsert(bestSolution, data)
        checked, newSolSum = feasChecker(newSol, data)
        if checked:
            newSolSum += costFinder(newSol, data)
        if (newSolSum < bestSum) and checked:
            bestSum = newSolSum
            bestSolution = newSol
    if checked:
        return newSolSum, initSum, newSol
    return bestSum, initSum, bestSolution
    # return bestSolution, initSum, theSolution

