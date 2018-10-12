import pandas

class Cluster(object):
    meanTwoPoints = 0
    meanThreePoints = 0
    meanAssists = 0
    meanFouls = 0
    meanBlocks = 0
    fieldnames = ["twoPoints", "threePoints", "assists", "fouls", "blocks"]
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

    def get_centroid_info(self):
        info = self.members
        values = [self.meanTwoPoints, self.meanThreePoints, self.meanAssists, self.meanFouls, 2]
        position = len(info.index) + 1
        info.loc[position] = values
        # info['twoPoints'] = self.meanTwoPoints
        # info['threePoints'] = self.meanThreePoints
        # info['assists'] = self.meanAssists
        # info['fouls'] = self.meanFouls
        # info['blocks'] = self.meanBlocks
        return info.loc[position]


def new_cluster(obj):
    cluster = Cluster(obj['twoPoints'], obj['threePoints'], obj['assists'], obj['fouls'], obj['blocks'])
    return cluster

