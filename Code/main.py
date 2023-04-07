from useful import *

COST_MAP = read_file("Data/Cost_map.txt")
PRODUCTION_MAP = read_file("Data/Production_map.txt")
USAGE_MAP = read_usage_file("Data/Usage_map.txt")

SIZE_X = len(COST_MAP)  # Taille (largeur) de la carte
SIZE_Y = len(COST_MAP[0])  # Taille (hauteur) de la carte

BUDGET = 50  # en dizaines de milliers d'euros
PROD_MAX = 10000  # Valeur max du score de productivité
PROX_MAX = 10000  # Valeur max du score de proximité
COMP_MAX = 10000  # Valeur max du score de compacité


# Poids de la somme pondérée[Proximité, Productivité, Compacité]
WEIGHTS = [0.2, 0.4, 0.4]

"""----------------------------------------------------------------------------------------------------
                                        Génération des solutions
----------------------------------------------------------------------------------------------------"""


def generate_solution():
    """Génère une solution qui répond aux différentes contraintes (une solution de départ)"""
    matrix = np.zeros((SIZE_X, SIZE_Y))
    return matrix


"""----------------------------------------------------------------------------------------------------
                                            Calcul du score
----------------------------------------------------------------------------------------------------"""


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


"""----------------------------------------------------------------------------------------------------
                                    Implémentation de l'algorithme
----------------------------------------------------------------------------------------------------"""
