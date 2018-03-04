
class Simulator:
    # Problem Parameters
    R = 0 # Number of rows in Grid
    C = 0 # Number of columns in Grid
    F = 0 # Number of vehicles in fleet
    N = 0 # Number of rides
    B = 0 # Per ride bonus for starting the ride on time
    T = 0 # Number of steps in simulation

    # Array storing rides
    rides = []


# Loads in problem parameters and rides
def loadProblem(filename):
    f = open(filename, "r", encoding="utf-8")

    # Loading parameters
    paramsData = list(map(int,f.readline().split(' '))) # R,C,F,N,B,T
    Simulator.R = paramsData[0]
    Simulator.C = paramsData[1]
    Simulator.F = paramsData[2]
    Simulator.N = paramsData[3]
    Simulator.B = paramsData[4]
    Simulator.T = paramsData[5]

    # Loading rides
    Simulator.rides = [0] * Simulator.N
    for i in range(0,Simulator.N):
        raw = list(map(int,f.readline()[:-1].split(' ')))
        ride = []
        ride.append([raw[0],raw[1]]) # Start coords
        ride.append([raw[2],raw[3]]) # End coords
        ride.append(raw[4]) # Earliest start
        ride.append(raw[5]) # Latest finish

        Simulator.rides[i] = ride;

# Scores given solution
def simulate(solution, inSubmissionFormat):
    score = 0

    if len(solution) > Simulator.F:
        print("That many taxis does not exist!")
        print(Simulator.F,"<", len(solution))

    if len(solution) < Simulator.F:
        print("Note that the problem allows", Simulator.F, "taxis but the given solution only utilises", len(solution))

    for i in range(0, min(Simulator.F,len(solution))):
        schedule = 0
        if inSubmissionFormat:
            schedule = solution[i][1:]
        else:
            schedule = solution[i]

        t = 0
        pos = [0,0]
        for j in range(0, len(schedule)):
            if schedule[j] >= Simulator.N:
                print("Tried to get ride that doesn't exist", schedule[j], ">= N", Simulator.N)
                continue
            ride = Simulator.rides[schedule[j]]

            # Coordinates
            start = ride[0]
            end = ride[1]

            # Times
            earliest = ride[2]
            latest = ride[3]

            journey_length = abs(start[0] - end[0]) + abs(start[1] - end[1])
            start_length = abs(pos[0] - start[0]) + abs(pos[1] - start[1])
            total_length = start_length + journey_length

            end_t = max(earliest + journey_length - 1, t + total_length - 1)

            if end_t >= Simulator.T:
                continue

            if end_t <= latest:
                score += journey_length

                if t + start_length - 1 <= earliest:
                    score += Simulator.B

                t = end_t
                pos = end

    return(score)
