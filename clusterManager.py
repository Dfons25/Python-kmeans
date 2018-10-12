import importer, math
from Cluster import Cluster, new_cluster

data = importer.data_import()

clusterNumber = 3
clusterList = []

for x in range(0,clusterNumber):
    cluster = new_cluster(data.sample(1))
    clusterList.append(cluster)

for clusters in clusterList:
    clusters.print_cluster()

def calculateDistance(cluster, elem):

    return math.sqrt((cluster.meanTwoPoints - elem['twoPoints']) ** 2 +
                      (cluster.meanThreePoints - elem['threePoints']) ** 2 +
                      (cluster.meanAssists - elem['assists']) ** 2 +
                      (cluster.meanBlocks - elem['blocks']) ** 2 +
                      (cluster.meanFouls - elem['fouls']) ** 2
                 )

def assignToClosestCluster(data, clusterList):

    for cluster in clusterList:
        cluster.reset_members()

    for index, member in data.iterrows():

        leastDistance = math.inf

        for cluster in clusterList:
            distance = calculateDistance(cluster,member)

            if distance < leastDistance:
                leastDistance = distance
                closestCluster = cluster

        closestCluster.add_members(member)

    return clusterList

newClusterList = assignToClosestCluster(data, clusterList)

for x in newClusterList:
    x.print_members()
