import numpy as np
import math, random, time


"""
Simulated Annealing algorithm
input object format: np.array with 3 columns:
point_index, x_pos, y_pos
example:
[['1' 37252471.0 -79951871.0]
 ['2' 37279602.0 -79935901.0]
 ['3' 37265971.0 -79945038.0]...]
 
cooling rate default is 0.001
It will enable the algorithm running for 100 times. 
It can be also passed via arguments. 
"""


class SimulatedAnnealing(object):
    def __init__(self, all_points, cooling_rate=0.001):
        self.all_points = all_points
        self.Temp = 10000
        self.cooling_rate = cooling_rate
        self.best_solution = None
        self.best_distance = float("inf")
        self.best_route = []
        self.trace = []

    def initial_solution(self):
        """
        :return: create a random solution
        """
        new_array = np.copy(self.all_points)
        np.random.shuffle(new_array)
        return new_array

    def distance_to(self, point1, point2):
        """
        :return: get the distance between two points
        """
        distance = 0
        xdist = abs(point1[1] - point2[1])
        ydist = abs(point1[2] - point2[2])
        distance = math.sqrt(xdist * xdist + ydist * ydist)
        return distance

    def get_distance(self, arr):
        """
        :return: total distance of the route
        """
        distance = 0
        n_rows = arr.shape[0]
        for i in range(1, n_rows):
            distance += self.distance_to(arr[i, :], arr[i-1, :])

        # add the distance come from the last point to the origin point
        distance += self.distance_to(arr[n_rows-1, :], arr[0, :])
        return distance

    def swap_points(self, arr):
        """
        :return: swap two points to generate the neighbor solution
        """
        new_arr = np.copy(arr)
        rand_data = random.sample(range(0, new_arr.shape[0]), 2)
        x = rand_data[0]
        y = rand_data[1]
        new_arr[[x, y]] = new_arr[[y, x]]
        return new_arr

    def acceptance_probability(self, curr_dist, new_dist):
        """
        :return: if new distance < old distance, return 1.0;
        if new distance > old distance, return exp^((old - new)/T)
        """
        if new_dist < curr_dist:
            return 1.0
        else:
            return math.exp((curr_dist - new_dist)/self.Temp)

    def convert_route(self, arr):
        """
        :return: return a list with the sequenced indexes for each point
        """
        best_route = []
        for i in range(arr.shape[0]):
            best_route.append(int(arr[i, 0]))
        return best_route

    def anneal(self,cutoff):
        """
        :return: Annealing till cool down, update the best_solution
        """
        # Program timer
        start_time = time.time()

        # Random initiate the current solution and best solution
        current_solution = self.initial_solution()
        self.best_solution = np.copy(current_solution)


        while self.Temp > 1:
            # timer for each iteration
            itr_time = time.time()

            # get new solution by swap two points in the current solution
            new_solution = self.swap_points(current_solution)

            # get the distance
            current_dist = self.get_distance(current_solution)
            new_dist = self.get_distance(new_solution)

            # Decide if the neighbour is accepted
            accept_probability = self.acceptance_probability(current_dist, new_dist)
            if accept_probability > random.random():
                current_solution = new_solution
                # if accept the new solution, compare to best solution, decide whether update the best solution
                if self.get_distance(current_solution) < self.get_distance(self.best_solution):
                    self.best_solution = current_solution
                    self.best_distance = int(self.get_distance(self.best_solution))
                    # calculate time
                    current_time = time.time()
                    elapsed = current_time - start_time
                    self.trace.append([elapsed, self.best_distance])
                
            self.Temp *= (1-self.cooling_rate)

            # cutoff the program if the time left to cutoff is less than the time for one more iteration
            if (cutoff - 0.5 - (time.time() - start_time)) < (time.time() - itr_time):
                self.best_route = self.convert_route(self.best_solution)
                return

        self.best_route = self.convert_route(self.best_solution)



