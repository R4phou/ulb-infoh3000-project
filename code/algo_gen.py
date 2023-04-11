from algo import *


def selection(population, scores_pop):
    """Selection d'un algorithme génétique
    Nico et Raph
    Mercredi 12 aprem 14h
    """


def reproduction(population):
    """Reproduction d'un algorithme génétique
    Alex et Raph
    Vendredi aprem
    """


def mutation(population):
    """Mutation d'un algorithme génétique
    Nico et Alex
    Samedi aprem
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
    begin = t.time()

    print("Le programme a pris: ", round(t.time()-begin, 4), "s")
