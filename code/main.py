from algo_gen import *
from visualize import *

if __name__ == "__main__":
    r.seed(4)
    NB_GENERATIONS = 500  # Nombre de générations
    NB_INDIVIDUS = 1000  # Nombre d'individus par génération
    time_algo = t.time()
    population = generate_n_solutions(NB_INDIVIDUS)
    score_pop,population = algo_genetic(population, NB_GENERATIONS)
    print("Temps d'exécution de l'algorithme génétique: ", round(t.time() - time_algo,5), "s")
    np.savetxt("results/scores_gen"+str(NB_GENERATIONS)+"_pop"+str(NB_INDIVIDUS)+".csv", score_pop, delimiter=",")
    print_3D_solutions(score_pop)
    print_usagemap_plus_sol_list(USAGE_MAP, population[0])
