from model import *

def read(filename):
    with open(filename) as f:
        lines = [list(map(int, it.rstrip().split())) for it in f.readlines()]
        # R: number of rows
        # C: number of columns
        # F: number of vehicles
        # N: number of rides
        # B: bonus for starting on time
        # T: number of steps
        R, C, F, N, B, T = lines.pop(0)
        
        vehicles = []
        for vehicle in range(F):
            vehicles.append(Vehicle())
            vehicles[vehicle].id = vehicle
            
        rides = []
        for ride_id in range(N):
            # a: start row
            # b: start column
            # x: finish row
            # y: finish column
            # s: earliest start
            # f: latest finish
            a, b, x, y, s, f = lines.pop(0)
            start_pos = Point(row=a, column=b)
            end_pos = Point(row=x, column=y)
            ride = Ride(ride_id, start_pos, end_pos, s, f)
            rides.append(ride)
            
        return Simulator(vehicles, rides, B, T)

def write(simulator):
    with open('b_out.txt','w') as F:
        for vehicle in simulator.vehicles:
            rides = ' '.join([str(it.id) for it in vehicle.scheduled_rides])
            line = str(len(vehicle.scheduled_rides)) + ' ' + rides + '\n'
            F.write(line)
