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

def getTopRank(netxGraph):
		topRanks = []
		for i in netxGraph.nodes():
			if netxGraph.in_edges(i) == []:
				topRanks.append(i)
		return topRanks

class branchedGraph():
	def __init__(self, rL, DG):
		self.remainingList = rL
		self.DG = DG
	def isDone(self):
		if len(self.remainingList) ==0:
			return True
		else:
			return False
	def getNextEdge(self, currentWinners):
		branchedGraphList = []
		branchedEdges, branchedRemEdges = self.findTies()

		for i in range(len(branchedEdges)):
			tmpGraph = self.DG.copy()
			tmpEdge = branchedEdges[i]
			
			self.addOneWayEdge(tmpGraph, tmpEdge)

			if not set(getTopRank(tmpGraph)).issubset(set(currentWinners)):
				tmpBranchedGraph = branchedGraph(branchedRemEdges[i], tmpGraph)
				branchedGraphList.append( tmpBranchedGraph)
		return branchedGraphList
		
	def addOneWayEdge(self, graph, edge):
		if not graph.has_edge(edge[2], edge[1]):
			graph.add_edge(edge[1], edge[2], weight=edge[0])
			try:
				nx.find_cycle(graph)
				graph.remove_edge(edge[1], edge[2])
			except:
				pass
			

	def findTies(self):
		branchedRemEdges = [] #list of lists
		edges = self.remainingList
		tmpList = [] #holds list of edges to branch out to
		tmpRemEdges = []
		if len(edges) > 0:
			tmpWeight = edges[0][0]
			for i in range(len(edges)):
				if edges[i][0] == tmpWeight: #we find tied edge that we want to use
					tmpRemEdges = copy.copy(edges) #deep copy edge list
					del tmpRemEdges[i] #remove tied edge from the remaining list
					branchedRemEdges.append(tmpRemEdges)
					tmpList.append(copy.copy(edges[i])) #add the edge we are using to the list of edges to extend G`
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
					#if wmg[cand1][cand2] >= 0:

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
		topRanks = []
		for bGraph in graphList:
			newGraph = bGraph.DG
			for i in newGraph.nodes():
				inedges = newGraph.in_edges(i)
				if inedges == []:
					topRanks.append(i)
		return topRanks
		
	def initDG(self, edges):
		nodeSet=set()
		DG = nx.DiGraph()
		for i in range(len(edges)):
			nodeSet.add(edges[i][1])

		DG.add_nodes_from(nodeSet)
		return DG

	def getWinners(self, prof=None,edges=None):
		if edges is None:
			edges = self.getSortedEdges(prof)
		else:
			edges = sorted(edges, key=lambda weight: weight[0], reverse = True)
		print(edges)
		#DG = nx.DiGraph()
		DG=self.initDG(edges)

		winners = []
		doneList = []
		newBranchedGraph = branchedGraph(edges, DG)
		graphs = newBranchedGraph.getNextEdge(winners)
		while(len(graphs) != 0):
		#Iterating through graph, appending to tmp graphs list such that we arent modifying the list we are iterating over
			tmpGraphs = []
			graph=graphs.pop(0)

			tmpNextEdgeList = graph.getNextEdge(winners)
			if tmpNextEdgeList == [] and graph.isDone():
				doneList.append(graph)
				winners += self.getTopRank(doneList)

			else:

				graphs=tmpNextEdgeList+graphs

				
		#winners = self.getTopRank(doneList)
		print(len(doneList))
		for winner in doneList:
			self.drawGraph(winner.DG)
		plt.show()
		
		return set(winners)


	def getRanking(self, prof):
		pass





