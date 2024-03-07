# from infoGetter import *

def oneCarFeasChecker(carNum, pickedUpItems, data):
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
    travelTimeAndCost = data["Travel Time and Cost"]
    dockingCostAndTime = data["Docking Cost and Time"]

    pickedUp = []
    visited = []
    travelCost = 0
    vehicleCap = vehicleCapacity[carNum]
    currentVehicleCargo = 0
    time = vehicleStartingTime[carNum]
    vehiclePlacement = vehicleStartingNode[carNum]

    for i in range(len(pickedUpItems)):
        node = pickedUpItems[i]
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
        callPoint = ((int(vehiclePlacement-1)*(int(numOfNodes) * int(numOfVehicles))) + int((callPlace[node-1]-1) * numOfVehicles) + (carNum))
        time += int(travelTimeAndCost[callPoint][3])
        travelCost += int(travelTimeAndCost[callPoint][4])
        left, right = callTime[node-1]
        if time > right:
            return False, 0
        elif time < left:
            time = left
        vehiclePlacement = travelTimeAndCost[callPoint][2]


        callPoint = (carNum * numOfCalls) + (node-1)
        time += dockingCostAndTime[callPoint][dockDelOrPick]
        if node not in visited:
            travelCost += dockingCostAndTime[callPoint][3]; travelCost += dockingCostAndTime[callPoint][5]
            visited.append(node)
    return True, travelCost