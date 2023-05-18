from algo_gen import *
from visualize import *

"""----------------------------------------------------------------------------------------------------
                                    Choix de la manière de launch
----------------------------------------------------------------------------------------------------"""


def launch_evolutive_genetic(nb_gen, nb_ind):
    time_algo = t.time()
    population = generate_n_solutions(nb_ind)
    print("Population initiale générée en: ", round(t.time() - time_algo, 5), "s")
    # evolution contient 3 populations a différentes générations
    score_pop, evolution = algo_genetic(population, nb_gen, evolution=True)
    print(
        "Temps d'exécution de l'algorithme génétique: ",
        round(t.time() - time_algo, 5),
        "s",
    )

    # affiche l'évolution des solutions
    print_3D_evolutions(evolution)


def get_pareto_frontier(nb_gen, nb_ind, gsa=False):
    time_algo = t.time()
    score_pop = [[0, 0, 0]]
    if gsa:
        score_pop_gsa, population_gsa = algo_genetic(nb_gen, 100, gravi=True)
    score_pop_random, population_random = algo_genetic(nb_gen, nb_ind)
    score_pop_comp, population_comp = algo_genetic(nb_gen, nb_ind, random=False)
    np.concatenate((score_pop, score_pop_random), axis=0)
    np.concatenate((score_pop, score_pop_comp), axis=0)
    population = population_random + population_comp
    if gsa:
        np.concatenate((score_pop, score_pop_gsa), axis=0)
        population += population_gsa

    # recupération de la frontière de pareto finale
    population = selection_dominance_pareto_final(population, score_pop)
    score_pop = get_scores(population)
    print(
        "Temps d'exécution des algorithmes génétiques: ",
        round(t.time() - time_algo, 5),
        "s",
    )
    if gsa:
        results = {"r": score_pop_random, "g": score_pop_gsa, "b": score_pop_comp}
        show_3d_multicolor(results)
    # sauvegarde les scores
    np.savetxt(
        "result_AMCD/scores" + str(nb_gen) + "_gen_" + str(nb_ind) + "_pop.csv",
        score_pop,
        delimiter=",",
    )

    # sauvegarde des invividus
    save_pop(population, nb_gen, nb_ind)
    print("Il y a ", len(population), "solutions composant la frontière de Pareto!")
    #     print_usagemap_plus_sol_list(USAGE_MAP, population[0])
    print_3D_solutions(score_pop)


if __name__ == "__main__":
    r.seed(4)
    NB_GENERATIONS = 1002  # Nombre de générations
    NB_INDIVIDUS = 1002  # Nombre d'individus par génération
    get_pareto_frontier(NB_GENERATIONS, NB_INDIVIDUS, gsa=True)
    # launch_evolutive_genetic(NB_GENERATIONS, NB_INDIVIDUS)
    # import amcd as amcd

    # amcd.launch_amcd()
