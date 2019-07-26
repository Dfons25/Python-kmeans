import math, pandas
from helpers import importer
import matplotlib.pyplot as plt
from helpers.Cluster import new_cluster
from helpers.kmeansFunctions import assignToClosestCluster, recalculateCentroids, calculateError
from sklearn.decomposition import PCA as sklearnPCA


pandas.set_option('display.max_rows', 500)
data, players = importer.data_import()

clusterNumber = 3
maxIterations = 1
prevError = 1
deltaError = 0.001
iterationError = 0
colors = ['red', 'blue', 'green', 'purple', 'pink', 'gray', 'olive']
colorIndex = 0
clusterList = []

for _ in range(clusterNumber):
    cluster = new_cluster(data.sample())
    clusterList.append(cluster)

# fixed initial centroids for easy debugging

# cluster = new_cluster(data.loc[[10]])
# clusterList.append(cluster)
# cluster = new_cluster(data.loc[[202]])
# clusterList.append(cluster)
# cluster = new_cluster(data.loc[[31]])
# clusterList.append(cluster)

assignToClosestCluster(data, clusterList)

countIterations = 0

while True:
    closestClusterList = assignToClosestCluster(data, clusterList)

    recalculatedCentroidsList = recalculateCentroids(closestClusterList)

    iterationError = calculateError(data, recalculatedCentroidsList)

    countIterations += 1

    if countIterations > maxIterations or math.fabs(prevError - iterationError) < deltaError:
        break


##### vv PLOT vv


mergedMembers = []

for x in recalculatedCentroidsList:

    x.members['idf'] = colorIndex
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

data = data.join(ids)
data = data.set_index(idx)

fig,ax = plt.subplots()

fig.canvas.set_window_title('K-means')

for id, coords in data.iterrows():
    annot = ax.annotate(id ,xy=(coords[0],coords[1]), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)


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