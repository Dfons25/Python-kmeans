import importer, math
from Cluster import Cluster, new_cluster

data = importer.data_import()

clusterNumber = 3
maxIterations = 10
prevError = 0
deltaError = 0.001
iterationError = 0
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

def recalculateCentroids(clusterList):
    for cluster in clusterList:
        cluster.editCluster(cluster.get_average())

    return clusterList

def calculateError(clusterList):
    sumDistance = 0.0

    for cluster in clusterList:
        for index, member in data.iterrows():
            sumDistance += calculateDistance(cluster, member) ** 2

    return sumDistance

countIterations = 0

newClusterList = []

while True:
    newClusterList = assignToClosestCluster(data, clusterList)
    newClusterList = recalculateCentroids(newClusterList)
    iterationError = calculateError(newClusterList)
    if countIterations < maxIterations and math.fabs(prevError - iterationError) > deltaError:
        break


for x in newClusterList:
    x.print_members()