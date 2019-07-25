import pandas, copy

def caps(x):
    return x[0].upper() + x[1:]

class Cluster(object):

    fieldnames = ["twoPoints", "threePoints", "assists", "fouls", "blocks"]

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, 'mean' + caps(key), float(value))
        self.members = pandas.DataFrame(columns=self.fieldnames)

    def add_members(self, obj):
        self.members = self.members.append(obj)

    def reset_members(self):
        self.members = self.members.iloc[0:0]

    def print_members(self):
        print(self.members)

    def update_average(self):
        for key, value in self.members.mean().items():
            self.__dict__['mean' + caps(key)] = value


def new_cluster(clusterInfo):
    cluster = Cluster(**clusterInfo)
    return cluster

