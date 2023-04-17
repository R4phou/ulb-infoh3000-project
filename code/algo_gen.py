from init import *
from tqdm import tqdm


def selection(population, scores_pop):
    """Selection d'un algorithme génétique
    population = liste des solutions
    scores_pop = liste des scores des solutions sous la forme [prod, prox, comp]
    """


def sort_by_dominance(scores_pop):
    """
    Trie les scores de la population selon leur dominance de Pareto
    Renvoie un dictionnaire {it: #domination sur lui}
    """
    n = len(scores_pop)
    dominated_by = {i: 0 for i in range(n)}

    for i1 in range(n):
        for i2 in range(n):
            if i1 == i2:
                continue
            if is_dominated(scores_pop[i1], scores_pop[i2]):
                dominated_by[i2] += 1
    return dominated_by


def selection_dominance_Pareto(population, scores_pop):
    """
    Selection d'un algorithme génétique avec la méthode de dominance de Pareto
    population = liste des solutions
    scores_pop = liste des scores des solutions sous la forme [prod, prox, comp]
    """
    sorted_scores = sort_by_dominance(scores_pop)
    selected_pop = []
    for i, score in sorted(sorted_scores.items(), key=lambda x: x[1]):
        selected_pop.append(population[i])
        if len(selected_pop) == len(population)//2:
            return selected_pop


def is_dominated(ind1, ind2):
    """Fonction qui return true si ind1 est dominé
    False ne veut rien dire (si i1 n'est pas dominé, il n'est pas d'office dominant)
    Args:
        ind1 (list): score de l'individu 1
        ind2 (list): score de l'individu 2
    """
    return ind1[0] <= ind2[0] and ind1[1] <= ind2[1] and ind1[2] <= ind2[2] and (ind1[0] < ind2[0] or ind1[1] < ind2[1] or ind1[2] < ind2[2])


def crossover_simple(individu1, individu2):
    """Crossover d'un algorithme génétique avec une coupe aléatoire
    """
    budget1 = BUDGET+1
    budget2 = BUDGET+1
    test = 0
    while (budget1 > BUDGET and budget2 > BUDGET):
        print(test)
        test += 1
        # prends la longueur min des deux individus
        cut = r.randint(0, min(len(individu1), len(individu2)))
        new_individu1 = individu1[:cut] + individu2[cut:]
        new_individu2 = individu2[:cut] + individu1[cut:]
        budget1 = get_price(new_individu1)
        budget2 = get_price(new_individu2)
    return new_individu1, new_individu2


def crossover_uniform(individu1, individu2):
    """Crossover d'un algorithme génétique avec une coupe aléatoire en respectant le budget
    """
    new_individu1 = []
    new_individu2 = []
    len_individu1 = len(individu1)
    len_individu2 = len(individu2)
    max_len = max(len_individu1, len_individu2)
    for i in range(max_len):
        choose = r.randint(0, 1)
        if i < len_individu1 and get_price(new_individu1) < BUDGET and i < len_individu2:
            if choose == 0:
                if get_price(new_individu1 + [individu1[i]]) <= BUDGET:
                    new_individu1.append(individu1[i])
            else:
                if get_price(new_individu1 + [individu2[i]]) <= BUDGET:
                    new_individu1.append(individu2[i])
        if i < len_individu2 and get_price(new_individu2) < BUDGET and i < len_individu1:
            if choose == 0:
                if get_price(new_individu2 + [individu1[i]]) <= BUDGET:
                    new_individu2.append(individu1[i])
            else:
                if get_price(new_individu2 + [individu2[i]]) <= BUDGET:
                    new_individu2.append(individu2[i])
        while get_price(new_individu1) < BUDGET-3 or get_price(new_individu1) > BUDGET:
            if get_price(new_individu1) > BUDGET:
                new_individu1.pop()
            new_individu1.append(get_initial_pos())
        while get_price(new_individu2) < BUDGET-3 or get_price(new_individu2) > BUDGET:
            if get_price(new_individu2) > BUDGET:
                new_individu2.pop()
            new_individu2.append(get_initial_pos())
    return new_individu1, new_individu2


def sort_by_price(positions):
    """Renvoie la population triée par prix
    """
    pos_prix = [(pos, get_price_terrain(pos)) for pos in positions]
    sorted_pos_prix = sorted(pos_prix, key=lambda x: x[1], reverse=True)
    return sorted_pos_prix


