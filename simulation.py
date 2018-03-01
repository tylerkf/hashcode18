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
            print("fucked it")
            return
        start_pos = [vals[0], vals[1]]
        end_pos   = [vals[2], vals[3]]
        start_time= vals[4]
        end_time  = vals[5]

rides = [0] * paramsData[3]
grid = Grid(paramsData,ridesData)


