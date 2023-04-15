import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from init import *


def print_usagemap_plus_sol(usage, sol):
    """
    USAGE_MAP: 0 libre/ 1 Route/ 2 Construction
    """
    mat = usage
    # [vide, route, constru, acheté, erreur]
    couleurs = ['white', 'lightblue', 'red',  'blue', 'green']
    cmap = ListedColormap(couleurs)
    for i in range(len(usage)):
        for j in range(len(usage[0])):
            if (sol[i][j] == 1 and usage[i][j] == 0):
                mat[i][j] = 3
            elif sol[i][j] == 1 and usage[i][j] != 0:
                mat[i][j] = 4
    fig, ax = plt.subplots()
    ax.matshow(mat, cmap=cmap)
    ax.set_title("USAGE MAP et Achat (vert)")
    plt.show()


def productivity(solution):
    """Calcule le score de productivité totale d'une solution
    Solution = matrice de 0 et de 1 (1 = acheté et 0 = Pas acheté)
    """
    return int(np.sum(np.multiply(solution, PRODUCTION_MAP)))


def proximity(solution):
    """Calcule le score de proximité totale d'une solution
    La proximité est la distance entre les bâtiments (2 dans USAGE_MAP) et le terrain acheté
    retourne la plus grande distance
    PROXIMITE A MAXIMISER car 1000/distance_tot
    """
    boughts = position_of_item(1, solution)
    distance = 100000
    distance_tot = 0
    for bought in boughts:
        for building in BUILDINGS:  # pour chaque terrain acheté, on regarde la distance minimale avec un batiment
            distance = min(distance, distance_between_tuple(bought, building))
        distance_tot += distance  # on ajoute la distance minimale pour un terrain
    return round(1000/distance_tot, 3)  # simplifier les calculs


def compacity(solution):
    """Calcule le score de compacité totale d'une solution"""
    boughts = position_of_item(1, solution)
    distance_tot = 0
    for bought in boughts:
        for i in range(len(boughts)):
            distance_tot += distance_between_tuple(bought, boughts[i])
    return round(1000/distance_tot, 3)


def check_bought(position, invest_map):
    """Vérifie que la position n'est pas déjà achetée"""
    return invest_map[position[1]][position[0]] == 0


def buy_position(pos, invest_map, budg):
    """Achat d'un terrain"""
    if check_in_map(pos) and check_bought(pos, invest_map):
        budg += COST_MAP[pos[1]][pos[0]]
        invest_map[pos[1]][pos[0]] = 1
    return invest_map, budg


def generate_compact_solution():
    """
    Génère une solution qui répond aux différentes contraintes (une solution de départ)
    Càd qu'on ne peut pas acheter de routes ou de batiments
    Et qu'on a un budget de 50
    """
    invested_map = np.zeros(
        (SIZE_Y, SIZE_X))  # Matrice de la taille de la carte
    to_buy = get_initial_pos()
    budget = i = 0
    while budget < BUDGET:
        if i == 4:
            break
        if budget + COST_MAP[to_buy[1]][to_buy[0]] <= BUDGET:
            invested_map, budget = buy_position(
                to_buy, invested_map, budget)  # Achat
        else:
            i += 1
        to_buy = select_next_pos(to_buy)  # selection de nouvelle position
    return invested_map, budget


def generate_random_solution():
    invested_map = np.zeros((SIZE_Y, SIZE_X))
    budget = 0
    while budget < BUDGET:
        to_buy = get_initial_pos()
        if check_in_map(to_buy):
            invested_map, budget = buy_position(to_buy, invested_map, budget)
    return invested_map, budget
