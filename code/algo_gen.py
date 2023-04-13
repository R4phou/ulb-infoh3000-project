from algo import *


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
    scores_sel = []
    for i, score in sorted(sorted_scores.items(), key=lambda x: x[1]):
        # if score == 0:
        selected_pop.append(population[i])
        scores_sel.append(scores_pop[i])
        if len(selected_pop) == len(population)//2:
            return selected_pop, scores_sel


def if_dominated(ind1, ind2):
    """Fonction qui return true si ind1 est dominé
    False ne veut rien dire (si i1 n'est pas dominé, il n'est pas d'office dominant)
    Args:
        ind1 (list): score de l'individu 1
        ind2 (list): score de l'individu 2
    """
    return ind1[0] <= ind2[0] and ind1[1] <= ind2[1] and ind1[2] <= ind2[2] and (ind1[0] < ind2[0] or ind1[1] < ind2[1] or ind1[2] < ind2[2])


def reproduction(population):
    """Reproduction d'un algorithme génétique
    Alex et Raph
    """


def mutation(population):
    """Mutation d'un algorithme génétique
    Nico et Alex
    """


def algo_genetic(population, nb_gen):
    score_pop = get_scores(population)
    for gen in range(nb_gen):
        print("Génération n°", gen)
        selection(population, score_pop)
        reproduction(population)
        score_pop = get_scores(population)
        mutation(population)
    return score_pop


if __name__ == "__main__":
    import visualize as v
    r.seed(1)
    begin = t.time()
    population_100 = generate_n_solutions(100)
    scores_pop_100 = get_scores(population_100)
    print(scores_pop_100)

    newpop, newscore = selection_dominance_Pareto(
        population_100, scores_pop_100)
    print("--------------------------------------------------------------------------\n",
          newscore)
    print(len(scores_pop_100))
    print(len(newscore))
    print("Le programme a pris: ", round(t.time()-begin, 4), "s")
    v.print_3D_solutions(scores_pop_100)
    v.print_3D_solutions(newscore)
