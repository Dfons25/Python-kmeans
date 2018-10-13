import importer, math, pandas
from Cluster import Cluster, new_cluster
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA as sklearnPCA


data = importer.data_import()

clusterNumber = 3
maxIterations = 30
prevError = 1
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
        # cluster.print_members()

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
    countIterations += 1
    print(countIterations)
    if countIterations > maxIterations or math.fabs(prevError - iterationError) < deltaError:
        break

colors = ['red', 'blue', 'green', 'purple', 'pink', 'gray', 'olive']
colorIndex = 0
mergedMembers = []

for x in newClusterList:

    x.members.loc[:, 'idf'] = colorIndex

    # extra = x.get_centroid_info()
    # x.members.loc[len(x.members.index) + 1] = extra

    mergedMembers.append(x.members)
    colorIndex += 1


result = pandas.concat(mergedMembers)
print(result)

ids = result['idf']
# print(ids)

pca = sklearnPCA(n_components=2)  # 2-dimensional PCA

data = pandas.DataFrame(pca.fit_transform(result))

data = data.reset_index(drop=True)
ids = ids.reset_index(drop=True)
data = data.join(ids)

for index, row in data.iterrows():
    print(row)
    if int(row[2]) == 55:
        plt.scatter(row[0],row[1], marker='s', color='orange')
    else:
        plt.scatter(row[0],row[1], color=colors[int(row[2])])
    #
    #

plt.show()