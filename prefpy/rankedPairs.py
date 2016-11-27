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
	#returns a list of tuples(weight,label,label)
	def createNXGraph(self,edgeList):
		DG = nx.DiGraph()
		for edge in edgeList:
			DG.add_edge(edge[1], edge[2], weight=edge[0])

		#nx.draw(DG)
		nodeLayout=nx.spring_layout(DG)
		nx.draw_networkx(DG,pos=nodeLayout,arrows=True)
		labels = nx.get_edge_attributes(DG, 'weight')
		nx.draw_networkx_edge_labels(DG, pos=nodeLayout, edge_labels=labels)
		plt.show()

	#returns edges from the wmg sorted by weights
	def getSortedEdges(self,prof):
		# newGraph={}
		wmg = prof.getWmg()
		# print(wmg)
		# create empty networkx graph

		edges = []
		# initialize new graph to all zero edges
		for cand1 in prof.candMap.keys():
			for cand2 in prof.candMap.keys():
				if cand1 is not cand2:
					if wmg[cand1][cand2] >= 0:
						edges.append((wmg[cand1][cand2], prof.candMap[cand1], prof.candMap[cand2]))
		sorted(edges, key=lambda weight: weight[0])

		return edges
	def getNewGraph(self,prof):

		wmg=prof.getWmg()

		DG=nx.DiGraph()
		newGraph=nx.DiGraph()
		edges=[]
		#initialize new graph to all zero edges
		edges=self.getSortedEdges(prof)
		for edge in edges:
			if edge[0]<0:
				break
			DG.add_edge(edge[1], edge[2], weight=edge[0])
			try:
				#if there is no cycle the method throws an exception

				nx.find_cycle(DG)
				DG.remove_edge(edge[1], edge[2])
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

	def getWinnerWithTieBreakingMech(self,prof,prefList):
		pass

	def getWinners(self, prof):
		pass


	def getRanking(self, prof):
		pass





