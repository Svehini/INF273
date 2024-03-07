
import random as rd


def reInsert(currentSol, data):
    vehicleCapabilities = data["VehicleCapabilities"]
    numOfVehicles = data['NumOfVehicles']
    numOfCalls = data["NumOfCalls"]
    whichToSwitch = rd.randint(1,numOfCalls)

    changedCars = []
    for oldCar in range(len(currentSol)):
        if whichToSwitch in currentSol[oldCar]:
            currentSol[oldCar].remove(whichToSwitch)
            currentSol[oldCar].remove(whichToSwitch)
            break
    capableCars = []
    for capability in vehicleCapabilities:
        if whichToSwitch in capability[1:]:
            capableCars.append(capability[0]-1)
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
    changedCars.append(oldCar)
    changedCars.append(newCar)
    return currentSol, changedCars



# This operator takes a call and re-delivers it to the car which is feasible and makes the biggest difference in cost (VERY SLOW)
def bestInsert():

    return ...

# Same as reInsert but shuffles the car which has just been added a new call.
# This resuslts in higher diversity but lower intensity
# Will probably also return many infeasible solitions since it shuffles a whole cars deliveries
def reInsertWithShuffle(currentSol, data):
    vehicleCapabilities = data["VehicleCapabilities"]
    numOfVehicles = data['NumOfVehicles']
    numOfCalls = data["NumOfCalls"]
    whichToSwitch = rd.randint(1,numOfCalls)

    changedCars = []
    for oldCar in range(len(currentSol)):
        if whichToSwitch in currentSol[oldCar]:
            currentSol[oldCar].remove(whichToSwitch)
            currentSol[oldCar].remove(whichToSwitch)
            changedCars.append(oldCar)
            break
    capableCars = []
    for capability in vehicleCapabilities:
        if whichToSwitch in capability[1:]:
            capableCars.append(capability[0]-1)
    capableCars.append(numOfVehicles)
    rd.shuffle(capableCars)
    newCar = capableCars[0]
    if newCar == oldCar:
        try:
            newCar = capableCars[1]
        except:
            ...
    changedCars.append(newCar)
    spots = len(currentSol[newCar])
    currentSol[newCar].insert((rd.randint(0,spots)), whichToSwitch)
    currentSol[newCar].insert((rd.randint(0,spots+1)), whichToSwitch)
    rd.shuffle(currentSol[newCar])
    currentSol[newCar] = currentSol[newCar]
    return currentSol, changedCars


# This reverses one vehicle's calls
def reverser(currentSol, data):
    possibles = []
    for i in range(len(currentSol)):
        if len(currentSol[i]) > 0:
            possibles.append(i)
    rd.shuffle(possibles)
    whichToReverse = possibles[0]
    currentSol[whichToReverse].reverse()
    return currentSol, [whichToReverse]



# This is a "twoOpt"-ish operator that switches two calls in a vehicle to slighlty change it
# This is not as "risky" as some of the other ones, but will also most likely result in a smaller change
def twoOpt(currentSol, data):
    possibles = []
    for i in range(len(currentSol)):
        if len(currentSol[i]) > 2:
            possibles.append(i)
    
    rd.shuffle(possibles)

    whichToTwoOpt = currentSol[possibles[0]]
    optSpace = len(whichToTwoOpt)
    x = rd.randint(0, (optSpace-1))
    y = rd.randint(0, (optSpace-1))
    if x == y:
        if y == (optSpace-1):
            y -= 1
        else:
            y += 1
    xn = whichToTwoOpt[x]
    yn = whichToTwoOpt[y]
    whichToTwoOpt.pop(x)
    whichToTwoOpt.insert(x, xn)
    whichToTwoOpt.pop(y)
    whichToTwoOpt.insert(y, yn)
    currentSol[possibles[0]] = whichToTwoOpt
    return currentSol, [possibles[0]]

def shuffler(currentSol, data):
    numOfVehicles = data['NumOfVehicles']
    whichToReverse = rd.randint(0,numOfVehicles)
    rd.shuffle(currentSol[whichToReverse])
    return currentSol, [whichToReverse]

def outsourcedReInsert(currentSol, data):
    vehicleCapabilities = data["VehicleCapabilities"]
    numOfVehicles = data['NumOfVehicles']
    numOfCalls = data["NumOfCalls"]
    changedCars = []
    if len(currentSol[-1]) > 0:
        changedCars.append(numOfVehicles)
        whichToSwitch = currentSol[-1][rd.randint(0,len(currentSol[-1])-1)]
        currentSol[-1].remove(whichToSwitch); currentSol[-1].remove(whichToSwitch)
        capableCars = []
        for capability in vehicleCapabilities:
            if whichToSwitch in capability[1:]:
                capableCars.append(capability[0]-1)
        rd.shuffle(capableCars)
        newCar = capableCars[0]
        changedCars.append(newCar)
        spots = len(currentSol[newCar])
        currentSol[newCar].insert((rd.randint(0,spots)), whichToSwitch)
        currentSol[newCar].insert((rd.randint(0,spots+1)), whichToSwitch)
    else:
        capableCars = []
        for car in range(len(currentSol)):
            if len(currentSol[car]) > 0:
                capableCars.append(car)
        rd.shuffle(capableCars)
        oldCar = capableCars[0]
        changedCars.append(oldCar)
        whichToSwitch = currentSol[oldCar][rd.randint(0,len(currentSol[oldCar]))]
        currentSol[oldCar].remove(whichToSwitch); currentSol[oldCar].remove(whichToSwitch)
        currentSol[-1].append(whichToSwitch); currentSol[-1].append(whichToSwitch)
        changedCars.append(numOfVehicles)
    return currentSol, changedCars


# This sorts the calls in a car so that every pickup will be delivered after maximum to other pickups
def smartSorter(currentSol, _):
    mostCalls = len(currentSol[0])
    carToShuffle = 0
    for car in range(1,len(currentSol)):
        if len(currentSol[car]) > mostCalls:
            mostCalls = len(currentSol[car])
            carToShuffle = car
    if mostCalls > 4:
        oldCar = currentSol[carToShuffle]
        oldCar = list({x: None for x in oldCar})
        rd.shuffle(oldCar)
        newCar = []
        removed = oldCar.pop(0)
        newCar.append(removed); newCar.append(removed)
        while oldCar != []:
            removed = oldCar.pop(0)
            newCar.insert(-1, removed); newCar.append(removed)
        currentSol[carToShuffle] = newCar
    else: 
        rd.shuffle(currentSol[carToShuffle])
    return currentSol, [carToShuffle]
