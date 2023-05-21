import algo_gen as ag
import visualize as v
import main as m
import os.path as f
from useful import *


"""----------------------------------------------------------------------------------------------------
                                    Chargement des données
----------------------------------------------------------------------------------------------------"""


def get_data(use_seed=False, seed=4):
    """Charge les données"""
    score_file_name = "result_AMCD/scores" + str(NBGEN) + "_gen_" + str(NBPOP) + "_pop"
    pop_file_name = (
        "result_AMCD/population" + str(NBGEN) + "_gen_" + str(NBPOP) + "_pop"
    )
    if use_seed:
        score_file_name += "_" + str(seed) + "_seed"
        pop_file_name += "_" + str(seed) + "_seed"
    score_file_name += ".csv"
    pop_file_name += ".txt"
    SCORES = np.loadtxt(
        score_file_name,
        delimiter=",",
    )
    # prends le maximum de chaque colonne pour normaliser
    MAXS = [max(SCORES[:, i]) for i in range(len(SCORES[0]))]
    SCORES = normalise(SCORES, MAXS)
    POPULATION = v.read_pop(pop_file_name)
    POPU_SCORE = to_tuple_liste(POPULATION, SCORES)
    return SCORES, POPULATION, POPU_SCORE


"""----------------------------------------------------------------------------------------------------
                                    1.Préférences mono-critères
----------------------------------------------------------------------------------------------------"""


def get_dk(sol_1, sol_2, critere):
    """
    sol1 et sol2 sont des tuples (individu, score)
    """
    return sol_1[1][critere] - sol_2[1][critere]


def preference_monocritere(sol_1, sol_2, critere):
    """
    sol1 et sol2 sont des tuples (individu, score)
    """
    dk = get_dk(sol_1, sol_2, critere)
    if dk < SEUIL_INDIF[critere]:
        return 0
    if dk > SEUIL_PREF[critere]:
        return 1
    return (
        1 / (SEUIL_PREF[critere] - SEUIL_INDIF[critere]) * (dk - SEUIL_INDIF[critere])
    )


"""----------------------------------------------------------------------------------------------------
                                    2.Matrice de préférence
----------------------------------------------------------------------------------------------------"""


def matrice_preference(sol_1, sol_2, w):
    """matrice de préférence entre deux solutions"""
    return sum(w[i] * preference_monocritere(sol_1, sol_2, i) for i in range(len(w)))


"""----------------------------------------------------------------------------------------------------
                                    3.Calcul des flux
----------------------------------------------------------------------------------------------------"""


def flux_pos(ai):
    """Calcule le flux positif de l'individu ai"""
    return (
        1
        / (len(POPU_SCORE) - 1)
        * sum(matrice_preference(ai, aj, POIDS) for aj in POPU_SCORE)
    )


def flux_neg(ai):
    """Calcule le flux négatif de l'individu ai"""
    return (
        1
        / (len(POPU_SCORE) - 1)
        * sum(matrice_preference(aj, ai, POIDS) for aj in POPU_SCORE)
    )


"""----------------------------------------------------------------------------------------------------
                                    4.Calcul des flux nets totaux
----------------------------------------------------------------------------------------------------"""


def flux_net(ai):
    """Calcule le flux net de l'individu ai"""
    return flux_pos(ai) - flux_neg(ai)


def fluxes_net_population():
    """Calcule les flux nets de la population"""
    return {flux_net(ai): ai for ai in POPU_SCORE}


"""----------------------------------------------------------------------------------------------------
                                    Implémentation de PROMETHEE II
----------------------------------------------------------------------------------------------------"""


def prometheeII():
    """Méthode de PROMETHEE II"""
    return sorted(fluxes_net_population().items())


"""----------------------------------------------------------------------------------------------------
                         Affichage de la meilleure solution PROMETHEE II
----------------------------------------------------------------------------------------------------"""


def print_solution(sol, show_graph):
    """Affiche la meilleure solution PROMETHEE II"""
    print("Meilleure solution PROMETHEE II :")
    print("POIDS : ", POIDS)
    print("Flux net : ", sol[0])
    print("Individu : ", sol[1][0])
    print("Scores : ", sol[1][1])
    print("Budget : ", ag.get_price(sol[1][0]))
    if show_graph:
        v.print_usagemap_plus_sol_list(ag.USAGE_MAP, sol[1][0])


def print_all_solutions(sol, show_graph):
    """Affiche toutes les solutions PROMETHEE II"""
    for i in sol:
        print_solution(i, show_graph)
        print("\n")


def launch_amcd(show_graphs=True, seed=4, use_seed=False):
    """Lance AMCD"""
    begin = t.time()
    global SCORES, POPULATION, POPU_SCORE
    SCORES, POPULATION, POPU_SCORE = get_data(seed=seed, use_seed=use_seed)
    print("Début de la méthode PROMETHEE II")
    sol = prometheeII()
    print("Fin de la méthode PROMETHEE II en: ", round(t.time() - begin, 5), "s")
    scores = [sol[i][1][1] for i in range(len(sol))]
    print_solution(sol[0], show_graphs)
    if show_graphs:
        v.print_3D_solutions_AMCD(scores, best=sol[0][1][1])


"""----------------------------------------------------------------------------------------------------
                                    Etude de la stabilité
----------------------------------------------------------------------------------------------------"""


def stabilite_poids():
    """Lance AMCD avec des poids différents"""
    weight_list = [
        [0.5, 0.5, 0.5],
        [1, 0.5, 0.5],
        [0.5, 1, 0.5],
        [0.5, 0.5, 1],
        [1, 1, 1],
        [0.3, 0.3, 0.3],
        [0.7, 0.7, 0.7],
        [1, 0.7, 0.7],
        [1, 0.2, 0.5],
    ]

    for weight in weight_list:
        global POIDS
        POIDS = weight
        separator_print()
        launch_amcd(show_graphs=False)


def stabilite_generations(nb_gen, nb_ind, nb_exec=3):
    """Lance AMCD avec des générations issues de seed différentes"""
    # Les seeds utilisées. Elles sont comprises entre 0 et nb_exec-1 inclus
    seed_list = [i for i in range(4, 4 + nb_exec)]
    # exécute la recherche Pareto puis amcd pour chaque seed
    for s in seed_list:
        seed_separator_print(s)
        if not f.exists(
            "result_AMCD/population"
            + str(NBGEN)
            + "_gen_"
            + str(NBPOP)
            + "_pop_"
            + str(s)
            + "_seed.txt"
        ):
            print("Population non trouvée, création...")
            m.get_pareto_frontier(nb_gen, nb_ind, gsa=True, seed=s, show_graph=False)
        launch_amcd(show_graphs=False, seed=s, use_seed=True)


CRITERES = ["Production", "Proximité", "Compacité"]
POIDS = [0.5, 0.5, 0.5]
SEUIL_PREF = [0.9, 0.9, 0.9]
SEUIL_INDIF = [0.05, 0.05, 0.05]
NBGEN = 1000
NBPOP = 1000

if __name__ == "__main__":
    stabilite_poids()
    # stabilite_generations(NBGEN,NBPOP)
