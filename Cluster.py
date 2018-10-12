import pandas

class Cluster(object):
    meanTwoPoints = 0
    meanThreePoints = 0
    meanAssists = 0
    meanFouls = 0
    meanBlocks = 0
    fieldnames = ["id_game", "twoPoints", "threePoints", "assists", "fouls", "blocks", "count"]
    members = pandas.DataFrame(columns=fieldnames)

    def __init__(self, meanTwoPoints, meanThreePoints, meanAssists, meanFouls, meanBlocks):
        self.meanTwoPoints = meanTwoPoints
        self.meanThreePoints = meanThreePoints
        self.meanAssists = meanAssists
        self.meanFouls = meanFouls
        self.meanBlocks = meanBlocks
        members = pandas.DataFrame(columns=self.fieldnames)

    def add_members(self, obj):
        self.members = self.members.append(obj)

    def reset_members(self):
        self.members.iloc[0:0]

    def editCluster(self, obj):
        self.meanTwoPoints = obj['twoPoints']
        self.meanThreePoints = obj['threePoints']
        self.meanAssists = obj['assists']
        self.meanFouls = obj['fouls']
        self.meanBlocks = obj['blocks']

    def print_cluster(self):
        print("{0:.2f} \t {0:.2f} \t {0:.2f} \t {0:.2f} \t {0:.2f}".format(self.meanTwoPoints.values[0], self.meanThreePoints.values[0], self.meanAssists.values[0],
              self.meanFouls.values[0], self.meanBlocks.values[0]))

    def print_members(self):
        print(self.members)

    def get_average(self):
        return self.members.mean()


def new_cluster(obj):
    cluster = Cluster(obj['twoPoints'], obj['threePoints'], obj['assists'], obj['fouls'], obj['blocks'])
    return cluster

