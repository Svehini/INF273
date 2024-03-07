
from feasabilityChecker import *
from totalCost import *
from infoGetter import *
from operatorFunc import *
from feasCheckForOneCar import *
import random as rd
import math
import copy

def initialSolution(numOfVehicles, numOfCalls):
    initSol = []
    carCosts = []
    for i in range(numOfVehicles):
        initSol.append([])
        carCosts.append(0)
    outsourcedList = []
    for i in range(1, numOfCalls+1):
        outsourcedList.append(i); outsourcedList.append(i)
    carCosts.append(0)
    initSol.append(outsourcedList)
    return initSol, carCosts


def simulatedAnnealingFunc(filename, data, repeats):
    numOfVehicles = data['NumOfVehicles']
    numOfCalls = data["NumOfCalls"]
    callPenalty = data['CallPenalty']

    initSol, bestCosts = initialSolution(numOfVehicles, numOfCalls)
    initSum = costFinder(initSol, callPenalty)

    bestSolution = initSol
    bestSum = initSum

    incubentSol = initSol
    incubentSum = initSum
    bestCosts[-1] = initSum

    LowestTemperature = 0.1
    deltaAvg = []
    # operators = [reInsert, outsourcedReInsert, shuffler]
    # chances = [0.3, 0.30, 0.1]
    allOperators = [reInsert, outsourcedReInsert, shuffler, smartSorter, reInsertWithShuffle, reverser, twoOpt]
    operators = [reInsert, outsourcedReInsert, shuffler, smartSorter]
    chances = [0.35, 0.75, 0, 0.2]

    for i in range(100):
        newCosts = []
        newSolValid = True
        newSolSum = incubentSum

        # This is with equal weights
        # rd.shuffle(operators)
        # newSol, changedCars = operators[0](copy.deepcopy(incubentSol), data)

        # This is with whifted weight
        chosenOp = rd.choices(operators, chances)[0]
        newSol, changedCars = chosenOp(copy.deepcopy(incubentSol), data)
        # newSol, changedCars = smartSorter(copy.deepcopy(incubentSol), data)

        # This iterates through the cars that has been changed in the operator and updates the costs
        for car in changedCars:
            newSolSum -= bestCosts[car]
            if car < numOfVehicles:
                newCarChecked, newCarPrice = oneCarFeasChecker(car, newSol[car], data)
                if not newCarChecked:
                    newSolValid = False
                    break
            else:
                newCarPrice = costFinder(newSol, callPenalty)
            newSolSum += newCarPrice
            newCosts.append(newCarPrice)

        if newSolValid:
            delE = newSolSum - incubentSum
            if delE < 0:
                incubentSum = newSolSum
                incubentSol = copy.deepcopy(newSol)
                for car in changedCars:
                    bestCosts[car] = newCosts.pop(0)
                if incubentSum < bestSum:
                    bestSum = newSolSum
                    bestSolution = copy.deepcopy(newSol)
            else:
                if rd.random() < 0.8:
                    incubentSum = newSolSum
                    incubentSol = copy.deepcopy(newSol)
                    for car in changedCars:
                        bestCosts[car] = newCosts.pop(0)
                deltaAvg.append(delE)
    if deltaAvg != []:
        deltaAvg = sum(deltaAvg) / len(deltaAvg)
    else:
        deltaAvg = initSum/20
    startTemp = (-deltaAvg) / math.log(0.8)
    alpha = (0.1/startTemp) ** (1/9900)
    temp = startTemp

    for i in range(9900):
        if temp < LowestTemperature:
            break
        newCosts = []
        newSolValid = True
        newSolSum = incubentSum


        # This is with equal weights
        # rd.shuffle(operators)
        # newSol, changedCars = operators[0](copy.deepcopy(incubentSol), data)

        # This is with whifted weight
        chosenOp = rd.choices(operators, chances)[0]
        newSol, changedCars = chosenOp(copy.deepcopy(incubentSol), data)

        # This iterates through the cars that has been changed in the operator and updates the costs
        for car in changedCars:
            newSolSum -= bestCosts[car]
            if car < numOfVehicles:
                newCarChecked, newCarPrice = oneCarFeasChecker(car, newSol[car], data)
                if not newCarChecked:
                    newSolValid = False
                    break
            else:
                newCarPrice = costFinder(newSol, callPenalty)
            newSolSum += newCarPrice
            newCosts.append(newCarPrice)

        if newSolValid:
            delE = newSolSum - incubentSum
            if delE < 0:
                incubentSum = newSolSum
                incubentSol = copy.deepcopy(newSol)
                for car in changedCars:
                    bestCosts[car] = newCosts.pop(0)
                if incubentSum < bestSum:
                    bestSum = newSolSum
                    bestSolution = copy.deepcopy(newSol)
            else:
                p = math.e ** ((-delE)/temp)
                if rd.random() < p:
                    incubentSum = newSolSum
                    incubentSol = copy.deepcopy(newSol)
                    for car in changedCars:
                        bestCosts[car] = newCosts.pop(0)
        temp = alpha * temp
    for i in range(len(bestSolution)-1):
        appCar = bestSolution[i]
        appCar.append(0)
        bestSolution[i] = appCar
    return bestSum, initSum, sum(bestSolution, [])

