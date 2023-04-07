from useful import *

r.seed(22)

COST_MAP = read_file("Data/Cost_map.txt")
PRODUCTION_MAP = read_file("Data/Production_map.txt")
USAGE_MAP = read_usage_file("Data/Usage_map.txt")

SIZE_X = len(COST_MAP)  # Taille (largeur) de la carte
SIZE_Y = len(COST_MAP[0])  # Taille (hauteur) de la carte

BUDGET = 50  # en dizaines de milliers d'euros
PROD_MAX = 10000  # Valeur max du score de productivité
PROX_MAX = 10000  # Valeur max du score de proximité
COMP_MAX = 10000  # Valeur max du score de compacité


# Poids de la somme pondérée [Proximité, Productivité, Compacité]
WEIGHTS = [1, 1, 1]

"""----------------------------------------------------------------------------------------------------
                                        Génération des solutions
----------------------------------------------------------------------------------------------------"""


def generate_solution():
    """
    Génère une solution qui répond aux différentes contraintes (une solution de départ)
    Càd qu'on ne peut pas acheter de routes ou de batiments
    Et qu'on a un budget de 50
    """
    invested_map = np.zeros(
        (SIZE_X, SIZE_Y))  # Matrice de la taille de la carte
    to_buy_init = [r.randint(0, SIZE_X), r.randint(0, SIZE_Y)]
    # S'assurer que l'emplacement de départ est libre
    while check_in_map(to_buy_init):
        to_buy_init = (r.randint(0, SIZE_X), r.randint(0, SIZE_Y))
    to_buy = to_buy_init
    budget = 0
    while budget < BUDGET:
        invested_map, budget = buy_position(
            to_buy, invested_map, budget)  # Acheter
        to_buy = select_next_pos(to_buy)  # selection de nouvelle position
    return invested_map


def buy_position(pos, invest_map, budg):
    """Achat d'un terrain"""
    if check_in_map(pos) and check_bought(pos, invest_map):
        budg += COST_MAP[pos[0]][pos[1]]
        invest_map[pos[0]][pos[1]] = 1
    return invest_map, budg


def select_next_pos(pos):
    x = r.randint(0, 3)
    if x == 0:
        pos[0] += 1
    elif x == 1:
        pos[0] -= 1
    elif x == 2:
        pos[1] += 1
    elif x == 3:
        pos[1] -= 1
    return pos


def check_in_map(position):
    """reçoit un tuple (position)
    Vérifie que la position est bien dans la carte, aussi non
    @return False si la position n'est pas achetable ou n'est pas dans la carte
    """
    return ((position[0] <= len(USAGE_MAP[0])) or (position[1] <= len(USAGE_MAP)) or (USAGE_MAP[position[0]][position[1]] == 0))


def check_bought(position, invest_map):
    """Vérifie que la position n'est pas déjà achetée"""
    return invest_map[position[0]][position[1]] == 0


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
solution_claquee = generate_solution()

print(solution_claquee)
