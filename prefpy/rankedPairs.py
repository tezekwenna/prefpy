'''
Authors: Bilal Salam, Levin Huang, Lucky Cho
'''


import io
import math
import itertools
from prefpy.profile import Profile
from prefpy.preference import Preference
from prefpy.mechanism import Mechanism
import networkx as nx
import matplotlib.pyplot as plt
import copy

class branchedGraph():
	def __init__(self, rL, DG):
		self.remainingList = rL
		self.DG = DG
		
	def getNextEdge(self):
		branchedGraphList = []
		branchedEdges, branchedRemEdges = self.findTies()

		for i in range(len(branchedEdges)):
			tmpGraph = self.DG.copy()
			tmpEdge = branchedEdges[i]
			tmpGraph.add_edge(tmpEdge[1], tmpEdge[2], weight=tmpEdge[0])
			try: 
				nx.find_cycle(tmpGraph)
			except:
				tmpBranchedGraph = branchedGraph(branchedRemEdges[i], tmpGraph)
				branchedGraphList.insert(0, tmpBranchedGraph)
		return branchedGraphList
			
		
	def findTies(self):
		branchedRemEdges = [] #list of lists
		edges = self.remainingList
		tmpList = []
		tmpRemEdges = []
		if len(edges) > 0:
			tmpWeight = edges[0][0]
			
			for i in range(len(edges)):
				if edges[i][0] == tmpWeight:
					tmpRemEdges = copy.copy(edges)
					del tmpRemEdges[i]
					branchedRemEdges.append(tmpRemEdges)
					tmpList.append(edges[i])
		
		return tmpList, branchedRemEdges
	

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
		edges = sorted(edges, key=lambda weight: weight[0], reverse = True)

		return edges
		
	def drawGraph(self, DG):
		#nx.draw(DG)
		plt.figure()
		nodeLayout=nx.spring_layout(DG)
		nx.draw_networkx(DG,pos=nodeLayout,arrows=True)
		labels = nx.get_edge_attributes(DG, 'weight')
		nx.draw_networkx_edge_labels(DG, pos=nodeLayout, edge_labels=labels)
		#plt.show()
		
		
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
		
	def getTopRank(self, graphList):
		winners = []
		for bGraph in graphList:
			newGraph = bGraph.DG
			for i in newGraph.nodes():
				inedges = newGraph.in_edges(i)
				if inedges == []:
					winners.append(i)
		return winners
		

	def getWinners(self, prof=None,edges=None):
		if edges is None:
			edges = self.getSortedEdges(prof)
		else:
			edges = sorted(edges, key=lambda weight: weight[0], reverse = True)
		print(edges)
		DG = nx.DiGraph()
		newBranchedGraph = branchedGraph(edges, DG)
		graphs = newBranchedGraph.getNextEdge()
		winners = []
		doneList = []
		while(len(graphs) != 0):
		#Iterating through graph, appending to tmp graphs list such that we arent modifying the list we are iterating over
			tmpGraphs = []
			for graph in graphs: 
				tmpNextEdgeList = graph.getNextEdge()
				if tmpNextEdgeList == []:
					doneList.append(graph) 
				else:
					tmpGraphs = tmpGraphs + tmpNextEdgeList
			graphs = copy.copy(tmpGraphs)
				
		winners = self.getTopRank(doneList)
		print(len(doneList))
		for winner in doneList:
			self.drawGraph(winner.DG)
		plt.show()
		
		return set(winners)


	def getRanking(self, prof):
		pass





