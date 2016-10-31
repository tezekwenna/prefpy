import io
import math
import itertools
from prefpy.profile import Profile
from prefpy.preference import Preference
from prefpy.mechanism import Mechanism

class RankedPairs(Mechanism):
    def __init__(self):
        pass
    #DFS
    def isCycle(self,graph,candList):

        stack=[]
        visited=[]
        #there is a edge btween each node
        #so stack has n-1 elements to begin with
        currentNode=candList[0]
        stack=list(graph[currentNode].keys())

        while len(stack)!=0:
            currentNode=stack.pop(0)
            visited.append(currentNode)
            #print((graph))
            #print(currentNode)
            for neighbor in list(graph[currentNode].keys()):
                if neighbor in visited:
                    return False
            stack.extend(list(graph[currentNode].keys()))

        return True

    def getNewGraph(self,prof):
        newGraph={}
        wmg=prof.getWmg()
        #print(wmg)
        edges=[]
        for cand in prof.candMap.keys():
            newGraph[cand] = {}
        #initialize new graph to all zero edges
        for cand1 in prof.candMap.keys():
            for cand2 in prof.candMap.keys():
                if cand1 is not cand2:
                    #print("cand1 %d cand2 %d \n"%(cand1,cand2))
                    newGraph[cand1][cand2] = 0
                    if wmg[cand1][cand2]>=0 :

                        edges.append((wmg[cand1][cand2],cand1,cand2))
        #print('initialized new graph\n')
        #print(newGraph)
        sorted(edges, key=lambda weight: weight[0])
        ##print(edges)
        for i in range(len(edges)):
            if edges[i][0]<0:
                break
            #print(edges[i][0])
            newGraph[edges[i][1]][edges[i][2]]=edges[i][0]
            if self.isCycle(newGraph,list(prof.candMap.keys())):
                #every edge is initialized ot 0
                # may have to delet edge instead
                newGraph[edges[i][1]][edges[i][2]]=0
                break

        return newGraph
    def getOneWinner(self,prof):
        newGraph=self.getNewGraph(prof)
        #print(newGraph)
        candMap=prof.candMap
        numCanidates=len(candMap.keys())
        tempCount=0
        winnerList=[]
        for cand1 in candMap.keys():
            tempCount=0
            for cand2 in candMap.keys():

                if cand1 is not cand2 and newGraph[cand1][cand2]>0:
                    tempCount+=1
            if tempCount==numCanidates-1:
                winnerList.append((cand1,candMap[cand1]))

        return winnerList



    def getWinners(self, prof):
        pass


    def getRanking(self, prof):
        pass





