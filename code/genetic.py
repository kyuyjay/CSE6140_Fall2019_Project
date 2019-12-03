###
# Genetic algorithm to optimize travelling salesman problem.
# 
# To initialize algorithm, create a class genetic with the TSP parameters, data,
# and the required hyperparameters if not using the default.
#
# Call genetic.evolve() to run the algorithm. Returns trace, quality, route
##

import sys
import time
import random
import numpy as np

class genetic:
    # Main driver class to hold algorithm parameters
    def __init__(self,params,cities,cutoff,pop=250,elite=0.20,mutate=0.05):
        self.hyp = {
                "N": params["DIMENSION"],
                "POPULATION": pop,
                "ELITIST FACTOR": elite,
                "MUTATION": mutate,
                "GENERATIONS": 10000
                }
        self.hyp["ELITISM"] = int(round(self.hyp["ELITIST FACTOR"] * self.hyp["POPULATION"]))
        self.cities = cities
        self.cutoff = cutoff
        self.gene_pool = []
        self.mating_pool = []
        self.weights = []
        print("Hyperparameters")
        for param in self.hyp:
            print("{}: {}".format(param,self.hyp[param]))

    # Each gene represents a location from the TSP data
    class gene:
        def __init__(self,node_id=-1,x=0,y=0):
            self.node_id = node_id
            self.x = x
            self.y = y

        # Calculate the distance from this location to another location
        def distance(self,dest):
            return np.linalg.norm([dest.x - self.x,dest.y - self.y])

    # Each DNA is a valid solution to the TSP problem and is composed of N genes
    class DNA:
        def __init__(self,N,gene_pool):
            self.strand = random.sample(gene_pool,N)
            self.tour_length = 0
            self.N = N

        # Evaluates the tour length of the DNA and returns the recipocal as the solution
        def fitness(self):
            self.tour_length = 0
            for i in range(len(self.strand) - 1):
                self.tour_length = self.tour_length + self.strand[i].distance(self.strand[i+1])
            self.tour_length = int(round(self.tour_length + self.strand[-1].distance(self.strand[0])))
            return

        # Mutates each gene by swapping gene positions in the DNA with the given probability
        def mutate(self,N,MUTATION):
            for i in range(len(self.strand)):
                chance = random.random()
                if chance <= MUTATION:
                    swap = random.randrange(0,N)
                    self.strand[i],self.strand[swap] = self.strand[swap],self.strand[i]
            return

    # Create the initial population from the gene pool by generating DNA
    def populate(self):
        for i in range(self.hyp["POPULATION"]):
            self.mating_pool.append(self.DNA(self.hyp["N"],self.gene_pool))
            self.mating_pool[i].fitness()
            self.weights.append(1/self.mating_pool[i].tour_length)
        self.mating_pool.sort(key=lambda x: x.tour_length)
        return

    # Select 2 parents from the population with a weighted probability
    def select(self):
        parents = random.choices(self.mating_pool,weights=self.weights,k=2)
        return parents
 
    # Mate two DNA by selecting different portions of them while preserving the validity of the solution
    def crossbreed(self,host,partner):
        N = self.hyp["N"]
        start = random.randrange(0, round((N/2) - 1))
        child = self.DNA(self.hyp["N"],self.gene_pool)
        child.strand = host.strand[start:start + round(N/2)]
        node_id = list(map(lambda x: x.node_id,child.strand))
        for gene in partner.strand:
            if gene.node_id not in node_id:
                child.strand.append(gene)
        return child

    # Driver method to conduct selection and mating for the whole population
    def survive(self):
        N = self.hyp["N"]
        POPULATION = self.hyp["POPULATION"]
        ELITISM = self.hyp["ELITISM"]
        MUTATION = self.hyp["MUTATION"]
        next_gen = self.mating_pool[0:ELITISM]
        for i in range(POPULATION - ELITISM):
            parents = self.select()
            child = self.crossbreed(parents[0],parents[1])
            child.mutate(N,MUTATION)
            next_gen.append(child)
        self.weights.clear()
        for DNA in next_gen:
            DNA.fitness()
            self.weights.append(1/DNA.tour_length)
        next_gen.sort(key=lambda x: x.tour_length)
        self.mating_pool = next_gen
        return

    # Extract quality and route from optimal DNA
    def output(self,DNA):
        route = []
        for gene in DNA.strand:
            route.append(gene.node_id)
        return DNA.tour_length,route

    # Main driver program to run the whole algorithm for a fixed number of generation or until timeout
    def evolve(self):
        start_time = time.time()
        trace =[]
        for city in self.cities:
            self.gene_pool.append(self.gene(city[0],city[1],city[2]))
        self.populate()
        curr_min = sys.maxsize
        gen_time = 0
        gen_start = time.time()
        for i in range(self.hyp["GENERATIONS"]):
            self.survive()
            if self.mating_pool[0].tour_length < curr_min:
                elapsed = time.time() - start_time
                print("{:.2f},{}".format(elapsed,self.mating_pool[0].tour_length))
                trace.append([elapsed,self.mating_pool[0].tour_length])
                curr_min = self.mating_pool[0].tour_length
                best_DNA = self.mating_pool[0]
            if self.cutoff is not None:
                if (self.cutoff - elapsed) < (gen_time + 2):
                    break
            gen_time = time.time() - gen_start

        quality,route = self.output(best_DNA)
        return trace,quality,route
 
