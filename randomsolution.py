#!/bin/python

from random import randint
f = open("b_should_be_easy.in", "r", encoding="utf-8")
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

rides = [0] * paramsData[3]
grid = Grid(paramsData,ridesData)
#simulate(rides,grid,vehicles,0)
def naiive_solution():
        rc = []
        vehicle_rides = []
        for i in range(grid.vehicles):
                vehicle_rides.append([])      
        for i in range(0,grid.num_rides):
                vehicle_rides[randint(0, grid.vehicles-1)].append(i)
        for i in vehicle_rides:
                lin = str(len(i))
                for j in range(0, len(i)):
                        lin+=" "+str(i[j])
                        print(lin)
                        rc.append(lin)
        return rc
naiive_solution()
