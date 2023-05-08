import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import Axes3D
import useful as u

MAX_COMP = 5500
MAX_PROD = 1
MAX_PROX = 330
MAX_IMPACT = 1


def print_usagemap_plus_sol_list(usage, sol):
    """
    sol = liste des positions de terrains (positions également des listes)
    USAGE_MAP: 0 libre/ 1 Route/ 2 Construction
    """
    mat = usage
    # [vide, route, constru, acheté, erreur]
    couleurs = ['white', 'lightblue', 'red',  'blue', 'green']
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
    couleurs = ['white', 'lightblue', 'red',  'blue', 'green']
    cmap = ListedColormap(couleurs)
    fig, ax = plt.subplots()
    ax.matshow(mat, cmap=cmap)
    ax.set_title("USAGE MAP")
    plt.show()


def print_maps(prod_map, cost_map, prox_map, impact_map):
    fig, axs = plt.subplots(nrows=2, ncols=2)
    axs[0, 0].set_title("Production Map")
    axs[0, 0].matshow(prod_map, cmap=plt.cm.Oranges)
    axs[0, 1].set_title("Cost Map")
    axs[0, 1].matshow(cost_map, cmap=plt.cm.Blues)
    axs[1, 0].set_title("Proximity Map")
    axs[1, 0].matshow(prox_map, cmap=plt.cm.Greens)
    axs[1, 1].set_title("Impact Map")
    axs[1, 1].matshow(impact_map, cmap=plt.cm.Greens)
    plt.show()


def print_4D_solutions(scores):
    prod, prox, comp, imp = [sublst[0] for sublst in scores], [sublst[1] for sublst in scores], [
        sublst[2] for sublst in scores], [sublst[3] for sublst in scores]
    maxes = [max(prod), max(prox), max(comp), max(imp)]
    print("maxes done")
    prod = u.normalize(prod, maxes[0])
    prox = u.normalize(prox, maxes[1])
    comp = u.normalize(comp, maxes[2])
    imp = u.normalize(imp, maxes[3])
    print("normlaisation done")
    fig, axs = plt.subplots(nrows=2, ncols=3)
    axs[0, 0].set_title("Prod vs Prox")
    axs[0, 0].scatter(prod, prox, c='r')
    axs[0, 1].set_title("Prod vs Comp")
    axs[0, 1].scatter(prod, comp, c='r')
    axs[0, 2].set_title("Prod vs Impact")
    axs[0, 2].scatter(prod, imp, c='r')
    axs[1, 0].set_title("Prox vs Comp")
    axs[1, 0].scatter(prox, comp, c='r')
    axs[1, 1].set_title("Prox vs Impact")
    axs[1, 1].scatter(prox, imp, c='r')
    axs[1, 2].set_title("Comp vs Impact")
    axs[1, 2].scatter(comp, imp, c='r')
    plt.show()


def print_4D_solutions_with_best(scores, best_score):
    prod, prox, comp, imp = [sublst[0] for sublst in scores], [sublst[1] for sublst in scores], [
        sublst[2] for sublst in scores], [sublst[3] for sublst in scores]
    maxes = [max(prod), max(prox), max(comp), max(imp)]
    prod = u.normalize(prod, maxes[0])
    prox = u.normalize(prox, maxes[1])
    comp = u.normalize(comp, maxes[2])
    imp = u.normalize(imp, maxes[3])
    best_score = [best_score[0]/maxes[0], best_score[1] /
                  maxes[1], best_score[2]/maxes[2], best_score[3]/maxes[3]]
    fig, axs = plt.subplots(nrows=2, ncols=3)
    axs[0, 0].set_title("Prod vs Prox")
    axs[0, 0].scatter(prod, prox, c='r')
    axs[0, 0].scatter(best_score[0], best_score[1], c='b')
    axs[0, 1].set_title("Prod vs Comp")
    axs[0, 1].scatter(prod, comp, c='r')
    axs[0, 1].scatter(best_score[0], best_score[2], c='b')
    axs[0, 2].set_title("Prod vs Impact")
    axs[0, 2].scatter(prod, imp, c='r')
    axs[0, 2].scatter(best_score[0], best_score[3], c='b')
    axs[1, 0].set_title("Prox vs Comp")
    axs[1, 0].scatter(prox, comp, c='r')
    axs[1, 0].scatter(best_score[1], best_score[2], c='b')
    axs[1, 1].set_title("Prox vs Impact")
    axs[1, 1].scatter(prox, imp, c='r')
    axs[1, 1].scatter(best_score[1], best_score[3], c='b')
    axs[1, 2].set_title("Comp vs Impact")
    axs[1, 2].scatter(comp, imp, c='r')
    axs[1, 2].scatter(best_score[2], best_score[3], c='b')
    plt.show()


def save_pop(population, nb_gen, nb_ind):
    """population est une liste de solutions sous la forme d'une liste d'individu
    un individu est une liste de liste [x,y]
    """
    with open("version_4criteres/results/pop"+ str(nb_gen)+"_gen_"+str(nb_ind)+"_pop.txt", "w") as f:
        for i in range(len(population)):
            for j in range(len(population[i])):
                f.write(str(population[i][j][0])+","+str(population[i][j][1]))
                if j < len(population[i])-1:
                    f.write("|")
            if i < len(population)-1:
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


if __name__ == "__main__":
    import init as init
    NB_GEN = 500
    NB_POP = 1000
    NUM_IND = 48
   
