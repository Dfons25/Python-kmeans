import importer, math, pandas
from Cluster import Cluster, new_cluster

data = importer.data_import()
# print(data)
# print(data.sample(1))

clusterNumber = 3
clusterList = []

ds_ = data.sample(1)
print(ds_)

# fieldnames = ["id_player", "id_game", "twoPoints", "threePoints", "assists", "fouls","blocks", "count"]
# data = pandas.read_csv('resources/games.csv', sep=';', header=None, names=fieldnames)
df_ = data

df_.iloc[0:0]
df_ = df_.append(ds_)
print(df_)
