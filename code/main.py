from algo_gen import *
from visualize import *


def launch_evolutive_genetic(nb_gen, nb_ind):
    time_algo = t.time()
    population = generate_n_solutions(nb_ind)
    print("Population initiale générée en: ",
          round(t.time() - time_algo, 5), "s")
    # evolution contient 3 populations a différentes générations
    score_pop, evolution = algo_genetic_evolution(population, nb_gen)
    print("Temps d'exécution de l'algorithme génétique: ",
          round(t.time() - time_algo, 5), "s")

    # affiche l'évolution des solutions
    print_3D_evolutions(evolution)


def launch_normal_genetic(nb_gen, nb_ind):
    time_algo = t.time()
    population = generate_n_solutions(nb_ind)
    score_pop, population = algo_genetic(population, nb_gen)
    print("Temps d'exécution de l'algorithme génétique: ",
          round(t.time() - time_algo, 5), "s")

    # sauvegarde les scores
    np.savetxt("results/scores_gen"+str(nb_gen)+"_pop" +
               str(nb_ind)+".csv", score_pop, delimiter=",")

    # permet de sauvegarder les individus
    for i in range(45, 51):
        np.savetxt("results/ind"+str(i)+"_gen"+str(nb_gen)+"_pop" +
                   str(nb_ind)+".csv", population[i], delimiter=",")
    # affiche les solutions
    print(len(population))
    print_3D_solutions(score_pop)


if __name__ == "__main__":
    # r.seed(4)
    NB_GENERATIONS = 500  # Nombre de générations
    NB_INDIVIDUS = 1000  # Nombre d'individus par génération
    launch_normal_genetic(NB_GENERATIONS, NB_INDIVIDUS)
