from feasabilityChecker import *
from totalCost import *
from infoGetter import *
import random


# If a car is assigned to a package they cant pick up and deliver the package will be assigned to outsourcing instead
def vibeChecker(shuffledSol, vehicleCapabilities, numOfVehicles):
    vehicleNum = 0
    for num in range(numOfVehicles-1):
        for package in shuffledSol[num]:
            if package not in vehicleCapabilities[vehicleNum]:
                shuffledSol[num].remove(package)
                if len(shuffledSol) < numOfVehicles:
                    shuffledSol.append([package])
                else:
                    shuffledSol[vehicleNum].append(package)
        numOfVehicles += 1
    return shuffledSol


# MAKE A SHUFFLER THAT EVENLY DISTRIBUTES THE CALLS AMONG THE VEHICLES
# MAYBE ALSO SORT CALLS AFTER EARLIST UB DELIVERY TIME (?)
def listShuffler(numOfVehicles, numOfCalls, vehicleCapabilities):
    solRep = []
    for i in range(numOfVehicles):
        solRep.append(0)
    for i in range(1,numOfCalls+1):
        solRep.append(i)
    random.shuffle(solRep)
    shuffledSol = []
    tempList = []
    for i in solRep:
        if i == 0:
            shuffledSol.append(tempList)
            tempList = []
        else:
            tempList.append(i)
    if tempList != []:
        shuffledSol.append(tempList)
    solRep = []
    shuffledSol = vibeChecker(shuffledSol, vehicleCapabilities, numOfVehicles)
    for i in range(len(shuffledSol)):
        tempList =[]
        for j in shuffledSol[i]:
            tempList.append(j); tempList.append(j)
        random.shuffle(tempList)
        if i != numOfVehicles:
            tempList.append(0)
        solRep.append(tempList)
    solRep = sum(solRep, [])
    return solRep

def initialSolution(numOfVehicles, numOfCalls):
    initialSolution = []
    for i in range(numOfVehicles):
        initialSolution.append(0)
    for i in range(1, numOfCalls+1):
        initialSolution.append(i); initialSolution.append(i);
    return initialSolution

def randoFunc(filePath, data, repeats):

    numOfVehicles = data['NumOfVehicles']
    numOfCalls = data["NumOfCalls"]
    vehicleCapabilities = data["VehicleCapabilities"]


    initSol = initialSolution(numOfVehicles, numOfCalls)
    initSum = costFinder(initSol, data)
    bestSolution = "Nan"
    for i in range(0, repeats):                              # Change to 10 000
        solRep = listShuffler(numOfVehicles, numOfCalls, vehicleCapabilities)
        checked, totalSum = feasChecker(solRep, data)
        if checked == True:
            totalSum += costFinder(solRep, data)
            if (bestSolution == "Nan"):
                bestSolution = totalSum
                theSolution = solRep
            elif (totalSum < bestSolution):
                bestSolution = totalSum
                theSolution = solRep
    if bestSolution != "Nan":
        return bestSolution, initSum
    else: 
        return "Nan", initSum