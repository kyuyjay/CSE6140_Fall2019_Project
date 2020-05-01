# CSE 6140 TSP Project (2019 Fall)

## Group members
Eric Gastineau
Jacob Beel
Yiwen Bu
Yong Jian Quek

## Description
Solve a Travelling Salesman Problem using multiple different algorithms. Individual algorithms are implemented in seperate modules that are then called by tsp_main.py.
All code tested on python 3.6.0


## Usage:
python3 tsp_main.py -inst <filename>
                    -alg [BnB | Approx | LS1 | LS2]
                    -time <cutoff_in_seconds>
                    [-seed <random_seed>]

## Dependencies
numpy    1.17.4
All other modules part of python 3.6.0 standard library

## Algorithm implemented
1. Branch-and-Bound
2. Heuristics
3. Local Search: Genetic Algorithm
4. Local Search: Simulated Annealing Algorithm

### Branch-and-Bound
    Implemented in BranchAndBound.py and linked to tsp_main.py.
    Create BranchAndBound object and call BranchAndBound method to run algorithm. 
    BranchAndBound.minimum returns the quality
    BranchAndBound.bestSolution returns the route
    BranchAndBound.trace returns the trace
### Heuristics
    Implemented in construction_heuristics.py and linked to tsp_main.py
    Call construction_heuristic.nearest_neighbor to run algorithm.
    Returns trace, quality, route.
### Genetic Algorithm
    Implemented in genetic.py and linked to tsp_main.py.
    Create genetic object and call evolve method to run algorithm.
    evolve returns trace, quality, route
#### Hyperparameters
    Population: 250
    Elitism Factor: 0.2
    Mutation Probability: 0.05
    Number of Generations: 10000
### Simulated Algorithm
    Implemented in SA.py and linked to tsp_main.py
    Create SimulatedAnnealing object and call anneal method to run algorithm.
    SimulatedAnnealing.best_distance returns the quality
    SimulatedAnnealing.best_route returns the route
    SimulatedAnnealing.trace returns the trace 
#### Hyperparameters
    Cooling Rate: 0.001
    



