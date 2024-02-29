
import random as rd


def reInsert(currentSol, data):
    vehicleCapabilities = data["VehicleCapabilities"]
    numOfVehicles = data['NumOfVehicles']
    numOfCalls = data["NumOfCalls"]

    whichToSwitch = rd.randint(1,numOfCalls)

    for oldCar in range(len(currentSol)):
        if whichToSwitch in currentSol[oldCar]:
            currentSol[oldCar].remove(whichToSwitch)
            currentSol[oldCar].remove(whichToSwitch)
            break

    capableCars = []
    for capability in vehicleCapabilities:
        carNum = capability[0]
        if whichToSwitch in capability[1:]:
            capableCars.append(carNum-1)
    capableCars.append(numOfVehicles)
    rd.shuffle(capableCars)
    newCar = capableCars[0]
    if newCar == oldCar:
        try:
            newCar = capableCars[1]
        except:
            ...
    spots = len(currentSol[newCar])
    currentSol[newCar].insert((rd.randint(0,spots)), whichToSwitch)
    currentSol[newCar].insert((rd.randint(0,spots+1)), whichToSwitch)
    return currentSol, oldCar, newCar