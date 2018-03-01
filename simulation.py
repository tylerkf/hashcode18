
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
                

rides = [0] * paramsData[3]
grid = Grid(paramsData,ridesData)
vehicles = [Vehicle(i) for i in range(paramsData[2])]

def simulate(rides,grid,vehicles,schedule):
    score = 0

    # Setting up each vehicle
    for vehicleId in range(0,len(vehicles)):
        vehicleSchedule = schedule[vehicleId]
        M = vehicleSchedule[0]
        for i in range(1,M+1):
            vehicles[vehicleId].assign(rides[vehicleSchedule[i]])

    
    for t in range(0,grid.max_time): # Time step
        for vehicleId in range(0,len(vehicles)):
            score += vehicles[vehicleId].step(t)

    print(score)

sch = [[2,0,2],[1,1]]
for j in range(2,F):
    sch[j] = [0]
               
simulate(rides,grid,vehicles,sch)
            
            



