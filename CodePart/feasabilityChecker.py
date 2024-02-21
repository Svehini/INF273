from infoGetter import *


def feasChecker(solution, data):
    numOfVehicles = data['NumOfVehicles']
    numOfNodes = data['NumOfNodes']
    numOfCalls = data["NumOfCalls"]
    vehicleCapacity = data["VehicleCapacity"]
    vehicleStartingTime = data["VehicleStartingTime"]
    vehicleStartingNode = data["VehicleStartingNode"]
    callOrigin = data["CallOrigin"]
    calldestination = data["CallDestination"]
    callSize = data["CallSize"]
    callPickupTimes = data["CallPickUpTimes"]
    callDeliveryTimes = data["CallDeliveryTimes"]
    # vehicleCapabilities = data["VehicleCapabilities"]
    travelTimeAndCost = data["Travel Time and Cost"]
    dockingCostAndTime = data["Docking Cost and Time"]
    

    pickedUp = []
    visited = []
    vehicleNum = 0
    travelCost = 0
    if solution[0] != 0:
        vehicleCap = vehicleCapacity[0]
        currentVehicleCargo = 0
        time = vehicleStartingTime[0]
        vehiclePlacement = vehicleStartingNode[0]

    for i in range(len(solution)):
        if solution[i] != 0:
            node = solution[i]
            if node not in pickedUp:
                pickedUp.append(node)
                if currentVehicleCargo + callSize[node-1] > vehicleCap:
                    return False, 0
                currentVehicleCargo += callSize[node-1]
                callPlace = callOrigin
                callTime = callPickupTimes
                dockDelOrPick = 2
            else:
                pickedUp.remove(node)
                currentVehicleCargo -= (callSize[node-1])
                callPlace = calldestination
                callTime = callDeliveryTimes
                dockDelOrPick = 4

            # Checks the delivery time and makes sure it is not too late, and makes the car wait until LB constraint is met
            callPoint = ((int(vehiclePlacement-1)*(int(numOfNodes) * int(numOfVehicles))) + int((callPlace[node-1]-1) * numOfVehicles) + (vehicleNum))
            time += int(travelTimeAndCost[callPoint][3])
            travelCost += int(travelTimeAndCost[callPoint][4])
            left, right = callTime[node-1]
            if time > right:
                return False, 0
            elif time < left:
                time = left
            vehiclePlacement = travelTimeAndCost[callPoint][2]


            callPoint = (vehicleNum * numOfCalls) + (node-1)
            time += dockingCostAndTime[callPoint][dockDelOrPick]
            if node not in visited:
                travelCost += dockingCostAndTime[callPoint][3]; travelCost += dockingCostAndTime[callPoint][5]
                visited.append(node)


        else:
            vehicleNum += 1
            if (vehicleNum+1) > numOfVehicles:
                break
            vehicleCap = vehicleCapacity[vehicleNum]
            currentVehicleCargo = 0
            pickedUp = []                               # Which packages the given vehicle has picked up
            time = vehicleStartingTime[vehicleNum]      # The time of the vehicle
            vehiclePlacement = vehicleStartingNode[vehicleNum]


    return True, travelCost