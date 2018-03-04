from collections import namedtuple
from heur import *

Point = namedtuple("Point", ["row", "column"])


class Vehicle:
    def __init__(self):
        self.initial_pos = Point(0,0)
        self.scheduled_rides = []
        self.unavailable_until = 0
        self.id = None
        self.never_possible = False
        self.wagi =[]
        self.current_pos = self.initial_pos


class Ride:
    def __init__(self, id, start_pos, end_pos, earliest_start, latest_finish):
        self.id = id
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.earliest_start = earliest_start
        self.latest_finish = latest_finish
        self.available = True
        self.wage = None


class Simulator:
    def __init__(self, vehicles, rides, bonus, steps):
        self.vehicles = vehicles
        self.rides = rides
        self.bonus = bonus
        self.steps = steps

    def RidesWages(self):
        for ride in self.rides:
            mins =[]
            for ride2 in self.rides:
                if ride.id != ride2.id:
                    mins.append(abs(ride.end_pos.row - ride2.start_pos.row) + abs(ride.end_pos.column - ride2.start_pos.column))
            ride.wage = min(mins)
            print(ride.id, ride.wage)

    def daniel_simulate(self):
        score = 0
        step = 0
        self.RidesWages()
        while step < self.steps:

            if GetAllAvailableVehicles(self.vehicles,step) == []:
                possibleDate = GetDateOfNextAvailable(self.vehicles)
                if possibleDate: step = possibleDate
                else: return score

            print(step, 'score:',score)

            for vehicle in self.vehicles:
                vehicle.wagi = []
                if vehicle.unavailable_until <= step:
                    for ride in self.rides:
                        if ride.available:
                            if IsRidePossible(
                                vehicle.current_pos.row, vehicle.current_pos.column,
                                ride.start_pos.row, ride.start_pos.column, 
                                ride.end_pos.row, ride.end_pos.column,
                                ride.latest_finish, step):

                                pts, realpoints, finish_time_ride = CalculatePoints(
                                        ride.start_pos.row, ride.start_pos.column,
                                        ride.end_pos.row, ride.end_pos.column,
                                        vehicle.current_pos.row, vehicle.current_pos.column,
                                        step, ride.earliest_start,self.bonus,ride.wage,step, ride.id,score)
                                vehicle.wagi.append({'id':ride.id, 'pts':pts, 'realpts':realpoints,'finish':finish_time_ride})
                    
                    max_ride = max(vehicle.wagi, key=lambda it: it['pts'], default=None)
                    if max_ride:
                        picked_ride = self.rides[max_ride['id']]
                        score += max_ride['realpts']
                        print('assigned', picked_ride.id)
                        vehicle.scheduled_rides.append(picked_ride)
                        picked_ride.available = False
                        vehicle.unavailable_until = max_ride['finish']
                        vehicle.current_pos= Point(picked_ride.end_pos.row, picked_ride.end_pos.column)
                    else: vehicle.never_possible = True

        step+=1
        return score

