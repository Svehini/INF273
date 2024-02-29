
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

    initSol, bestCosts = initialSolution(numOfVehicles, numOfCalls)
    initSum = costFinder(initSol, data)

    bestSolution = initSol
    bestSum = initSum

    incubentSol = initSol
    incubentSum = initSum
    bestCosts[-1] = initSum

    LowestTemperature = 0.1
    deltaAvg = []

    for i in range(100):
        checkedAdd = False
        checkedRev = False
        newSol, carRev, carAdd = reInsert(copy.deepcopy(incubentSol), data)
        if carAdd < (numOfVehicles):
            checkedAdd, carAddSol = oneCarFeasChecker(carAdd, newSol[carAdd], data)
        else:
            carAddSol = costFinder(newSol, data)
            checkedAdd = True

        if carRev < (numOfVehicles):
            checkedRev, carRevSol = oneCarFeasChecker(carRev, newSol[carRev], data)
        else:
            carRevSol = costFinder(newSol, data)
            checkedRev = True

        if (checkedAdd == True) and (checkedRev == True):
            newSolSum = incubentSum - bestCosts[carAdd] - bestCosts[carRev] + carAddSol + carRevSol
            delE = newSolSum - incubentSum
            if delE < 0:
                incubentSum = newSolSum
                incubentSol = copy.deepcopy(newSol)
                bestCosts[carAdd] = carAddSol
                bestCosts[carRev] = carRevSol
                if incubentSum < bestSum:
                    bestSum = newSolSum
                    bestSolution = copy.deepcopy(newSol)
            else:
                if rd.random() < 0.8:
                    incubentSum = newSolSum
                    incubentSol = copy.deepcopy(newSol)
                    bestCosts[carAdd] = carAddSol
                    bestCosts[carRev] = carRevSol
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
        newSol, carRev, carAdd = reInsert(copy.deepcopy(incubentSol), data)
        if carAdd < (numOfVehicles):
            checkedAdd, carAddSol = oneCarFeasChecker(carAdd, newSol[carAdd], data)
        else:
            carAddSol = costFinder(newSol, data)
            checkedAdd = True
        if carRev < (numOfVehicles):
            checkedRev, carRevSol = oneCarFeasChecker(carRev, newSol[carRev], data)
        else:
            carRevSol = costFinder(newSol, data)
            checkedRev = True
        if (checkedAdd == True) and (checkedRev == True):
            newSolSum = incubentSum - bestCosts[carAdd] - bestCosts[carRev] + carAddSol + carRevSol
            delE = newSolSum - incubentSum
            if delE < 0:
                incubentSum = newSolSum
                incubentSol = copy.deepcopy(newSol)
                bestCosts[carAdd] = carAddSol
                bestCosts[carRev] = carRevSol
                if incubentSum < bestSum:
                    bestSum = newSolSum
                    bestSolution = copy.deepcopy(newSol)
            else:
                p = math.e ** ((-delE)/temp)
                if rd.random() < p:
                    incubentSum = newSolSum
                    incubentSol = copy.deepcopy(newSol)
                    bestCosts[carAdd] = carAddSol
                    bestCosts[carRev] = carRevSol
        temp = alpha * temp
    for i in range(len(bestSolution)-1):
        appCar = bestSolution[i]
        appCar.append(0)
        bestSolution[i] = appCar
    return bestSum, initSum, sum(bestSolution, [])

