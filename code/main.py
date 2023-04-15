from algo_gen import *
from visualize import *


def launch_evolutive_genetic(nb_gen, nb_ind):
    time_algo = t.time()
    population = generate_n_solutions(nb_ind)
    score_pop, population = algo_genetic_evolution(population, nb_gen)
    print("Temps d'exécution de l'algorithme génétique: ",
          round(t.time() - time_algo, 5), "s")
    print_3D_evolutions(population)


def launch_normal_genetic(nb_gen, nb_ind):
    time_algo = t.time()
    population = generate_n_solutions(nb_ind)
    score_pop, population = algo_genetic(population, nb_gen)
    print("Temps d'exécution de l'algorithme génétique: ",
          round(t.time() - time_algo, 5), "s")
    np.savetxt("results/scores_gen"+str(nb_gen)+"_pop" +
               str(nb_ind)+".csv", score_pop, delimiter=",")
    print_3D_solutions(score_pop)
    print_usagemap_plus_sol_list(USAGE_MAP, population[0])


if __name__ == "__main__":
    r.seed(4)
    NB_GENERATIONS = 200  # Nombre de générations
    NB_INDIVIDUS = 100  # Nombre d'individus par génération
    launch_normal_genetic(NB_GENERATIONS, NB_INDIVIDUS)
