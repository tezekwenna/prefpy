import io
import math
import itertools
from prefpy.profile import Profile
from prefpy.preference import Preference
from prefpy.mechanism import Mechanism
import networkx as nx
import matplotlib.pyplot as plt

class RankedPairs(Mechanism):
	def __init__(self):
		pass
	
	def getNewGraph(self,prof):
		#newGraph={}
		wmg=prof.getWmg()
		#print(wmg)
		#create empty networkx graph
		DG=nx.DiGraph()
		newGraph=nx.DiGraph()
		edges=[]
        #initialize new graph to all zero edges
		for cand1 in prof.candMap.keys():
			for cand2 in prof.candMap.keys():
				if cand1 is not cand2:
					if wmg[cand1][cand2]>=0 :
						edges.append((wmg[cand1][cand2],cand1,cand2))
		sorted(edges, key=lambda weight: weight[0])
		for i in range(len(edges)):
			if edges[i][0]<0:
				break
			DG.add_edge(prof.candMap.get(edges[i][1]), prof.candMap.get(edges[i][2]), weight=edges[i][0])
			try:
				nx.find_cycle(DG)
				DG.remove_edge(prof.candMap.get(edges[i][1]), prof.candMap.get(edges[i][2]))
				break
				# every edge is initialized to 0
				# may have to delete edge instead
			except:
				pass
		return DG
		
	def getOneWinner(self,prof):
		newGraph=self.getNewGraph(prof)
		numCanidates=newGraph.number_of_nodes()
		winners = []
		for i in newGraph.nodes():
			inedges = newGraph.in_edges(i)
			if inedges == []:
				winners.append(i)
		return winners
		



	def getWinners(self, prof):
		pass


	def getRanking(self, prof):
		pass





