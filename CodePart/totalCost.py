def costFinder(solution, callPenalty):
    totalCost = 0
    covered = []
    for outsourced in solution[-1]:
        if outsourced not in covered:
            covered.append(outsourced)
            totalCost += callPenalty[outsourced-1]
    return totalCost
