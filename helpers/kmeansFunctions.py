import math

def caps(x):
    return x[0].upper() + x[1:]

def calculateDistance(cluster, elem):
    return math.sqrt(sum([(cluster.__dict__['mean' + caps(key)] - value) ** 2 for key, value in elem.items()]))

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
        cluster.update_average()

    return clusterList

def calculateError(data, clusterList):
    sumDistance = 0.0

    for cluster in clusterList:
        for index, member in data.iterrows():
            sumDistance += calculateDistance(cluster, member) ** 2

    return sumDistance