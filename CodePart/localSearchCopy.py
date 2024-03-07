
from feasabilityChecker import *
from totalCost import *
from infoGetter import *
from operatorFunc import *
from feasCheckForOneCar import *
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

def localSearchFunc(filename, data, repeats):
    numOfVehicles = data['NumOfVehicles']
    numOfCalls = data["NumOfCalls"]

    initSol, bestCosts = initialSolution(numOfVehicles, numOfCalls)
    initSum = costFinder(initSol, data)

    bestSolution = initSol
    bestSum = initSum
    bestCosts[-1] = initSum

    for i in range(repeats):
        newCosts = []
        newSolValid = True
        newSol, changedCars = reInsert(copy.deepcopy(bestSolution), data)
        newSolSum = bestSum
        for car in changedCars:
            newSolSum -= bestCosts[car]
            if car < numOfVehicles:
                newCarChecked, newCarPrice = oneCarFeasChecker(car, newSol[car], data)
                if not newCarChecked:
                    newSolValid = False
                    break
            else:
                newCarPrice = costFinder(newSol, data)
            newSolSum += newCarPrice
            newCosts.append(newCarPrice)
        if newSolValid:
            if (newSolSum < bestSum):
                for car in changedCars:
                    bestCosts[car] = newCosts.pop(0)
                bestSum = newSolSum
                bestSolution = copy.deepcopy(newSol)
    
    for i in range(len(bestSolution)-1):
        appCar = bestSolution[i]
        appCar.append(0)
        bestSolution[i] = appCar
    return bestSum, initSum, sum(bestSolution, [])



from feasabilityChecker import *
from totalCost import *
from infoGetter import *
from operatorFunc import *
from feasCheckForOneCar import *
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

def localSearchFunc(filename, data, repeats):
    numOfVehicles = data['NumOfVehicles']
    numOfCalls = data["NumOfCalls"]

    initSol, bestCosts = initialSolution(numOfVehicles, numOfCalls)
    initSum = costFinder(initSol, data)

    bestSolution = initSol
    bestSum = initSum
    bestCosts[-1] = initSum

    for i in range(repeats):
        checkedAdd = False
        newSol, carRev, carAdd = reInsert(copy.deepcopy(bestSolution), data)
        if carAdd < (numOfVehicles):
            checkedAdd, carAddSol = oneCarFeasChecker(carAdd, newSol[carAdd], data)
        else:
            carAddSol = costFinder(newSol, data)
            checkedAdd = True
        if carRev != "Nan":
            if carRev < (numOfVehicles):
                _ , carRevSol = oneCarFeasChecker(carRev, newSol[carRev], data) # A car where a call has been removed will never become infeasable from removing that call
            else:
                carRevSol = costFinder(newSol, data)
            newSolSum = bestSum - bestCosts[carAdd] - bestCosts[carRev] + carAddSol + carRevSol
        else:
            newSolSum = bestSum - bestCosts[carAdd] + carAddSol

        if (checkedAdd == True):
            if (newSolSum < bestSum):
                bestCosts[carAdd] = carAddSol
                bestCosts[carRev] = carRevSol
                bestSum = sum(bestCosts)
                bestSolution = copy.deepcopy(newSol)
    
    for i in range(len(bestSolution)-1):
        appCar = bestSolution[i]
        appCar.append(0)
        bestSolution[i] = appCar
    return bestSum, initSum, sum(bestSolution, [])

