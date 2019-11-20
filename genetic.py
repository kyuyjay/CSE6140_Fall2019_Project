import sys
import time
import random
import numpy as np

def genetic(params,cities,cutoff):

    start_time = time.time()
    N = params["DIMENSION"]
    POPULATION = 1000
    ELITISM = round(0.1 * POPULATION)
    MUTATION = 0.05
    GENERATIONS = 10000
    gene_pool = []
    mating_pool = []
    weights = []
    trace = []
    print("Hyperparameters\nN: {}\nPopulation: {}\nElitism: {}\nMutation: {}".format(N,POPULATION,ELITISM,MUTATION))
    class gene:
        def __init__(self,node_id=-1,x=0,y=0):
            self.node_id = node_id
            self.x = x
            self.y = y
            gene_pool.append(self)

        def distance(self,dest):
            return np.linalg.norm([dest.x - self.x,dest.y - self.y])

    class DNA:
        def __init__(self):
            self.strand = random.sample(gene_pool,N)
            self.tour_length = 0

        def fitness(self):
            self.tour_length = 0
            for i in range(len(self.strand) - 1):
                self.tour_length = self.tour_length + self.strand[i].distance(self.strand[i+1])
            self.tour_length = int(round(self.tour_length + self.strand[-1].distance(self.strand[0])))
            return

        def crossbreed(self,partner):
            start = random.randrange(0, round((N/2) - 1))
            child = DNA()
            child.strand = self.strand[start:start + round(N/2)]
            node_id = list(map(lambda x: x.node_id,child.strand))
            for gene in partner.strand:
                if gene.node_id not in node_id:
                    child.strand.append(gene)
            return child

        def mutate(self):
            for i in range(len(self.strand)):
                chance = random.random()
                if chance <= MUTATION:
                    swap = random.randrange(0,N)
                    self.strand[i],self.strand[swap] = self.strand[swap],self.strand[i]

    def populate():
        for i in range(POPULATION):
            mating_pool.append(DNA())
            mating_pool[i].fitness()
            weights.append(1/mating_pool[i].tour_length)
        mating_pool.sort(key=lambda x: x.tour_length)

    def select(weights):
        parents = random.choices(mating_pool,weights=weights,k=2)
        return parents
        
    def survive(mating_pool):
        next_gen = mating_pool[0:ELITISM]
        for i in range(POPULATION - ELITISM):
            parents = select(weights)
            child = parents[0].crossbreed(parents[1])
            child.mutate()
            next_gen.append(child)
        weights.clear()
        for DNA in next_gen:
            DNA.fitness()
            weights.append(1/DNA.tour_length)
        return next_gen

    def output(DNA):
        route = []
        for gene in DNA.strand:
            route.append(gene.node_id)
        return DNA.tour_length,route

    for city in cities:
        gene(city.node_id,city.x,city.y)
    populate()
    curr_min = sys.maxsize
    gen_time = 0
    gen_start = time.time()
    for i in range(GENERATIONS):
        mating_pool = survive(mating_pool)
        mating_pool.sort(key=lambda x: x.tour_length)
        if mating_pool[0].tour_length < curr_min:
            elapsed = time.time() - start_time
            print("{:.2f},{}".format(elapsed,mating_pool[0].tour_length))
            trace.append([elapsed,mating_pool[0].tour_length])
            curr_min = mating_pool[0].tour_length
            best_DNA = mating_pool[0]
        if cutoff is not None:
            if (cutoff - elapsed) < (gen_time + 5):
                break

    gen_time = time.time() - gen_start
    quality,route = output(best_DNA)
    return trace,quality,route
 
