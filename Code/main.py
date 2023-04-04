import numpy as np


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
        matrix = np.zeros((len(lines), len(lines[0])-1))
        for i in range(len(lines)):
            line = lines[i]
            for j in range(len(line)):
                if line[j] != '\n':
                    if line[j] == "R":
                        matrix[i][j] = 1
                    elif line[j] == "C":
                        matrix[i][j] = 2
    return matrix


cost_map = read_file("Données/Cost_map.txt")
production_map = read_file("Données/Production_map.txt")
usage_map = read_usage_file("Données/Usage_map.txt")

print(cost_map)
print(production_map)
print(usage_map)
