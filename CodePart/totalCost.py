import numpy as np

def costFinder(solution, data):
    numOfVehicles = data['NumOfVehicles']
    numOfCalls = data["NumOfCalls"]
    callPenalty = data["CallPenalty"]
    dockingCostAndTime = data["Docking Cost and Time"]

    totalCost = 0
    vehicleNum = 0

    visited = []
    for i in range(len(solution)):
        node = solution[i]
        if node != 0:
            if node not in visited:
                visited.append(node)
                for j in range((vehicleNum*numOfCalls), ((vehicleNum+1) * numOfCalls)):
                    if dockingCostAndTime[j][1] == node:
                        totalCost += (dockingCostAndTime[j][3] + dockingCostAndTime[j][5])
                        break
        else:
            vehicleNum += 1
            if (vehicleNum+1) > numOfVehicles:
                break
    covered = []
    # print(solution)
    for outsourced in solution[i+1:]:
        if outsourced not in covered:
            covered.append(outsourced)
            totalCost += callPenalty[outsourced-1]
            # print(totalCost)
            
    return totalCost
