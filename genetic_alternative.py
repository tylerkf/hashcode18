import numpy as np
import random
import math
import simulation as sim

def naiive_solution(inSubmissionFormat):
    vehicle_rides = [[] for v in range(sim.Simulator.F)]
    for i in range(0,sim.Simulator.N):
        vehicle_rides[random.randint(0, sim.Simulator.F-1)].append(i)
    if inSubmissionFormat:
        for i in range(0,sim.Simulator.F):
            vehicle_rides[i].insert(0, len(vehicle_rides[i]))
    return vehicle_rides

def crossover(sol1, sol2):
    sol = []

    taken = []
    for j in range(len(sol1)):
        r1 = sol1[j]
        r2 = sol2[j]

        currentLength = 0
        for k in min()

    return sol1

def main(n,epochs):
    solutionPool = []
    for i in range(n):
        solutionPool.append(naiive_solution(False))

    nextEpoch = []
    for epoch in range(epochs):
        bestScoreEpoch = 0
        while True:
            sol1 = solutionPool[0]

            targetScore = sim.simulate(sol1, False)

            bestScore = targetScore
            bestSolIndex = 0
            index = 1
            while index < len(solutionPool):
                proposedSol = crossover(sol1,solutionPool[index])
                givenScore = sim.simulate(proposedSol, False)

                if givenScore > bestScore:
                    bestScore = givenScore
                    bestSolIndex = index

                index += 1

            nextEpoch.append(solutionPool.pop(0))
            if bestSolIndex != 0:
                nextEpoch.append(solutionPool.pop(bestSolIndex - 1))

            if bestScore > bestScoreEpoch:
                bestScoreEpoch = bestScore

            if len(solutionPool) < 2:
                break

        solutionPool = list(nextEpoch)
        nextEpoch = []
        print("n:", len(solutionPool))
        print("best score on epoch", epoch+1, "was", bestScoreEpoch)

sim.loadProblem("problems/b_should_be_easy.in")
main(100,10)
