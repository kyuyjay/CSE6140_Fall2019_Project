import sys
import argparse
import random
import numpy as np
from genetic import genetic

######## Command Line Arguments ########

parser = argparse.ArgumentParser(description="TSP")
parser.add_argument("-inst",dest="file_loc")
parser.add_argument("-alg",dest="method")
parser.add_argument("-time",dest="cutoff",type=int)
parser.add_argument("-seed")
options = parser.parse_args()

######## ###################### ########

######## Classes #########

class City:
    def __init__(self,node_id,x,y):
        self.node_id = node_id
        self.x = x
        self.y = y

    def test(self):
        print("hello")

######## ####### #########

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
            cities.append(City(int(line[0]),float(line[1]),float(line[2])))
    return params,cities

def write(trace,quality,route,params,options):
    file_loc = "{}_{}_{}.sol".format(params["NAME"],options.method,options.cutoff)
    with open(file_loc,"w+") as out:
        out.write("{}\n".format(quality))
        for city in route[0:-1]:
            out.write("{} ".format(city))
        out.write("{}\n".format(route[-1]))
    file_loc = "{}_{}_{}.trace".format(params["NAME"],options.method,options.cutoff)
    with open(file_loc,"w+") as out:
        for log in trace:
            out.write("{:.2f} {}\n".format(log[0],log[1]))

######## ############## ########  

######## Driver Program ########

params,cities = read_file(options.file_loc)
print(params)
for city in cities:
    print("{} {} {}".format(city.node_id,city.x,city.y))
if options.method == "BnB":
    # TODO
    pass
elif options.method == "Approx":
    # TODO
    pass
elif options.method == "LS1":
    # TODO
    pass
elif options.method == "LS2":
    trace,quality,route = genetic(params,cities,options.cutoff)

print(quality)
for id in route:
    print(id,end=" ")
print("")

write(trace,quality,route,params,options)

######## ############## ########  
