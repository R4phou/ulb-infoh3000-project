from useful import *

r.seed(4)


COST_MAP = read_file("data/Cost_map.txt")
PRODUCTION_MAP = read_file("data/Production_map.txt")
USAGE_MAP = read_usage_file("data/Usage_map.txt")


# Liste des positions de tous les batiments (x,y)
BUILDINGS = position_of_item(2, USAGE_MAP)

SIZE_X = len(COST_MAP[0])  # Taille (largeur) de la carte
SIZE_Y = len(COST_MAP)  # Taille (hauteur) de la carte

BUDGET = 50  # en dizaines de milliers d'euros
PROD_MAX = 10000  # Valeur max du score de productivité
PROX_MAX = 10000  # Valeur max du score de proximité
COMP_MAX = 10000  # Valeur max du score de compacité


# Poids de la somme pondérée [Proximité, Productivité, Compacité]
WEIGHTS = [1, 1, 1]

"""----------------------------------------------------------------------------------------------------
                                        Génération des solutions
----------------------------------------------------------------------------------------------------"""


def generate_random_solution_list():
    solution = []
    budget = 0
    while budget < BUDGET:
        position = get_initial_pos()
        if check_in_map(position) and position not in solution:
            budget += COST_MAP[position[1]][position[0]]
            solution.append(position)
    return solution, budget


def generate_compact_solution_list():
    """
    Génère une solution qui répond aux différentes contraintes (une solution de départ)
    Càd qu'on ne peut pas acheter de routes ou de batiments
    Et qu'on a un budget de 50
    """
    sol = []
    to_buy = get_initial_pos()
    budget = i = 0
    while budget < BUDGET:
        if i == 4:
            break
        if (budget + COST_MAP[to_buy[1]][to_buy[0]] <= BUDGET) and (to_buy not in sol) and check_in_map(to_buy):
            budget += COST_MAP[to_buy[1]][to_buy[0]]
            sol.append(to_buy)
            i = 0
        else:
            i += 1
        to_buy = select_next_pos(to_buy)  # selection de nouvelle position
    return sol, budget


def get_initial_pos():
    """Fonction qui renvoie la position initiale à partir de laquelle on va commencer à acheter des terrains
    Vérifie que la position de départ est bien achetable
    """
    pos = [r.randint(0, SIZE_X), r.randint(0, SIZE_Y)]
    # S'assurer que l'emplacement de départ est libre
    while not check_in_map(pos):
        pos = [r.randint(0, SIZE_X), r.randint(0, SIZE_Y)]
    return pos


def buy_position(pos, invest_map, budg):
    """Achat d'un terrain"""
    if check_in_map(pos) and check_bought(pos, invest_map):
        budg += COST_MAP[pos[1]][pos[0]]
        invest_map[pos[1]][pos[0]] = 1
    return invest_map, budg


def select_next_pos(pos):
    """Position c'est [x,y]"""
    x = r.randint(0, 3)
    if x == 0 and pos[0]+1 < SIZE_X:
        pos[0] += 1
    elif x == 1 and 0 <= pos[0]-1:
        pos[0] -= 1
    elif x == 2 and pos[1]+1 < SIZE_Y:
        pos[1] += 1
    elif x == 3 and 0 <= pos[1]-1:
        pos[1] -= 1
    return pos


def check_in_map(position):
    """reçoit un position = [x, y]
    Vérifie que la position est bien dans la carte, aussi non
    @return False si la position n'est pas achetable ou n'est pas dans la carte
    """
    return ((position[0] < SIZE_X) and (position[1] < SIZE_Y) and (USAGE_MAP[position[1]][position[0]] == 0))


def check_bought(position, invest_map):
    """Vérifie que la position n'est pas déjà achetée"""
    return invest_map[position[1]][position[0]] == 0


"""----------------------------------------------------------------------------------------------------
                                            Calcul du score
----------------------------------------------------------------------------------------------------"""


def productivity_list(solution):
    """Calcule le score de productivité totale d'une solution
    Solution = matrice de 0 et de 1 (1 = acheté et 0 = Pas acheté)
    """
    score = 0
    for elem in solution:
        score += PRODUCTION_MAP[elem[1]][elem[0]]
    return score


def proximity_list(solution):
    """Calcule le score de proximité totale d'une solution
    La proximité est la distance entre les bâtiments (2 dans USAGE_MAP) et le terrain acheté
    retourne la plus grande distance
    PROXIMITE A MAXIMISER car 1000/distance_tot
    """
    # boughts = position_of_item(1, solution)
    distance = 100000
    distance_tot = 0
    for bought in solution:
        for building in BUILDINGS:  # pour chaque terrain acheté, on regarde la distance minimale avec un batiment
            distance = min(distance, distance_between_tuple(bought, building))
        distance_tot += distance  # on ajoute la distance minimale pour un terrain
    return round(1000/distance_tot, 3)  # simplifier les calculs


def compacity_list(solution):
    """Calcule le score de compacité totale d'une solution"""
    # boughts = position_of_item(1, solution)
    distance_tot = 0
    for bought in solution:
        for i in range(len(solution)):
            distance_tot += distance_between_tuple(bought, solution[i])
    return round(1000/distance_tot, 3)


def calcul_global_score_list(solution, weights):
    """Renvoie la somme pondérée des scores partiels"""
    prod = productivity_list(solution)
    comp = compacity_list(solution)
    prox = proximity_list(solution)
    return weights[0]*prod/PROD_MAX + weights[1]*prox/PROX_MAX + weights[2]*comp/COMP_MAX


def get_score_list(solution):
    """Renvoie la liste des scores [prod, prox, comp]"""
    prod = productivity_list(solution)
    comp = compacity_list(solution)
    prox = proximity_list(solution)
    return [prod, prox, comp]


"""----------------------------------------------------------------------------------------------------
                                    Implémentation de l'algorithme
----------------------------------------------------------------------------------------------------"""


if __name__ == "__main__":
    import visualize
    begin = t.time()
    solution_claquee, budget = generate_compact_solution_list()
    print("Budget utilisé: ", budget)
    print(get_score_list(solution_claquee))
    print("Le programme a pris: ", round(t.time()-begin, 4), "s")
    visualize.print_usagemap_plus_sol_list(
        USAGE_MAP, solution_claquee)
