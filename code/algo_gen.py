from init import *
from tqdm import tqdm
import algo_gsa as gsa

"""----------------------------------------------------------------------------------------------------
                                    Etape de sélection
----------------------------------------------------------------------------------------------------"""


def is_dominated(ind1, ind2):
    """Fonction qui return true si ind1 est dominé
    False ne veut rien dire (si i1 n'est pas dominé, il n'est pas d'office dominant)
    ind1 (list): score de l'individu 1"""
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


def reproduction(population):
    """Reproduction d'un algorithme génétique"""
    for i in range(0, len(population), 2):
        individu1 = population[i]
        individu2 = population[i + 1]
        child1, child2 = no_crossover(individu1, individu2)  # copie des parents
        mutation(child1)
        mutation(child2)
        population.append(child1)
        population.append(child2)


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


def mutation_simple(individu):
    """Mutation avec une probabilité de 100% d'un terrain"""
    if r.randint(0, 100) < 100:
        change_terrain = r.choice(individu)
        new_terrain = change_terrain
        # retire le prix de l'ancien terrain et ajoute le prix du nouveau terrain
        while (new_terrain in individu) or (
            get_price(individu)
            - get_price_terrain(change_terrain)
            + get_price_terrain(new_terrain)
            > BUDGET
        ):
            new_terrain = get_initial_pos()
        individu.remove(change_terrain)
        individu.append(new_terrain)


def multiple_mutation(individu):
    """Mutation avec une probabilité de 10% de chaque terrain"""
    for change_terrain in individu:
        if r.randint(0, 100) < 10:
            new_terrain = change_terrain
            # retire le prix de l'ancien terrain et ajoute le prix du nouveau terrain
            while (new_terrain in individu) or (
                get_price(individu)
                - get_price_terrain(change_terrain)
                + get_price_terrain(new_terrain)
                > BUDGET
            ):
                new_terrain = get_initial_pos()
            individu.remove(change_terrain)
            individu.append(new_terrain)


def mutation(individu):
    """Mutation d'un algorithme génétique"""
    mutation_simple(individu)
    multiple_mutation(individu)


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
                                Critère d'arrêt et convergence
----------------------------------------------------------------------------------------------------"""


def moyenne_score(scores_pop):
    """Retourne la moyenne des scores de la population
    Score = [prod, prox, comp]"""
    m_prod = m_prox = m_comp = 0
    for i in scores_pop:
        m_prod += i[0]
        m_prox += i[1]
        m_comp += i[2]
    return [
        m_prod / len(scores_pop),
        m_prox / len(scores_pop),
        m_comp / len(scores_pop),
    ]


def convergence_algo_genetic(nb_gen, nb_ind, random=True):
    import visualize as v

    if random:
        population = generate_n_solutions(nb_ind)
    else:
        population = generate_n_compact_solutions(nb_ind)
    score_pop = get_scores(population)
    iteration = []
    prod = []
    prox = []
    comp = []
    for gen in tqdm(range(nb_gen), desc="Générations normales"):
        population = selection_dominance_Pareto(population, score_pop)
        a, b, c = moyenne_score(score_pop)
        iteration.append(gen)
        prod.append(a)
        prox.append(b)
        comp.append(c)
        if random:
            reproduction(population)
        else:
            reproduction(population)
        score_pop = get_scores(population)
    v.print_conv(iteration, prod, prox, comp)
    population = selection_dominance_pareto_final(population, score_pop)
    score_pop = get_scores(population)
    return score_pop, population


"""----------------------------------------------------------------------------------------------------
                                    Algorithme complet
----------------------------------------------------------------------------------------------------"""


def algo_genetic(nb_gen, nb_ind, random=True, gravi=False, evolution=False):
    if random:
        desc = "Générations normales"
        population = generate_n_solutions(nb_ind)
    else:
        desc = "Générations compactes"
        population = generate_n_compact_solutions(nb_ind)
    if gravi:
        desc = "Générations GSA"
        population = gsa.get_initial_population(nb_ind, nb_iterations=1000)
    if evolution:
        evolution0 = get_scores(population)
    score_pop = get_scores(population)
    for gen in tqdm(range(nb_gen), desc=desc):
        population = selection_dominance_Pareto(population, score_pop)
        if random:
            reproduction(population)
        else:
            reproduction_compact(population)
        if evolution and gen == nb_gen // 2:
            evolution1 = get_scores(population)
        score_pop = get_scores(population)
    population = selection_dominance_pareto_final(population, score_pop)
    score_pop = get_scores(population)
    if evolution:
        evolution2 = score_pop
        return score_pop, [evolution0, evolution1, evolution2]
    return score_pop, population


def compare_algorithms(nb_gen, nb_ind):
    """
    compare les résultats obtenus avec les différentes génération de populations initiales:
    - aléatoire
    - compact
    - GSA
    """
    import visualize as v

    time_algo = t.time()
    score_gsa, population_gsa = algo_genetic(nb_gen, nb_ind, gravi=True)
    score_pop, population = algo_genetic(nb_gen, nb_ind)
    score_pop_comp, population_comp = algo_genetic(nb_gen, nb_ind, random=False)
    print("Temps d'exécution: ", round(t.time() - time_algo, 5), "s")
    results = {"r": score_pop, "g": score_gsa, "b": score_pop_comp}

    v.show_3d_multicolor(results)


if __name__ == "__main__":
    # compare_initial_populations(500, 500)
    convergence_algo_genetic(1000, 100, False)
