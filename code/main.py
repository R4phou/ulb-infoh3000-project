"""
    Projet AMCD: Exploitation Agricole
    Date : 21/05/2023
    Ecole : Université Libre de Bruxelles, Ecole Polytechnique de Bruxelles
    Auteurs : Alexandre ACHTEN, Nicolas GUILBAUD, Raphaël HUMBLET
    Ce projet a pour but de générer une frontière de Pareto pour le problème de l'achat de terrains dans une carte comportant des zones constructibles et non constructibles.
    Il prend en compte les différentes contraintes du problème et les différentes solutions possibles.
    Il utilise pour cela un algorithme génétique et un algorithme de recherche gravitationnelle (heuristique).
"""
from algo_gen import *
from visualize import *


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


def get_pareto_frontier(nb_gen, nb_ind, gsa=False, seed=4, show_graph=True):
    """Fonction qui lance l'algorithme génétique aléatoire et compacte et qui affiche et sauvegarde les scores et la population de
    la frontière de Pareto finale
    Args:
        nb_gen (int): nombre de génération effectuées par les algorithmes génétiques
        nb_ind (int): nombre d'individus par population génération
        gsa (bool, optional): Mettre à True pour que l'algorithme GSA soit aussi réalisé (souvent à false car assez lent). Defaults to False.
    """
    time_algo = t.time()
    score_tot = [[0, 0, 0]]
    if gsa:
        score_pop_gsa, population_gsa = algo_genetic(nb_gen, 100, gravi=True)

    score_pop_random, population_random = algo_genetic(nb_gen, nb_ind)
    score_pop_comp, population_comp = algo_genetic(nb_gen, nb_ind, random=False)

    pop_list = [population_random, population_comp]

    if gsa:
        pop_list.append(population_gsa)

    population_tot_generee = flatten(pop_list)
    score_pop_generee = get_scores(population_tot_generee)

    # recupération de la frontière de pareto finale
    population_tot_filtree = selection_dominance_pareto_final(
        population_tot_generee, score_pop_generee
    )
    score_pop_filtree = get_scores(population_tot_filtree)
    print(
        "Temps d'exécution des algorithmes génétiques: ",
        round(t.time() - time_algo, 5),
        "s",
    )
    if gsa:
        results = {"r": score_pop_random, "g": score_pop_gsa, "b": score_pop_comp}
        if show_graph:
            show_3d_multicolor(results)
    # sauvegarde les scores
    np.savetxt(
        "result_AMCD/scores"
        + str(nb_gen)
        + "_gen_"
        + str(nb_ind)
        + "_pop_"
        + str(seed)
        + "_seed.csv",
        score_pop_filtree,
        delimiter=",",
    )

    # sauvegarde des invividus
    save_pop(population_tot_filtree, nb_gen, nb_ind, seed=seed)
    print(
        "Il y a ",
        len(population_tot_filtree),
        "solutions composant la frontière de Pareto!",
    )
    #     print_usagemap_plus_sol_list(USAGE_MAP, population[0])
    if show_graph:
        print_3D_solutions(score_pop_filtree)


if __name__ == "__main__":
    r.seed(4)
    NB_GENERATIONS = 42  # Nombre de générations
    NB_INDIVIDUS = 42  # Nombre d'individus par génération
    get_pareto_frontier(NB_GENERATIONS, NB_INDIVIDUS, gsa=True)
    import amcd as amcd

    amcd.launch_amcd()
