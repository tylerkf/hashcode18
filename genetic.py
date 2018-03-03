import numpy as np
import random
from random import randint

f = open("a_example.in", "r", encoding="utf-8")
first = True
paramsData = list(map(int,f.readline().split(' '))) # R,C,F,N,B,T
B = paramsData[4]
F = paramsData[2]
ridesData = [] # Rides input data
for line in f:
        ridesData.append(list(map(int,line[:-1].split(' '))))

class Grid:
    def __init__(self, vals, lines):
        self.rows = vals[0]
        self.columns = vals[1]
        self.vehicles = vals[2]
        self.num_rides = vals[3]
        self.bonus = vals[4]
        self.max_time = vals[5]
        for line_no in range(0,self.num_rides):
            rides[line_no] = Ride(lines[line_no])


class Ride:
    def __init__(self, vals):
        if(len(vals)!=6):
            print("bad")
            return
        self.start_pos = [vals[0], vals[1]]
        self.end_pos  = [vals[2], vals[3]]
        self.start_time = vals[4]
        self.end_time  = vals[5]
    def distance(self):
        return abs(self.start_pos[0]-self.end_pos[0])+abs(self.start_pos[1]-self.end_pos[1])

class Vehicle:
    def __init__(self,id):
        self.id = id
        self.assignedRides = []
        self.currentRideId = 0
        self.pos = [0,0]
        self.scoreCache = 0

        self.intentState = 2 # 0 = Going to start, 1 = Going to end, 2 = Waiting, 3 = Done
        self.movementState = 0 # 0 = Going across, 1 = Going vertical

    def assign(self,ride):
        self.assignedRides.append(ride)

    def nextT(self,currentTime):
        self.currentRideId += 1
        if self.currentRideId == len(self.assignedRides):
            self.intentState = 3
        else:
            target = self.assignedRides[self.currentRideId].start_pos
            if self.pos == target:
                self.intentState = 1
            else:
                self.intentState = 0

            # Check whether to wait on or discard current ride
            ride = self.assignedRides[self.currentRideId]

            if currentTime < ride.start_time:
                self.intentState = 2

            if currentTime > ride.end_time - ride.start_time:
                self.nextT(currentTime)

    def step(self,currentTime):
        if currentTime == 0:
            if len(self.assignedRides) == 0:
                self.intentState = 3
                return 0
        target = []
        if self.intentState == 0:
            target = self.assignedRides[self.currentRideId].start_pos
        elif self.intentState == 1:
            target = self.assignedRide[self.currentRideId].end_pos
        elif self.intentState == 2:
            ride = self.assignedRides[self.currentRideId]
            if currentTime == ride.start_time:
                self.intentState = 0
                self.scoreCache += B
                self.step(currentTime)
                return 0
            return 0
        else:
            return 0

        # Going across so move across
        done = False
        if self.movementState == 0:
            if self.pos[0]<target[0]:
                self.pos[0] += 1
            else:
                self.pos[0] -= 1

            # Check
            if self.pos == target:
                done = True
            elif self.pos[0] == target[0]:
                self.movementState == 1

        # Going vertical so move up or down
        else:
            if self.pos[1]<target[1]:
                self.pos[1] += 1
            else:
                self.pos[1] -= 1

            # Check
            if self.pos == target:
                done = True

        if done:
            # Return a score
            self.scoreCache += self.assignedRides[self.currentRideId].distance()
            self.nextT(currentTime)
            temp = self.scoreCache
            self.scoreCache = 0
            return(temp)

        return 0

def simulate(rides,grid,vehicles,schedule):
    score = 0
    print("Schedule:  ", schedule)
    # Setting up each vehicle
    for vehicleId in range(0,len(vehicles)):
        vehicleSchedule = schedule[vehicleId]
        M = vehicleSchedule[0]
        print("M: ", M)
        for i in range(1,M+1):
                print(i)
                vehicles[vehicleId].assign(rides[vehicleSchedule[i]])

    for t in range(0,grid.max_time): # Time step
        for vehicleId in range(0,len(vehicles)):
            score += vehicles[vehicleId].step(t)

    print(score)

def fitness(sol, rides, grid, vehicles):
    return simulate(rides,grid,vehicles,sol)

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

def naiive_solution(rides, grid):
        vehicle_rides = []
        for i in range(grid.vehicles):
                vehicle_rides.append([])
        for i in range(0,grid.num_rides):
                vehicle_rides[randint(0, grid.vehicles-1)].append(i)
        for i in range(0,grid.vehicles):
                vehicle_rides[i].insert(0, len(vehicle_rides[i]))
        return vehicle_rides

def main(rides, grid, vehicles, numNodes, numRoutes):
    NUM_MAX = 5
    solutions = []
    for i in range(0, grid.num_rides):
            solutions.append(naiive_solution(rides, grid))
    while True:
        fitnesses = []
        for s in solutions:
           fitnesses.append(fitness(s, rides, grid, vehicles))
        npFitnesses = np.array(fitnesses)

        best = []
        for i in range(0, NUM_MAX):
            curMax = np.append(np.argmax(npFitnesses))
            npFitnesses[curMax] = 0
            best.append(curMax)
        print(npFitnesses[best[0]])
        print(solutions[best[0]])

        offspring = []
        for i in range(0, NUM_MAX):
            for j in range(i, NUM_MAX):
                offspring.append(cnxCrossover([], [], numNodes, numRoutes + 1))
        solutions = offspring

rides = [0] * paramsData[3]
grid = Grid(paramsData,ridesData)
vehicles = [Vehicle(i) for i in range(paramsData[2])]
main(rides, grid, vehicles, paramsData[3], paramsData[2])
#print(naiive_solution(rides, grid))
