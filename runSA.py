import os, sys, glob
import pandas as pd
import numpy as np
import SA

"""
It is for the simulated annealing algorithm. 
$ python runSA.py
or run directly from IDE, no argument parse needed. 
Functional steps in this file:
1. Read files from DATA/
2. process it to numpy array
3. pass numpy array to SA.py, return the shortest distance
4. write the city name(from DATA/file name) and the shortest distance in the result/SA.csv file
5. This is one time run, it may need multiple runs to generate average results. 
"""

def findHeader(filename):
    with open(filename, "r") as f:
        n = 0
        for line in f:
            n += 1
            line = line.strip()
            if line == "NODE_COORD_SECTION":
                break
    return n


def read_file(filename):
    headlines = findHeader(filename)
    df = pd.read_csv(filename, skiprows=headlines,  sep=" ", header=None, names=['pos', 'x', 'y'])
    df.drop(df.tail(1).index, inplace=True)
    np_df = df.values
    return np_df


def apply_annealing(df):
    # Call SA algorithm
    s = SA.SimulatedAnnealing(df)
    s.anneal()
    return s.best_distance


def main():
    print("Simulated Annealing Algorithm: \n")
    # if result file existed, remove the file
    if os.path.exists('results/SA.csv'):
        os.remove('results/SA.csv')

    for file in glob.glob('DATA/*.tsp'):
        city = os.path.basename(file).split('.')[0]
        df = read_file(file)
        result = apply_annealing(df)
        result = int(round(result))
        print('{} is processed!'.format(file))
        print('The shortest distance for {} is {}. \n'.format(city, result))
        # write the result
        with open('results/SA.csv', "a+") as out:
            out.write("{}, {}\n".format(city, result))


if __name__ == "__main__":
    main()

