from useful import *

PROD_MAX = 10000
PROX_MAX = 10000
COMP_MAX = 10000

COST_MAP = read_file("Data/Cost_map.txt")
PRODUCTION_MAP = read_file("Data/Production_map.txt")
USAGE_MAP = read_usage_file("Data/Usage_map.txt")

SIZE_X = len(COST_MAP)
SIZE_Y = len(COST_MAP[0])

WEIGHTS = [0.2, 0.4, 0, 4]

"""Générer une solution"""
solution = np.zeros((SIZE_X, SIZE_Y))  # matrice avec des 1 et des 0 ()


def generate_solution():
    """Génère une solution random"""


"""Calcul du score"""


def productivity(solution):
    """Calcule le score de productivité totale d'une solution
    Solution = matrice de 0 et de 1 (1 = acheté et 0 = Pas acheté)
    """
    return np.sum(np.multiply(solution, PRODUCTION_MAP))


def proximity(solution):
    """Calcule le score de proximité totale d'une solution"""
    return


def compacity(solution):
    """Calcule le score de compacité totale d'une solution"""
    return


def calcul_global_score(solution, weights):
    """Renvoie la somme pondérée des scores partiels"""
    prod = productivity(solution)
    comp = compacity(solution)
    prox = proximity(solution)
    return weights[0]*prod/PROD_MAX + weights[1]*prox/PROX_MAX + weights[2]*comp/COMP_MAX


"""Trouver l'algo à implémenter"""
