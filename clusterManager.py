import importer, math, pandas
from Cluster import Cluster, new_cluster
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA as sklearnPCA

pandas.set_option('display.max_rows', 500)
data, players = importer.data_import()

clusterNumber = 3
maxIterations = 1
prevError = 1
deltaError = 0.001
iterationError = 0
clusterList = []

# for x in range(0,clusterNumber):
#     cluster = new_cluster(data.sample(1))
#     clusterList.append(cluster)
cluster = new_cluster(data.loc[[10]])
clusterList.append(cluster)
cluster = new_cluster(data.loc[[202]])
clusterList.append(cluster)
cluster = new_cluster(data.loc[[31]])
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
    x.print_members()

    mergedMembers.append(x.members)
    colorIndex += 1


result = pandas.concat(mergedMembers)
# print(result)

ids = result['idf']
idx = result.index
# print(ids)

pca = sklearnPCA(n_components=2)  # 2-dimensional PCA

data = pandas.DataFrame(pca.fit_transform(result))

data = data.reset_index(drop=True)
ids = ids.reset_index(drop=True)
# idx = ids.reset_index(drop=True)

data = data.join(ids)
data = data.set_index(idx)

# print(data)

fig,ax = plt.subplots()

fig.canvas.set_window_title('K-means')

for id, coords in data.iterrows():
    annot = ax.annotate(id ,xy=(coords[0],coords[1]), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

# ax.annotate('a', (data[0], data[1]))



#
def update_annot(ind):

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    # text = "{}{}".format("\n".join([str(players.loc[players['id_player'] == idx[n]]['p_name'].values[0]) for n in ind["ind"]]))
    text = ''

    for n in ind["ind"]:
        player = players.loc[players['id_player'] == idx[n]]
        text += player['p_name'].values[0] + ' - ' + str(player['id_player'].values[0]) + '\n'

    annot.set_text(text[:-1])
    annot.get_bbox_patch().set_facecolor('white')
    annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    vis = annot.get_visible()
    # print(event.inaxes)
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            # pos = sc.get_offsets()[ind["ind"][0]]
            # annot.xy = pos
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()


colorList = []
for colorInd in data['idf'].tolist():
    colorList.append(colors[colorInd])

sc = plt.scatter(x=data[0],y=data[1], color=colorList)

fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()