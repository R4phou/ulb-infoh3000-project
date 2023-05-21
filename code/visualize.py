import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import Axes3D

MAX_COMP = 500
MAX_PROD = 1
MAX_PROX = 330


def print_usagemap_plus_sol_list(usage, sol):
    """
    sol = liste des positions de terrains (positions également des listes)
    USAGE_MAP: 0 libre/ 1 Route/ 2 Construction
    """
    mat = usage
    # [vide, route, constru, acheté, erreur]
    couleurs = ["white", "lightblue", "red", "blue", "green"]
    cmap = ListedColormap(couleurs)
    for elem in sol:
        if usage[elem[1]][elem[0]] == 0:
            mat[elem[1]][elem[0]] = 3
        else:
            mat[elem[1]][elem[0]] = 4
    fig, ax = plt.subplots()
    ax.matshow(mat, cmap=cmap)
    ax.set_title("USAGE MAP et Achat (vert)")
    plt.show()


def print_usage_map(usage):
    """
    USAGE_MAP: 0 libre/ 1 Route/ 2 Construction
    """
    mat = usage
    # [vide, route, constru, acheté, erreur]
    couleurs = ["white", "lightblue", "red", "blue", "green"]
    cmap = ListedColormap(couleurs)
    fig, ax = plt.subplots()
    ax.matshow(mat, cmap=cmap)
    ax.set_title("USAGE MAP")
    plt.show()


def print_maps(prod_map, cost_map, prox_map):
    fig, axs = plt.subplots(3)
    axs[0].set_title("Production Map")
    axs[0].matshow(prod_map, cmap=plt.cm.Oranges)
    axs[1].set_title("Cost Map")
    axs[1].matshow(cost_map, cmap=plt.cm.Blues)
    axs[2].set_title("Proximity Map")
    axs[2].matshow(prox_map, cmap="hot")
    plt.show()


def print_map(map, nom):
    fig, ax = plt.subplots()
    ax.set_title(nom)
    ax.matshow(map, cmap=plt.cm.Greens)
    plt.show()


def print_3D_solutions(scores):
    """
    Fonction qui reçoit en paramètre une liste des scores de toutes les solutions
    [prod, prox, comp] = [x, y, z]

    """
    # Créer la figure et l'axe 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlabel("Productivity")
    ax.set_ylabel("Proximity")
    ax.set_zlabel("Compacity")
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    ax.set_zlim(0, 1.0)

    # Les coordonnées des points
    prods = [i[0] / MAX_PROD for i in scores]
    proxs = [i[1] / MAX_PROX for i in scores]
    comps = [i[2] / MAX_COMP for i in scores]

    # Ajouter les points à l'axe 3D
    ax.scatter(prods, proxs, comps, c="r")
    # Afficher le graphique
    plt.show()


def print_3D_solutions_AMCD(scores, best):
    """
    Fonction qui reçoit en paramètre une liste des scores de toutes les solutions
    [prod, prox, comp] = [x, y, z]

    """
    # Créer la figure et l'axe 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlabel("Productivity")
    ax.set_ylabel("Proximity")
    ax.set_zlabel("Compacity")
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    ax.set_zlim(0, 1.0)

    # Les coordonnées des points
    prods = [i[0] for i in scores]
    proxs = [i[1] for i in scores]
    comps = [i[2] for i in scores]

    # Ajouter les points à l'axe 3D
    ax.scatter(prods, proxs, comps, c="violet")
    ax.scatter(best[0], best[1], best[2], c="green")
    # Afficher le graphique
    plt.show()


