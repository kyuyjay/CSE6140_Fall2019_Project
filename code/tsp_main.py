import sys
import os
import argparse
import random
import time
import numpy as np

######## Algorithm Modules ########

# Import your algorithm modules here

import genetic
import SA
import construction_heuristic
import BranchAndBound

######## ################# ########

######## Command Line Arguments ########

parser = argparse.ArgumentParser(description="TSP")
parser.add_argument("-inst",dest="file_loc")
parser.add_argument("-alg",dest="method")
parser.add_argument("-time",dest="cutoff",type=int)
parser.add_argument("-seed",dest="seed",type=int)
options = parser.parse_args()

######## ###################### ########

######## File Functions ########

def read_file(file_loc):
    cities = []
    params = {}
    with open(file_loc,"r") as inst:
        for line in inst:
            line = line.strip()
            if line != "NODE_COORD_SECTION":
                param = line.split(": ")
                params[param[0]] = param[1]
            else:
                break
        params["DIMENSION"] = int(params["DIMENSION"])
        for i in range(params["DIMENSION"]):
            line = inst.readline().split()
            cities.append([int(line[0]),float(line[1]),float(line[2])])
    return params,cities

def write(trace,quality,route,params,options):
    os.makedirs("output",exist_ok=True)
    file_loc = "output/{}_{}_{}.sol".format(params["NAME"],options.method,round(options.cutoff))
    # Write solution file
    with open(file_loc,"w+") as out:
        out.write("{}\n".format(quality))
        for city in route[0:-1]:
            out.write("{},".format(city))
        out.write("{}\n".format(route[-1]))
    # Write trace file
    file_loc = "output/{}_{}_{}.trace".format(params["NAME"],options.method,round(options.cutoff))
    with open(file_loc,"w+") as out:
        for log in trace:
            out.write("{:.2f}, {}\n".format(log[0],log[1]))

######## ############## ########  

######## Driver Program ########

start_time = time.time()
random.seed(options.seed)
params,cities = read_file(options.file_loc)
print(params)
for city in cities:
    print("{} {} {}".format(city[0],city[1],city[2]))

#### Algorithms ####

# Return the trace, quality, and route
# trace,quality,route = ALGO_METHOD(arg_1,arg_2,...)
# Trace: Array of best results found [[timestamp_1,quality_1],[timestamp_2,quality_2],...]
# Quality: Overall shortest tour found
# Route: Array of node_ids in order of travel [node_1,node_2,...]

if options.method == "BnB":
    branch=BranchAndBound.BranchAndBound(cities,options.cutoff)
    branch.main()
    quality = branch.minimum
    route = branch.bestSolution
    trace = branch.trace
    
elif options.method == "Approx":
    trace, quality, route = construction_heuristic.nearest_neighbor(params, cities, options.cutoff)
elif options.method == "LS1":
    s = SA.SimulatedAnnealing(cities, 0.00001)  # the second argument is the cooling rate, default is 0.001.
    s.anneal(options.cutoff)
    quality = s.best_distance
    route = s.best_route
    trace = s.trace
elif options.method == "LS2":
    g = genetic.genetic(params,cities,options.cutoff)
    trace,quality,route = g.evolve()

#### ########## ####

print(quality)
for id in route:
    print(id,end=" ")
print("")

write(trace,quality,route,params,options)

######## ############## ########  
