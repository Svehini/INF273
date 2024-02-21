
import random as rd


def reInsert(currentSol, data):
    vehicleCapabilities = data["VehicleCapabilities"]
    numOfVehicles = data['NumOfVehicles']
    numOfCalls = data["NumOfCalls"]

    whichToSwitch = rd.randint(1,numOfCalls)

    # This codeblock removes the given call which is just randomized at this point
    tempList = []
    shuffledSol = []
    for i in currentSol:
        if i == 0:
            shuffledSol.append(tempList)
            tempList = []
        else:
            tempList.append(i)
    if tempList != []:
        shuffledSol.append(tempList)
    elif currentSol[-1] == 0:
        shuffledSol.append([])
    for l in range(len(shuffledSol)):
        if whichToSwitch in shuffledSol[l]:
            shuffledSol[l].remove(whichToSwitch)
            shuffledSol[l].remove(whichToSwitch)
            break

    # This block makes a list of all capable cars for this package to be sent to
    # Now this also removes the car num (FYI)
    capableCars = []
    for capability in vehicleCapabilities:
        carNum = capability[0]
        if whichToSwitch in capability[1:]:
            capableCars.append(carNum-1)
    capableCars.append(numOfVehicles)
    rd.shuffle(capableCars)
    newCar = capableCars[0]
    if newCar == l:
        try:
            newCar = capableCars[1]
        except:
            ...
    spots = len(shuffledSol[newCar])
    shuffledSol[newCar].insert((rd.randint(0,spots)), whichToSwitch)
    shuffledSol[newCar].insert((rd.randint(0,spots+1)), whichToSwitch)

    # This part adds back the 0´s in the list
    for i in range(len(shuffledSol)):
        if i != numOfVehicles:
            shuffledSol[i].append(0)
    newSol = sum(shuffledSol, [])
    return newSol