def print_3D_evolutions(scores):
    """
    Fonction qui reçoit en paramètre une liste contenant les scores initiaux, intermédiaires et finaux des solutions
    [prod, prox, comp] = [x, y, z]
    """
    # Créer la figure et l'axe 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlabel("Productivity")
    ax.set_ylabel("Proximity")
    ax.set_zlabel("Compacity")
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    ax.set_zlim(0, 1.0)

    # Les coordonnées des points
    prods0 = [i[0] / MAX_PROD for i in scores[0]]
    proxs0 = [i[1] / MAX_PROX for i in scores[0]]
    comps0 = [i[2] / MAX_COMP for i in scores[0]]

    # Ajouter les points à l'axe 3D
    ax.scatter(prods0, proxs0, comps0, c="r")
    # Les coordonnées des points
    prods1 = [i[0] / MAX_PROD for i in scores[1]]
    proxs1 = [i[1] / MAX_PROX for i in scores[1]]
    comps1 = [i[2] / MAX_COMP for i in scores[1]]

    # Ajouter les points à l'axe 3D
    ax.scatter(prods1, proxs1, comps1, c="b")
    # Les coordonnées des points
    prods2 = [i[0] / MAX_PROD for i in scores[2]]
    proxs2 = [i[1] / MAX_PROX for i in scores[2]]
    comps2 = [i[2] / MAX_COMP for i in scores[2]]

    # Ajouter les points à l'axe 3D
    ax.scatter(prods2, proxs2, comps2, c="g")

    # Afficher le graphique
    plt.show()


def save_pop(population, nb_gen, nb_ind, seed=4):
    """
    population est une liste de solutions sous la forme d'une liste d'individu
    un individu est une liste de liste [x,y]
    """
    with open(
        "result_AMCD/population"
        + str(nb_gen)
        + "_gen_"
        + str(nb_ind)
        + "_pop_"
        + str(seed)
        + "_seed.txt",
        "w",
    ) as f:
        for i in range(len(population)):
            for j in range(len(population[i])):
                f.write(str(population[i][j][0]) + "," + str(population[i][j][1]))
                if j < len(population[i]) - 1:
                    f.write("|")
            if i < len(population) - 1:
                f.write("\n")


def read_pop(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        population = []
        for line in lines:
            ind = []
            for i in line.split("|"):
                ind.append([int(i.split(",")[0]), int(i.split(",")[1])])
            population.append(ind)
    return population


def show_3d_multicolor(results_dictionnary):
    """ "
    Affiche chacun des résultats en 3D selon une couleur attribuée.
    format du dictionnaire: {couleur:population}
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlabel("Productivity")
    ax.set_ylabel("Proximity")
    ax.set_zlabel("Compacity")
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    ax.set_zlim(0, 1.0)

    for color in results_dictionnary.keys():
        # Les scores de la population considérée
        score_pop = results_dictionnary[color]

        # Les coordonnées des points
        prods = [i[0] / MAX_PROD for i in score_pop]
        proxs = [i[1] / MAX_PROX for i in score_pop]
        comps = [i[2] / MAX_COMP for i in score_pop]

        # Ajouter les points à l'axe 3D
        ax.scatter(prods, proxs, comps, c=color, s=4)
    # Afficher le graphique
    plt.show()


def print_conv(iteration, prod, prox, comp):
    """Affiche les graphiques de convergence"""
    fig, axs = plt.subplots(3)
    axs[0].set_title("Convergence of Productivity")
    axs[0].scatter(iteration, prod, c="purple")
    axs[1].set_title("Convergence of Proximity")
    axs[1].scatter(iteration, prox, c="purple")
    axs[2].set_title("Convergence of Compac")
    axs[2].scatter(iteration, comp, c="purple")
    plt.show()


if __name__ == "__main__":
    import init as init

    NB_GEN = 1000
    NB_POP = 1000
    NUM_IND = 48
    filename = "result_AMCD/scores" + str(NB_GEN) + "_gen_" + str(NB_POP) + "_pop.csv"
    print_maps(init.PRODUCTION_MAP, init.COST_MAP, init.PROXIMITY_MAP)
    saved_scores = np.loadtxt(filename, delimiter=",")
    print_3D_solutions(saved_scores)
