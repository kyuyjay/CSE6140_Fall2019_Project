import sys
import argparse
import random
import time
import numpy as np
import glob
import csv

######## Algorithm Modules ########

# Import your algorithm modules here

import genetic

######## ################# ########

options = {}
options["cutoff"] = 10
options["seed"] = None

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

def write_file(results):
    with open("results/genetic_eval_med.csv","a") as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in results:
            csvwriter.writerow(row)

######## ############## ########  

######## Driver Program ########

trials = 40
results = []
local = []

def runtime(results):
    for file_loc in glob.glob("DATA/*.tsp"):
        print(file_loc)
        local_time = 0
        local_qual = 0
        for i in range(trials):
            start_time = time.time()
            random.seed(options["seed"])
            params,cities = read_file(file_loc)
            g = genetic.genetic(params,cities,options["cutoff"])
            trace,quality,route = g.evolve()
            local_time = local_time + trace[-1][0]
            local_qual = local_qual + quality
        results.append([file_loc.strip("DATA/"), local_time/trials, local_qual/trials])
        print(results)

def cv(results):
    for file_loc in glob.glob("DATA/Atlanta.tsp"):
        print(file_loc)
        for p in range(100,1000,150):
            for e in range(0,20,5):
                #for m in range(0,20,5):
                for m in range(1):
                    m = 20
                    local_time = 0
                    local_qual = 0
                    for i in range(trials):
                        start_time = time.time()
                        random.seed(options["seed"])
                        params,cities = read_file(file_loc)
                        g = genetic.genetic(params,cities,options["cutoff"],pop=p,elite=e/100,mutate=m/100)
                        trace,quality,route = g.evolve()
                        local_time = local_time + trace[-1][0]
                        local_qual = local_qual + quality
                    results.append([p, e/100, m/100, local_time/trials, local_qual/trials])
                    print(results)

def qrtd(results):
    for file_loc in ["DATA/Atlanta.tsp"]:
        for i in range(trials):
            temp = []
            start_time = time.time()
            random.seed(options["seed"])
            params,cities = read_file(file_loc)
            g = genetic.genetic(params,cities,60)
            trace,quality,route = g.evolve()
            results.append([quality])
            print(results)

def qrtd2(results2):
    for file_loc in ["DATA/NYC.tsp"]:
        for i in range(trials):
            temp = []
            start_time = time.time()
            random.seed(options["seed"])
            params,cities = read_file(file_loc)
            g = genetic.genetic(params,cities,125)
            trace,quality,route = g.evolve()
            results2.append([quality])
            print(results2)

qrtd(results)
results2 = []
qrtd2(results)
write_file(results)

######## ############## ########  
