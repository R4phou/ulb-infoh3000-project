from useful import *

time_init = t.time()
print("Initialisation du programme")

# Matrices de données
COST_MAP = read_file("data/Cost_map.txt")
PRODUCTION_MAP = read_file("data/Production_map.txt")
USAGE_MAP = read_usage_file("data/Usage_map.txt")

# Liste des positions de tous les batiments (x,y)
BUILDINGS = position_of_item(2, USAGE_MAP)
# Matrice de proximité
PROXIMITY_MAP = calculate_proximity_map(USAGE_MAP, BUILDINGS)
print("Matrices chargées en", round(t.time() - time_init, 5), "secondes")

SIZE_X = len(COST_MAP[0])  # Taille (largeur) de la carte
SIZE_Y = len(COST_MAP)  # Taille (hauteur) de la carte

BUDGET = 50  # en dizaines de milliers d'euros


"""----------------------------------------------------------------------------------------------------
                                        Génération des solutions
----------------------------------------------------------------------------------------------------"""


def generate_compact_solution():
    """
    Génère une solution qui répond aux différentes contraintes (une solution de départ)
    Càd qu'on ne peut pas acheter de routes ou de batiments
    Et qu'on a un budget de 50
    """
    sol = []
    to_buy = get_initial_pos()
    budget = i = 0
    while budget < BUDGET:
        if i == 15:
            break
        if (check_in_map(to_buy)) and (to_buy not in sol):
            if budget + COST_MAP[to_buy[1]][to_buy[0]] <= BUDGET:
                budget += COST_MAP[to_buy[1]][to_buy[0]]
                sol.append(to_buy)
                i = 0
        else:
            i += 1
        to_buy = select_next_pos(to_buy)  # selection de nouvelle position
    return sol, budget


def generate_random_solution():
    """Génère une solution aléatoire qui répond aux différentes contraintes (une solution de départ)"""
    solution = []
    budget = 0
    i = 0
    while budget < BUDGET:
        if i == 4:
            break
        position = get_initial_pos()
        if (
            budget + COST_MAP[position[1]][position[0]] <= BUDGET
            and check_in_map(position)
            and position not in solution
        ):
            budget += COST_MAP[position[1]][position[0]]
            solution.append(position)
            i = 0
        else:
            i += 1
    return solution, budget


def get_initial_pos():
    """
    Fonction qui renvoie la position initiale à partir de laquelle on va commencer à acheter des terrains
    Vérifie que la position de départ est bien achetable
    """
    pos = [r.randint(0, SIZE_X), r.randint(0, SIZE_Y)]
    # S'assurer que l'emplacement de départ est libre
    while not check_in_map(pos):
        pos = [r.randint(0, SIZE_X), r.randint(0, SIZE_Y)]
    return pos


def select_next_pos(old_pos):
    """Position c'est [x,y]"""
    pos = old_pos[:]
    x = r.randint(0, 3)
    if x == 0 and pos[0] + 1 < SIZE_X:
        pos[0] += 1
    elif x == 1 and 0 <= pos[0] - 1:
        pos[0] -= 1
    elif x == 2 and pos[1] + 1 < SIZE_Y:
        pos[1] += 1
    elif x == 3 and 0 <= pos[1] - 1:
        pos[1] -= 1
    return pos


def get_pos_close_to(pos):
    """Renvoie une position proche de pos"""
    newpos = [SIZE_X + 1, SIZE_Y + 1]
    while not check_in_map(newpos):
        newpos = pos[:]
        x = r.randint(0, 3)
        if x == 0 and newpos[0] + 1 < SIZE_X:
            newpos[0] += 1
        elif x == 1 and 0 <= newpos[0] - 1:
            newpos[0] -= 1
        elif x == 2 and newpos[1] + 1 < SIZE_Y:
            newpos[1] += 1
        elif x == 3 and 0 <= newpos[1] - 1:
            newpos[1] -= 1
    return newpos


def check_in_map(position):
    """
    Reçoit un position = [x, y]
    Vérifie que la position est bien dans la carte, aussi non
    Renvoie False si la position n'est pas achetable ou n'est pas dans la carte
    """
    return (
        (position[0] < SIZE_X)
        and (position[1] < SIZE_Y)
        and (USAGE_MAP[position[1]][position[0]] == 0)
    )


def generate_n_solutions(n):
    """Génère n solutions aléatoires qui répondent aux différentes contraintes (une population de départ)"""
    return [generate_random_solution()[0] for i in range(n)]


def generate_n_compact_solutions(n):
    """Génère n solutions compactes qui répondent aux différentes contraintes (une population de départ)"""
    return [generate_compact_solution()[0] for i in range(n)]


"""----------------------------------------------------------------------------------------------------
                                            Calcul du score
----------------------------------------------------------------------------------------------------"""


def productivity(solution):
    """
    Calcule le score de productivité totale d'une solution
    Solution = matrice de 0 et de 1 (1 = acheté et 0 = Pas acheté)
    """
    score = 0
    for elem in solution:
        score += PRODUCTION_MAP[elem[1]][elem[0]]
    return round(1 - score / 75, 3)


def proximity(solution):
    """Calcule le score de proximité totale d'une solution en sommant la valeur de chaque parcelle de la proximity_map"""
    distance_tot = 0
    for bought in solution:
        distance_tot += PROXIMITY_MAP[bought[1]][bought[0]]
    return round(distance_tot, 3)  # simplifier les calculs en arrondissant


def compacity(solution):
    """Calcule le score de compacité totale d'une solution"""
    score = 0
    n = len(solution)
    for i in range(n):
        for j in range(i + 1, n):
            distance = distance_between_tuple(solution[i], solution[j])
            if distance <= 1:
                score += 0
            elif 1 < distance <= 2:
                score += 1
            else:
                score += 6
    return round(score, 3)


def next_to(parcelle1, parcelle2):
    return distance_between_tuple(parcelle1, parcelle2) <= 1


def get_score(solution):
    """Renvoie la liste des scores [prod, prox, comp]"""
    prod = productivity(solution)
    comp = compacity(solution)
    prox = proximity(solution)
    return [prod, prox, comp]


def get_price(individu):
    """Renvoie le cout d'un individu"""
    price = 0
    for elem in individu:
        price += COST_MAP[elem[1]][elem[0]]
    return price


def get_price_terrain(terrain):
    """Renvoie le cout d'un terrain"""
    return COST_MAP[terrain[1]][terrain[0]]


def get_scores(solutions):
    """Renvoie la liste des scores de chaque solution"""
    return [get_score(solutions[i]) for i in range(len(solutions))]


if __name__ == "__main__":
    import visualize as v

    begin = t.time()
    print("Le programme a pris: ", round(t.time() - begin, 4), "s")
