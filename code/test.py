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
            if if_dominated(scores_pop[i1], scores_pop[i2]):
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
    for i, score in enumerate(sorted_scores):
        if score == 0:
            selected_pop.append(population[i])
    return selected_pop


def if_dominated(ind1, ind2):
    """Fonction qui return true si ind1 est dominé
    False ne veut rien dire (si i1 n'est pas dominé, il n'est pas d'office dominant)
    Args:
        ind1 (list): score de l'individu 1
        ind2 (list): score de l'individu 2
    """
    return ind1[0] <= ind2[0] and ind1[1] <= ind2[1] and ind1[2] <= ind2[2] and (ind1[0] < ind2[0] or ind1[1] < ind2[1] or ind1[2] < ind2[2])


# dominated_by = {i: set() for i in range(4)}

# dominated_by[2].add(4)

# print(dominated_by)
