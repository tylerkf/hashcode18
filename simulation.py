
f = open("a_example.in", "r", encoding="utf-8")
first = True
paramsData = list(map(int,f.readline().split(' '))) # R,C,F,N,B,T
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
        start_pos = [vals[0], vals[1]]
        end_pos   = [vals[2], vals[3]]
        start_time= vals[4]
        end_time  = vals[5]
    def distance(self):
        return abs(start_pos[0]-end_pos[0])+abs(start_pos[1]-end_pos[1])

class Vehicle:
    def __init__(self,id):
        self.id = id
        self.assignedRides = []
        self.currentRideId = 0
        self.pos = [0,0]

        self.intentState = 2 # 0 = Going to start, 1 = Going to end, 2 = Waiting, 3 = Done
        self.movementState = 0 # 0 = Going across, 1 = Going vertical

    def assign(self,ride):
        self.assignedRides.append(ride)

    def next(self,ride):
        self.assignedRide = ride
        if self.pos == ride.start_pos:
            self.intentState = 1
        else:
            self.intentState = 0
            if self.pos[0] != ride.start_pos[0]:
                self.movementState = 0
            else:
                self.movementState = 1

    def step(self,currentTime):
        target = []
        if self.intentState == 0:
            target = self.assignedRides[currentRideId].start_pos
        elif self.intentState == 1:
            target = self.assignedRide[currentRideId].end_pos
        elif self.intentState = 2:
            # Check if start next ride
        else:
            return

        # Going across so move across
        if self.movementState == 0:
            if self.pos[0]<target[0]:
                self.pos[0] += 1
            else:
                self.pos[0] -= 1

            # Check    
            if self.pos == target:
                self.intentState == 2
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
                self.intentState == 2
                

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
            vehicles[vehicleId].step(t)
            
               
simulate(rides,grid,vehicles,0)
            
            



