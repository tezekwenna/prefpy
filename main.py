import prefpy
from prefpy import preference
from prefpy import profile

from prefpy.rankedPairs import RankedPairs
from prefpy.profile import Profile

if __name__ == '__main__' :

    data=Profile({},[])

    data.importPreflibFile("input")

    rankpairMech=RankedPairs()
    print(rankpairMech.getOneWinner(data))
    #edgeList=rankpairMech.getSortedEdges(data)
    #rankpairMech.createNXGraph(edgeList)