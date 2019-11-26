import numpy as np
import time

class BranchAndBound:
    def __init__(self,cities,cutoff):
        self.cutoff=cutoff
        self.cities=cities
        self.points=[]
        self.distances=[]
        self.distances_minimum=[]
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
            self.points.append([cities[i][1],cities[i][2]])

    def euclidian(self,point1,point2):
        return np.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)

    def calculateDistances(self,points):
        for i in range(len(points)):
            dictionary={}
            temp=[]
            for j in range(len(points)):
                result=999999999.0
                if i!=j:
                    result=round(self.euclidian(points[i],points[j]))
                dictionary[result]=j
                temp.append(result)
            self.distances.append(temp)
            liste=temp.copy()
            liste.sort()
            temp2=[]
            for j in range(len(liste)):
                temp2.append(dictionary[liste[j]])
            self.distances_rank.append(temp2)
            self.distances_minimum.append(min(temp))

    def distancesRanking(self,distances):
        self.edges={}
        self.edges_values=[]
        for i in range(len(self.points)):
            for j in range(len(self.points)):
                if j>i:
                    self.edges[distances[i][j]]=[i,j]
                    self.edges_values.append(distances[i][j])
    
    def branch_bound(self,path):
        pathcopy=path[1:-1].copy()
        pathcopy.sort()
        string = [str(i) for i in pathcopy] 
        if "".join(string) in self.memory.keys():
            return self.memory["".join(string)]
        
        edge_list=self.edges_values.copy()
        trees={}
        somme=0
        for i in range(len(self.points)):
            if i not in path[1:-1]:
                trees[i]=i
        while len(edge_list)!=0:
            currentEdge=edge_list.pop(0)
            if self.edges[currentEdge][0] not in path[1:-1] and self.edges[currentEdge][1] not in path[1:-1]:
                if trees[self.edges[currentEdge][0]]!=trees[self.edges[currentEdge][1]]:
                    temp1=trees[self.edges[currentEdge][1]]
                    for k in trees.keys():
                        if trees[k]==temp1:
                            trees[k]=trees[self.edges[currentEdge][0]]
                    somme=somme+currentEdge
        self.memory["".join(string)]=somme
        return somme
        
    def research(self,path,somme):
        if (time.time()-self.timestamp)> self.cutoff:
            return
        if len(path)==len(self.points):
            length=somme+self.distances[path[-1]][path[0]]
            if length<self.minimum:
                self.minimum=int(length)
                self.bestSolution=path.copy()
                self.trace.append([round(time.time()-self.timestamp,2),int(length)])
        for i in range(len(self.points)):
            entier=self.distances_rank[path[-1]][i]
            if entier not in path:
                new_somme=somme+self.distances[path[-1]][entier]
                path.append(entier)
                
                bound=self.branch_bound(path)+new_somme

                if bound<self.minimum:
                    self.research(path,new_somme)
                path.pop()

    def main(self):
        self.readFile(self.cities)
        self.calculateDistances(self.points)
        self.distancesRanking(self.distances)
        self.edges_values.sort()

        self.timestamp=time.time()
    
        self.research([0],0)
