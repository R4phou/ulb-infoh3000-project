from init import *
from tqdm import tqdm

"""----------------------------------------------------------------------------------------------------
                                    Etape de sélection
----------------------------------------------------------------------------------------------------"""


def is_dominated(ind1, ind2):
    """Fonction qui return true si ind1 est dominé
    False ne veut rien dire (si i1 n'est pas dominé, il n'est pas d'office dominant)
    Args:
        ind1 (list): score de l'individu 1
        ind2 (list): score de l'individu 2
    """
    return (
        ind1[0] <= ind2[0]
        and ind1[1] <= ind2[1]
        and ind1[2] <= ind2[2]
        and (ind1[0] < ind2[0] or ind1[1] < ind2[1] or ind1[2] < ind2[2])
    )


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
        if len(selected_pop) == len(population) // 2:
            return selected_pop


def selection_dominance_pareto_final(population, scores_pop):
    """
    Selection d'un algorithme génétique avec la méthode de dominance de Pareto
    population = liste des solutions
    scores_pop = liste des scores des solutions sous la forme [prod, prox, comp]
    """
    sorted_scores = sort_by_dominance(scores_pop)
    selected_pop = []
    for i, score in sorted(sorted_scores.items(), key=lambda x: x[1]):
        if score == 0:
            selected_pop.append(population[i])
    return selected_pop


"""----------------------------------------------------------------------------------------------------
                                    Etape de reproduction
----------------------------------------------------------------------------------------------------"""


def no_crossover(parent1, parent2):
    """Replique les parents"""
    child1 = parent1[:]
    child2 = parent2[:]
    return child1, child2


def reproduction_compact(population):
    """Reproduction d'un algorithme génétique"""
    for i in range(0, len(population), 2):
        individu1 = population[i]
        individu2 = population[i + 1]
        child1, child2 = no_crossover(individu1, individu2)
        mutation_compact(child1)
        mutation_compact(child2)
        population.append(child1)
        population.append(child2)


"""----------------------------------------------------------------------------------------------------
                                    Etape de mutation
----------------------------------------------------------------------------------------------------"""


def mutation_simple_compact(individu):
    """Mutation avec une probabilité de 50% d'un terrain"""
    if r.randint(0, 100) < 100:
        change_terrain = r.choice(individu)
        new_terrain = change_terrain[:]
        # retire le prix de l'ancien terrain et ajoute le prix du nouveau terrain
        i = 0
        while (new_terrain in individu) or (
            get_price(individu)
            - get_price_terrain(change_terrain)
            + get_price_terrain(new_terrain)
            > BUDGET
        ):
            new_terrain = get_pos_close_to(change_terrain)
            i += 1
            if i > 4:
                change_terrain = r.choice(individu)
                i = 0
        individu.remove(change_terrain)
        individu.append(new_terrain)


def multiple_mutation_compact(individu):
    """Mutation d'un chaque terrain"""
    return generate_compact_solution()[0]


def mutation_compact(individu):
    """Mutation d'un algorithme génétique"""
    mutation_simple_compact(individu)
    multiple_mutation_compact(individu)


"""----------------------------------------------------------------------------------------------------
                                    Algorithme complet
----------------------------------------------------------------------------------------------------"""


def algo_genetic(population, nb_gen):
    score_pop = get_scores(population)
    for gen in tqdm(range(nb_gen), desc="Générations"):
        population = selection_dominance_Pareto(population, score_pop)
        reproduction(population)
        score_pop = get_scores(population)
    population = selection_dominance_pareto_final(population, score_pop)
    score_pop = get_scores(population)
    return score_pop, population


def algo_genetic_compact(nb_gen):
    population = generate_n_compact_solutions(nb_gen)
    score_pop = get_scores(population)
    for gen in tqdm(range(nb_gen), desc="Générations"):
        population = selection_dominance_Pareto(population, score_pop)
        reproduction_compact(population)
        score_pop = get_scores(population)
    population = selection_dominance_pareto_final(population, score_pop)
    score_pop = get_scores(population)
    return score_pop, population


def algo_genetic_evolution(population, nb_gen):
    score_pop = get_scores(population)
    evolution0 = score_pop
    for gen in tqdm(range(nb_gen), desc="Générations"):
        population = selection_dominance_Pareto(population, score_pop)
        reproduction(population)
        score_pop = get_scores(population)
        if gen == nb_gen // 2:
            evolution1 = score_pop
    population = selection_dominance_pareto_final(population, score_pop)
    score_pop = get_scores(population)
    return score_pop, [evolution0, evolution1, score_pop]


if __name__ == "__main__":
    import visualize as v

    begin = t.time()
    population_100 = generate_n_compact_solutions(1000)
    score_pop, population = algo_genetic(population_100, 100)
    print("Le programme a pris: ", round(t.time() - begin, 4), "s")
    # print(score_pop)
    np.savetxt("score_pop.txt", score_pop)
    v.print_3D_solutions(score_pop)
