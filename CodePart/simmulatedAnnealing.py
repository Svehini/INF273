
from feasabilityChecker import *
from totalCost import *
from infoGetter import *
from operatorFunc import *
import random as rd
import math

def initialSolution(numOfVehicles, numOfCalls):
    initSol = []
    for i in range(numOfVehicles):
        initSol.append(0)
    for i in range(1, numOfCalls+1):
        initSol.append(i); initSol.append(i)
    return initSol

def simulatedAnnealingFunc(filename, data, repeats):
    numOfVehicles = data['NumOfVehicles']
    numOfCalls = data["NumOfCalls"]

    initSol = initialSolution(numOfVehicles, numOfCalls)
    initSum = costFinder(initSol, data)

    bestSolution = initSol
    bestSum = initSum

    incubentSol = initSol
    incubentSum = initSum

    LowestTemperature = 0.1
    deltaAvg = []

    for i in range(100):
        newSolution = reInsert(incubentSol, data)
        checked, newSolSum = feasChecker(newSolution, data)
        if checked:
            newSolSum += costFinder(newSolution, data)
            delE = newSolSum - incubentSum
            if delE < 0:
                incubentSum = newSolSum
                incubentSol = newSolution
                if incubentSum < bestSum:
                    bestSolution = incubentSol
                    bestSum = incubentSum
            else:
                if rd.random() < 0.8:
                    incubentSum = newSolSum
                    incubentSol = newSolution
                deltaAvg.append(delE)

    deltaAvg = sum(deltaAvg) / len(deltaAvg)
    startTemp = (-deltaAvg) / math.log(0.8)
    alpha = (0.1/startTemp) ** (1/9900)
    temp = startTemp

    for i in range(9900):
        if temp < LowestTemperature:
            break
        newSolution = reInsert(incubentSol, data)
        checked, newSolSum = feasChecker(newSolution, data)
        if checked:
            newSolSum += costFinder(newSolution, data)
            delE = newSolSum - incubentSum
            if delE < 0:
                incubentSum = newSolSum
                incubentSol = newSolution
                if incubentSum < bestSum:
                    bestSolution = incubentSol
                    bestSum = incubentSum
            else:
                p = math.e ** ((-delE)/temp)
                if rd.random() < p:
                    incubentSum = newSolSum
                    incubentSol = newSolution
        temp = alpha * temp
    return bestSum, initSum, bestSolution
