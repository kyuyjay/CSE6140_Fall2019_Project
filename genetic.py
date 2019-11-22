import sys
import time
import random
import numpy as np

class genetic:
    def __init__(self,params,cities,cutoff):
        self.hyp = {
                "N": params["DIMENSION"],
                "POPULATION": 1000,
                "ELITIST FACTOR": 0.1,
                "MUTATION": 0.05,
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

    class gene:
        def __init__(self,node_id=-1,x=0,y=0):
            self.node_id = node_id
            self.x = x
            self.y = y

        def distance(self,dest):
            return np.linalg.norm([dest.x - self.x,dest.y - self.y])

    class DNA:
        def __init__(self,N,gene_pool):
            self.strand = random.sample(gene_pool,N)
            self.tour_length = 0
            self.N = N

        def fitness(self):
            self.tour_length = 0
            for i in range(len(self.strand) - 1):
                self.tour_length = self.tour_length + self.strand[i].distance(self.strand[i+1])
            self.tour_length = int(round(self.tour_length + self.strand[-1].distance(self.strand[0])))
            return

        def mutate(self,N,MUTATION):
            for i in range(len(self.strand)):
                chance = random.random()
                if chance <= MUTATION:
                    swap = random.randrange(0,N)
                    self.strand[i],self.strand[swap] = self.strand[swap],self.strand[i]
            return

    def populate(self):
        for i in range(self.hyp["POPULATION"]):
            self.mating_pool.append(self.DNA(self.hyp["N"],self.gene_pool))
            self.mating_pool[i].fitness()
            self.weights.append(1/self.mating_pool[i].tour_length)
        self.mating_pool.sort(key=lambda x: x.tour_length)
        return

    def select(self):
        parents = random.choices(self.mating_pool,weights=self.weights,k=2)
        return parents
 
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

    def output(self,DNA):
        route = []
        for gene in DNA.strand:
            route.append(gene.node_id)
        return DNA.tour_length,route

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
                if (self.cutoff - elapsed) < (gen_time + 5):
                    break
            gen_time = time.time() - gen_start

        quality,route = self.output(best_DNA)
        return trace,quality,route
 
