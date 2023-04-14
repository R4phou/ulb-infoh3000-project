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
    test =0
    while (budget1 > BUDGET and budget2 > BUDGET):
        print(test)
        test+=1
        cut = r.randint(0, min(len(individu1),len(individu2))) #prends la longueur min des deux individus
        new_individu1 = individu1[:cut] + individu2[cut:]
        new_individu2 = individu2[:cut] + individu1[cut:]
        budget1 = get_price(new_individu1)
        budget2 = get_price(new_individu2)
    return new_individu1,new_individu2

def crossover_uniform(individu1, individu2):
    """Crossover d'un algorithme génétique avec une coupe aléatoire en respectant le budget
    """
    budget1 = BUDGET+1
    budget2 = BUDGET+1
    test =0
    while (budget1 > BUDGET and budget2 > BUDGET):
        print(test)
        test+=1
        new_individu1 = []
        new_individu2 = []
        for i in range(min(len(individu1),len(individu2))):
            if r.randint(0,1) == 0:
                new_individu1.append(individu1[i])
                new_individu2.append(individu2[i])
            else:
                new_individu1.append(individu2[i])
                new_individu2.append(individu1[i])
        budget1 = get_price(new_individu1)
        budget2 = get_price(new_individu2)
        print(budget1,budget2)
    return new_individu1,new_individu2

def reproduction(population):
    """Reproduction d'un algorithme génétique
    """
    for i in range(0,len(population),2):
        individu1 = population[i]
        individu2 = population[i+1]
        print(get_price(individu1),get_price(individu2))
        child1,child2 = crossover_simple(individu1,individu2)
        population.append(child1)
        population.append(child2)     


def mutation(population):
    """Mutation d'un algorithme génétique
    Nico et Alex
    """


def algo_genetic(population, nb_gen):
    score_pop = get_scores(population)
    #v.print_3D_solutions(score_pop)
    for gen in range(nb_gen):
        print("Génération n°", gen)
        population=selection_dominance_Pareto(population, score_pop)
        reproduction(population)
        score_pop = get_scores(population)
        mutation(population)
    v.print_3D_solutions(score_pop)


if __name__ == "__main__":
    import visualize as v
    r.seed(1)
    begin = t.time()
    population_100 = generate_n_solutions(100)
    algo_genetic(population_100, 50)
    print("Le programme a pris: ", round(t.time()-begin, 4), "s")