def crossover_no_delete(individu1, individu2):
    """Crossover d'un algorithme génétique avec une coupe aléatoire en respectant le budget
    """
    all_terrain = individu1+individu2
    child1 = individu1[:len(individu1)//2] + individu2[len(individu2)//2:]
    child2 = individu2[:len(individu2)//2] + individu1[len(individu1)//2:]
    a = 0
    sorted_terrains = sort_by_price(all_terrain)
    while get_price(child1) > BUDGET or get_price(child2) > BUDGET or len(child1+child2) != len(all_terrain):
        # print("a =", a, " | ", get_price(child1), " | ", get_price(
        #     child2), " | ", len(child1+child2), " | ", len(all_terrain))
        child1 = []
        child2 = []
        a += 1
        if a < 10:  # teste 10 fois de façon random
            for i in range(0, len(all_terrain), 2):
                x = r.randint(0, 1)
                if x == 0:
                    child1.append(all_terrain[i])
                    if i+1 < len(all_terrain):
                        child2.append(all_terrain[i+1])
                else:
                    child2.append(all_terrain[i])
                    if i+1 < len(all_terrain):
                        child1.append(all_terrain[i+1])
        elif a > 20:  # teste 10 fois en triant par prix
            for i in range(0, len(all_terrain), 2):
                x = r.randint(0, 1)
                if x == 0:
                    child1.append(sorted_terrains[i][0])
                    if i+1 < len(all_terrain):
                        child2.append(sorted_terrains[i+1][0])
                else:
                    child2.append(sorted_terrains[i][0])
                    if i+1 < len(all_terrain):
                        child1.append(sorted_terrains[i+1][0])
        else:
            child1, child2 = crossover_uniform(individu1, individu2)
            break
    # print("Fin:", len(child1+child2), " et ", len(all_terrain),
    #       "|", get_price(child1), 'et', get_price(child2))
    multiple_mutation(child1)
    multiple_mutation(child2)
    return child1, child2


def reproduction(population):
    """Reproduction d'un algorithme génétique
    """
    for i in range(0, len(population), 2):
        individu1 = population[i]
        individu2 = population[i+1]
        child1, child2 = crossover_no_delete(individu1, individu2)
        population.append(child1)
        population.append(child2)


def mutation_simple(individu):
    """Mutation avec une probabilité de 50% d'un terrain"""
    if r.randint(0, 100) < 50:
        change_terrain = r.choice(individu)
        new_terrain = change_terrain
        # retire le prix de l'ancien terrain et ajoute le prix du nouveau terrain
        while (new_terrain in individu) or (get_price(individu)-get_price_terrain(change_terrain)+get_price_terrain(new_terrain) > BUDGET):
            new_terrain = get_initial_pos()
        individu.remove(change_terrain)
        individu.append(new_terrain)


def multiple_mutation(individu):
    """Mutation avec une probabilité de 10% de chaque terrain"""
    for change_terrain in individu:
        if r.randint(0, 100) < 10:
            new_terrain = change_terrain
            # retire le prix de l'ancien terrain et ajoute le prix du nouveau terrain
            while (new_terrain in individu) or (get_price(individu)-get_price_terrain(change_terrain)+get_price_terrain(new_terrain) > BUDGET):
                new_terrain = get_initial_pos()
            individu.remove(change_terrain)
            individu.append(new_terrain)


def mutation(individu):
    """Mutation d'un algorithme génétique
    """
    mutation_simple(individu)
    # multiple_mutation(population)


def algo_genetic(population, nb_gen):
    score_pop = get_scores(population)
    for gen in tqdm(range(nb_gen), desc="Générations"):
        population = selection_dominance_Pareto(population, score_pop)
        reproduction(population)
        score_pop = get_scores(population)
    population = selection_dominance_Pareto(population, score_pop)
    score_pop = get_scores(population)
    return score_pop, population


def algo_genetic_evolution(population, nb_gen):
    score_pop = get_scores(population)
    evolution0 = score_pop
    for gen in tqdm(range(nb_gen), desc="Générations"):
        population = selection_dominance_Pareto(population, score_pop)
        reproduction(population)
        score_pop = get_scores(population)
        if gen == nb_gen//2:
            evolution1 = score_pop
    return score_pop, [evolution0, evolution1, score_pop]


if __name__ == "__main__":
    import visualize as v
    begin = t.time()
    population_100 = generate_n_solutions(1000)
    score_pop = algo_genetic(population_100, 100)
    print("Le programme a pris: ", round(t.time()-begin, 4), "s")
    v.print_3D_solutions(score_pop)
