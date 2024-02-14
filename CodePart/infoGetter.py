import os
import numpy as np

def problemData(filename):

    vehicleInfo = []
    callInfo = []
    vehicleCapability = []
    travelTimeAndCost = []
    dockingCostAndTime = []

    with open(filename, "r") as f:
        lines = f.readlines()
        numOfNodes = int(lines[1])
        numOfVehicles = int(lines[3])
        numOfCalls = int(lines[6+numOfVehicles])

        for line in lines[5:(5+numOfVehicles)]:
            vehicleInfo.append(line.split(","))

        for line in lines[(8+numOfVehicles): (8+(numOfVehicles*2))]:
            line = line.split(",")
            for i in range(0, len(line)):
                line[i] = int(line[i])
            vehicleCapability.append(line)

        for line in lines[(9+(numOfVehicles*2)):(9+(numOfVehicles*2)+numOfCalls)]:
            callInfo.append(line.split(","))

        for line in lines[(10 + (numOfVehicles*2) + numOfCalls):(10 + (numOfVehicles*2) + numOfCalls+(numOfNodes*numOfNodes*numOfVehicles))]:
            line = line.split(",")
            for i in range(0, len(line)):
                line[i] = int(line[i])
            travelTimeAndCost.append(line)
        
        for line in lines[(11+(numOfVehicles*2) + numOfCalls+(numOfNodes*numOfNodes*numOfVehicles)):(11+(numOfVehicles*2) + numOfCalls+(numOfNodes*numOfNodes*numOfVehicles)+(numOfVehicles*numOfCalls))]:
            line = line.split(",")
            for i in range(0, len(line)):
                line[i] = int(line[i])
            dockingCostAndTime.append(line)
        
        f.close()

    vehicleCapacity = np.zeros(numOfVehicles)
    vehicleStartingTime = np.zeros(numOfVehicles)
    vehicleStartingNode = np.zeros(numOfVehicles)
    vehicleInfo = np.array(vehicleInfo, dtype=np.int64)

    callOrigin = np.zeros(numOfCalls)
    callDestination = np.zeros(numOfCalls)
    callSize = np.zeros(numOfCalls)
    callPenalty = np.zeros(numOfCalls)  # Cost of not transporting
    # Pick up time stored as a tuple with lower and upperbound (LB, UB)
    callPickupTimes = np.zeros(numOfCalls, dtype = [('x', 'int'), ('y','int')])
    # Same as above but for delivery time instead
    callInfo = np.array(callInfo, dtype=np.int64)
    callDeliveryTimes = np.zeros(numOfCalls, dtype = [('x', 'int'), ('y','int')])   

    # This is the list of which deliveries the different cars can do
    # vehicleCapability = np.array(vehicleCapability, dtype=object)  

    # travelTimeAndCost = np.array(travelTimeAndCost, dtype=np.int64) 

    # dockingCostAndTime = np.array(dockingCostAndTime, dtype=np.int64)

    for i in range(numOfVehicles):
        vehicleCapacity[i] = int(vehicleInfo[i,3])
        vehicleStartingTime[i] = int(vehicleInfo[i,2])
        vehicleStartingNode[i] = int(vehicleInfo[i,1])

    for i in range(numOfCalls):
        callOrigin[i] = int(callInfo[i,1])
        callDestination[i] = int(callInfo[i,2])
        callSize[i] = int(callInfo[i,3])
        callPenalty[i] = int(callInfo[i,4])
        callPickupTimes[i] = (int(callInfo[i,5]), int(callInfo[i,6]))
        callDeliveryTimes[i] = (int(callInfo[i,7]), int(callInfo[i,8]))

    output = {
        "NumOfVehicles" : numOfVehicles,
        "NumOfNodes" : numOfNodes,
        "NumOfCalls" : numOfCalls,
        "VehicleCapacity": vehicleCapacity,
        "VehicleStartingTime": vehicleStartingTime,
        "VehicleStartingNode": vehicleStartingNode,
        "CallOrigin": callOrigin,
        "CallDestination": callDestination,
        "CallSize": callSize,
        "CallPenalty": callPenalty,
        "CallPickUpTimes": callPickupTimes,
        "CallDeliveryTimes": callDeliveryTimes,
        "VehicleCapabilities" : vehicleCapability,
        "Travel Time and Cost" : travelTimeAndCost,
        "Docking Cost and Time" : dockingCostAndTime,
    }

    return output