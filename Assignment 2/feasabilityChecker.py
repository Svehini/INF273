from infoGetter import *
import numpy as np

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
    vehicleCapabilities = data["VehicleCapabilities"]
    travelTimeAndCost = data["Travel Time and Cost"]
    dockingCostAndTime = data["Docking Cost and Time"]


    solCopy = solution
    solCopyDict = {}
    for i in solCopy:
        if i != 0:
            if i not in solCopyDict.keys():
                solCopyDict[i] = 1
            elif solCopyDict[i] < 2:
                solCopyDict[i] = solCopyDict[i]+1
            else:
                # print(f"There is more than two mentions of item {i}")
                return False, 0
    if len(solCopyDict.keys())*2 != sum(solCopyDict.values()):
        # print(f"There is not an equal amount of pickups and deliveries!!")
        return False, 0
    

    pickedUp = []
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

            if node not in vehicleCapabilities[vehicleNum]:
                # print(f"This car {vehicleNum+1}, cannot deliver package {node}!")
                return False, 0
            
            if node not in pickedUp:
                pickedUp.append(node)
                if currentVehicleCargo + callSize[node-1] > vehicleCap:
                    # print(f"Car is too full to pick up this package")
                    return False, 0
                currentVehicleCargo += callSize[node-1]
                callPlace = callOrigin
                callTime = callPickupTimes
                delOrPick = "PICK UP"
                dockDelOrPick = 2
            else:
                pickedUp.remove(node)
                currentVehicleCargo -= (callSize[node-1])
                callPlace = calldestination
                callTime = callDeliveryTimes
                delOrPick = "DELIVER"
                dockDelOrPick = 4
            # print(f"Current weight is: {currentVehicleCargo}")

            # Checks the delivery time and makes sure it is not too late, and makes the car wait until LB constraint is met
            factor = int(numOfNodes) * int(numOfVehicles)
            for callPoint in range((int(vehiclePlacement-1)*factor), ((int(vehiclePlacement)) * factor)):
                if (travelTimeAndCost[callPoint][2] == callPlace[node-1]) and (travelTimeAndCost[callPoint][0] == vehicleNum+1):
                    time += int(travelTimeAndCost[callPoint][3])
                    travelCost += int(travelTimeAndCost[callPoint][4])
                    left, right = callTime[node-1]
                    if time > right:
                        # print(f"You are too late to {delOrPick} package {node} !!")
                        # print(f"VehicleNum {vehicleNum}")
                        return False, 0
                    elif time < left:
                        time = left
                    vehiclePlacement = travelTimeAndCost[callPoint][2]
                    # print(travelTimeAndCost[callPoint][1])
                    break

            for callPoint in range((vehicleNum * numOfCalls), ((vehicleNum+1) * numOfCalls)):
                if dockingCostAndTime[callPoint][1] == node:
                    time += dockingCostAndTime[callPoint][dockDelOrPick]
                    if time > right:
                        # print(f"You didnt finish docking before the time ran out!")
                        return False, 0


        else:
            if pickedUp != []:
                # print("Some car picked up a package but didnt deliver it!")
                # print(f"{pickedUp}")
                return False, 0
            vehicleNum += 1
            if (vehicleNum+1) > numOfVehicles:
                # print(f"Rest is delivered by renting another company to deliver.")
                # print(f"These packages are {solution[i+1:]}")
                break
            vehicleCap = vehicleCapacity[vehicleNum]
            currentVehicleCargo = 0
            pickedUp = []                               # Which packages the given vehicle has picked up
            time = vehicleStartingTime[vehicleNum]      # The time of the vehicle
            vehiclePlacement = vehicleStartingNode[vehicleNum]
            # print(f"\n\n")
            # print(f"VehicleNum is {vehicleNum}, \nTime is {time}, \nVehicleplacement is {vehiclePlacement}")


    # print("Its all good!")
    return True, travelCost