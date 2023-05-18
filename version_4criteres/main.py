from algo_gen import *
from visualize import *

"""----------------------------------------------------------------------------------------------------
                                    Choix de la manière de launch
----------------------------------------------------------------------------------------------------"""


def get_pareto_frontier(nb_gen, nb_ind):
    time_algo = t.time()
    score_pop, population = algo_genetic(nb_gen)
    score_pop_comp, population_comp = algo_genetic_compact(nb_gen)
    score_pop = np.concatenate((score_pop, score_pop_comp), axis=0)
    population = population + population_comp
    population = selection_dominance_pareto_final(population, score_pop)
    score_pop = get_scores(population)
    print(
        "Temps d'exécution des algorithmes génétiques: ",
        round(t.time() - time_algo, 5),
        "s",
    )
    # sauvegarde les scores
    np.savetxt(
        "version_4criteres/results/scores"
        + str(nb_gen)
        + "_gen_"
        + str(nb_ind)
        + "_pop.csv",
        score_pop,
        delimiter=",",
    )
    # sauvegarde des invividus
    save_pop(population, nb_gen, nb_ind)
    print("Il y a ", len(population), "solutions composant la frontière de Pareto!")
    #     print_usagemap_plus_sol_list(USAGE_MAP, population[0])
    print_4D_solutions(score_pop)


if __name__ == "__main__":
    r.seed(4)
    NB_GENERATIONS = 3000  # Nombre de générations
    NB_INDIVIDUS = 100  # Nombre d'individus par génération
    get_pareto_frontier(NB_GENERATIONS, NB_INDIVIDUS)
    # import amcd as amcd

    # amcd.launch_amcd()
