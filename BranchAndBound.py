import numpy as np
import time
'''
This file is the implementation for Branch And Bound algorithm.
To run this code, you have to create an instance of this class with the data and the cutoff as the arguments.
The data has to be in the format Nx3 where the first column represents the index and the 2 last columns represent the coordinates.
At the end, you get self.minimum and self.bestSolution that represent the best solution found so far.
'''

class BranchAndBound:
    def __init__(self,cities,cutoff):
        self.cutoff=cutoff
        self.cities=cities
        self.points=[]
        self.distances=[]
        self.distances_rank=[]
        
        self.minimum=99999999
        self.bestSolution=[]

        self.edges={}
        self.edges_values=[]

        self.memory={}

        self.trace=[]
        self.timestamp=0

    def readFile(self,cities):
        for i in range(len(cities)):
            self.points.append([cities[i][1],cities[i][2]]) #self.points represents the input data

    def euclidian(self,point1,point2): #a simple euclidian distance
        return np.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)

    def calculateDistances(self,points): #we calculate every distance between 2 points
        for i in range(len(points)):
            dictionary={} #this dictionary will be used to rank the points according to their distances to a specific point
            temp=[]
            for j in range(len(points)):
                result=999999999.0 #if i==j, then we put a huge value so that we don't take this value into account anymore
                if i!=j:
                    result=round(self.euclidian(points[i],points[j]),2)
                dictionary[result]=j #we keep in memomy what was the index for this distance
                temp.append(result) #we keep in memory this distance
            self.distances.append(temp)
            liste=temp.copy()
            liste.sort() #we sort the distances according to their values
            temp2=[]
            for j in range(len(liste)):
                temp2.append(dictionary[liste[j]]) #then for a point i, we have the list of points according to their distances to the point i
            self.distances_rank.append(temp2)

    def distancesRanking(self,distances): #this will be used for the kruskal algorithm
        self.edges={} #for each distance there is one edge, we keep these relations in memory
        self.edges_values=[] #this list only have the values of the distances, it will be used to sort the distances
        for i in range(len(self.points)):
            for j in range(len(self.points)):
                if j>i:
                    self.edges[distances[i][j]]=[i,j] #each distance is mapped to an edge
                    self.edges_values.append(distances[i][j]) #hopefully there is no case where there are 2 distances that are the same
    
    def branch_bound(self,path): #the kruskal's algorithm to calculate the lower bound
        pathcopy=path[1:-1].copy()
        pathcopy.sort()
        string = [str(i) for i in pathcopy]
        
        if "".join(string) in self.memory.keys(): #if this MSP has already been calculated, we don't need to calculate it anymore
            return self.memory["".join(string)]
        
        edge_list=self.edges_values.copy()
        trees={} #we use a dictionary. Each point has a different key and each set is represented by a specific value. 
        total=0 #this will be the length of the spanning tree
        for i in range(len(self.points)):
            if i not in path[1:-1]:
                trees[i]=i #we begin in a state where each point is a separate tree
        while len(edge_list)!=0:
            currentEdge=edge_list.pop(0) #we take the edge with the lowest value
            if self.edges[currentEdge][0] not in path[1:-1] and self.edges[currentEdge][1] not in path[1:-1]:
                if trees[self.edges[currentEdge][0]]!=trees[self.edges[currentEdge][1]]: #if these points are in different trees then ...
                    temp1=trees[self.edges[currentEdge][1]]
                    for k in trees.keys():
                        if trees[k]==temp1:
                            trees[k]=trees[self.edges[currentEdge][0]] #the union of the trees
                    total=total+currentEdge
        self.memory["".join(string)]=total #now that we have calculated the result, we save it so that we don't need to calculate it anymore
        return total
        
    def research(self,path,somme): #the sum of the current path is given as an argument to save computation time
        if (time.time()-self.timestamp)> self.cutoff:
            return
        if len(path)==len(self.points):
            length=somme+self.distances[path[-1]][path[0]]
            if length<self.minimum: #if the current solution is better than the global solution, then it becomes the new global solution
                self.minimum=int(round(length))
                self.bestSolution=path.copy()
                self.trace.append([round(time.time()-self.timestamp,2),int(round(length))])
            return
        for i in range(len(self.points)):
            entier=self.distances_rank[path[-1]][i] #we try firstly the closest points
            if entier not in path:
                new_somme=somme+self.distances[path[-1]][entier] #the length of the current path
                path.append(entier)
                bound=self.branch_bound(path)+new_somme
                if bound<self.minimum:  #if the lower bound is inferior to the minimum, we expand the new problem
                    self.research(path,new_somme)  #we expand recursively
                path.pop() #we remove the last element that we added

    def main(self):
        self.readFile(self.cities) #we create the input
        self.calculateDistances(self.points) #we calculate all the distances between all pair of points
        self.distancesRanking(self.distances) #we sort all the edges for the kruskal algorithm
        self.edges_values.sort()
        self.timestamp=time.time() #we begin to count the time now

        self.research([0],0)
