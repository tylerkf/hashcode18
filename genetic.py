import numpy as np
import random

def fitness(r):
    return 1

def fitnessMany(r):
    return 1

def nodesToArcs(route):
    nLast = -1
    arcs = []
    for n in route:
        if (nLast != -1):
            arcs.append([nLast, n])
        nLast = n
    return arcs

def getArcTrail(arcs, added, notInSolution, node):
    print(added)
    print(notInSolution)
    nextNode = -1
    for a in arcs:
        if a[0] == node:
            nextNode = a[1]
        elif a[1] == node:
            nextNode = a[0]
        else:
            continue
        if nextNode not in notInSolution:
            nextNode = -1
            continue
        arcs.remove(a)
        added.append(nextNode)
        break
    if nextNode == -1:
        return added
    return getArcTrail(arcs, added, notInSolution, nextNode)

def cnxCrossover(sol1, sol2, numNodes, numRoutes):
    # CNX CROSSOVER
    sol1Arcs = []
    sol2Arcs = []
    for r in sol1:
        sol1Arcs = sol1Arcs + nodesToArcs(r)
    for r in sol2:
        sol2Arcs = sol2Arcs + nodesToArcs(r)
    spareNodes = []
    offspringArcs = []

    for a in sol1Arcs:
        if a in sol2Arcs or [a[1], a[0]] in sol2Arcs:
            offspringArcs.append(a)
        else:
            spareNodes.append(a[0])

    spareNodes.remove(0)

    # RANDOMLY BUILDING SOLUTION
    # creates routes from 0 arcs
    sol = []
    notInSolution = list(range(1, numNodes))
    for a in offspringArcs:
        nextNode = -1
        if a[0] == 0:
            nextNode = a[1]
        elif a[1] == 0:
            nextNode = a[0]
        else:
            continue
        notInSolution.remove(nextNode)
        routeStart = [0, nextNode]
        added = getArcTrail(offspringArcs, [], notInSolution, nextNode)
        routeStart = routeStart + added
        sol.append(routeStart)

        for n in added:
            notInSolution.remove(n)

    if len(notInSolution) == 0:
        return sol

    for i in range(len(sol), numRoutes):
        node = random.choice(notInSolution)
        routeStart = [0, node]
        notInSolution.remove(node)
        added = getArcTrail(offspringArcs, [], notInSolution, node)
        routeStart = routeStart + added
        sol.append(routeStart)
        for n in added:
            notInSolution.remove(n)

    # gets rid of remaining nodes
    print("removing remaining nodes")
    randoms = np.random.randint(0, numRoutes, len(sol))
    i = 0
    while len(notInSolution) > 0:
        node = random.choice(notInSolution)
        added = getArcTrail(offspringArcs, [node], notInSolution, node)
        sol[randoms[i]] = sol[randoms[i]] + added
        for n in added:
            notInSolution.remove(n)
        i = (i + 1) % numRoutes

    return sol

def selection(routes, fitness, min):
    newRoutes = routes[fitness > min]
    return newRoutes

def main():
    sol1 = [
        [0, 2, 1, 3],
        [0, 4, 5, 6],
        [0, 8, 9, 10]
    ]
    sol2 = [
        [0, 8, 4, 3],
        [0, 1, 9, 5],
        [0, 2, 6, 7]
    ]
    print(cnxCrossover(sol1, sol2, 9, 3))



if __name__ == '__main__':
    main()
