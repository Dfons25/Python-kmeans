import csv
import json
import pandas

def data_import():

    fieldnames_games = ["id_player","id_game","twoPoints","threePoints","assists","fouls","blocks"]
    fieldnames_players = ["id_player","p_name","team","date","sex"]

    data_g = pandas.read_csv('resources/games.csv', sep = ';', header = None, names=fieldnames_games)

    data_p = pandas.read_csv('resources/players.csv', sep = ';', header = None, names=fieldnames_players)

    compressedGames = data_g.groupby('id_player').mean()
    compressedGames = (compressedGames-compressedGames.min())/(compressedGames.max()-compressedGames.min())
    compressedGames['id_game'] = data_g['id_game']

    del compressedGames['id_game']
    return compressedGames, data_p





