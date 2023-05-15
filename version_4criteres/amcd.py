import algo_gen as ag
import visualize as v
from useful import *


Q = 4
CRITERES = ["Production", "Proximité", "Compacité", "Impact"]


"""----------------------------------------------------------------------------------------------------
                                    Chargement des données
----------------------------------------------------------------------------------------------------"""


def getData():
    SCORES = np.loadtxt(
        "version_4criteres/results/scores"
        + str(NBGEN)
        + "_gen_"
        + str(NBPOP)
        + "_pop.csv",
        delimiter=",",
    )
    # prends le maximum de chaque colonne pour normaliser
    MAXS = [max(SCORES[:, i]) for i in range(len(SCORES[0]))]
    SCORES = normalise(SCORES, MAXS)
    POPULATION = v.read_pop(
        "version_4criteres/results/pop" + str(NBGEN) + "_gen_" + str(NBPOP) + "_pop.txt"
    )
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


def print_solution(sol):
    """Affiche la meilleure solution PROMETHEE II"""
    print("Meilleure solution PROMETHEE II :")
    print("POIDS : ", POIDS)
    print("Flux net : ", sol[0])
    print("Individu : ", sol[1][0])
    print("Scores : ", sol[1][1])
    print("Budget : ", ag.get_price(sol[1][0]))
    v.print_usagemap_plus_sol_list(ag.USAGE_MAP, sol[1][0])


def print_all_solutions(sol):
    """Affiche toutes les solutions PROMETHEE II"""
    for i in sol:
        print_solution(i)
        print("\n")


def launch_amcd():
    begin = t.time()
    global SCORES, POPULATION, POPU_SCORE
    SCORES, POPULATION, POPU_SCORE = getData()
    print("Début de la méthode PROMETHEE II")
    sol = prometheeII()
    print("Fin de la méthode PROMETHEE II en: ", round(t.time() - begin, 5), "s")
    scores = [sol[i][1][1] for i in range(len(sol))]
    print_solution(sol[0])

    v.print_4D_solutions_with_best(scores, sol[0][1][1])


POIDS = [0.5, 0.5, 100, 100]
SEUIL_PREF = [0.7, 0.7, 0.7, 0.7]
SEUIL_INDIF = [0.2, 0.2, 0.2, 0.2]
NBGEN = 1000
NBPOP = 1000
if __name__ == "__main__":
    launch_amcd()
