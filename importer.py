import csv
import json
import pandas

def data_import():

    fieldnames = ["id_player","id_game","twoPoints","threePoints","assists","fouls","blocks"]
    data = pandas.read_csv('resources/games.csv', sep = ';', header = None, names=fieldnames)

    compressedData = data.groupby('id_player').mean()
    compressedData = (compressedData-compressedData.min())/(compressedData.max()-compressedData.min())
    compressedData['id_game'] = data['id_game']
    compressedData['count'] = data.groupby(['id_player']).count()['id_game']

    return compressedData





