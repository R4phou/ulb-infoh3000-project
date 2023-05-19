import numpy as np
import random as r
import time as t


def read_file(path):
    """Fonction qui lit le fichier et renvoie une matrice (numpy) des nombres du fichier"""
    with open(path, "r") as file:
        lines = file.readlines()
        matrix = np.zeros((len(lines), len(lines[0])-1))
        for i in range(len(lines)):
            line = lines[i]
            for j in range(len(line)):
                if line[j] != '\n':
                    matrix[i][j] = int(line[j])
    return matrix


def read_usage_file(path):
    """Fonction qui lit le fichier Usage_map
    Renvoie une matrice de nombres (numpy)
    Lorsqu'il n'y a rien, c'est remplacé par le nombre 0
    Les routes R sont remplacées par le nombre 1
    Les constructions C sont remplacées par le nombre 2
    """
    with open(path, "r") as file:
        lines = file.readlines()
        matrix = np.zeros((len(lines), len(lines[0])-1))  # -1 car \n
        for i in range(len(lines)):
            line = lines[i]
            for j in range(len(line)):
                if line[j] != '\n':
                    if line[j] == "R":
                        matrix[i][j] = 1
                    elif line[j] == "C":
                        matrix[i][j] = 2
    return matrix


def position_of_item(item, matrice):
    """Fonction retournant la liste de toutes les positions des buildings dans la usage map"""
    indices = np.where(matrice == item)
    return list(zip(indices[1], indices[0]))


def distance_between_tuple(tup1, tup2):
    """Fonction qui calcule la distance entre deux tuples"""
    return np.sqrt((tup1[0]-tup2[0])**2 + (tup1[1]-tup2[1])**2)


def calculate_proximity_map(usage_map, buildings):
    """Fonction qui calcule la matrice de proximité"""
    mat = np.zeros((len(usage_map), len(usage_map[0])))
    for i in range(len(usage_map)):
        for j in range(len(usage_map[0])):
            if usage_map[i][j] == 2:
                mat[i][j] = 0  # si c'est un batiment, la distance est 0
            else:
                mat[i][j] = 100000
                for building in buildings:
                    dist = distance_between_tuple((j, i), building)
                    if dist < mat[i][j]:
                        mat[i][j] = dist
    return mat


def normalize(x, max):
    """Fonction qui normalise une liste de nombres"""
    return [i/max for i in x]


def to_tuple_liste(liste1, liste2):
    """Fonction qui transforme deux listes en une liste de tuples"""
    final = []
    for i in range(len(liste1)):
        final.append((liste1[i], liste2[i]))
    return final


def normalise(scores, maxs):
    """
    scores est une liste de liste de scores
    maxs est une liste de max de chaque critère
    """
    return [[scores[i][j]/maxs[j] for j in range(len(scores[0]))]
            for i in range(len(scores))]

def flatten(list_to_merge):
    """Fonction qui réduit une liste de liste en une liste (réduction de 1 niveau de profondeur seulement)"""
    return [element for liste in list_to_merge for element in liste]

if __name__ == "__main__":
    import init as i
