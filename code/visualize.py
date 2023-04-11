import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import Axes3D


def print_usagemap_plus_sol_list(usage, sol):
    """
    sol = liste des tuples de terrains
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


def print_maps(prod_map, cost_map):
    fig, axs = plt.subplots(2)
    axs[0].set_title("Production Map")
    axs[0].matshow(prod_map, cmap=plt.cm.Oranges)
    axs[1].set_title("Cost Map")
    axs[1].matshow(cost_map, cmap=plt.cm.Blues)
    plt.show()


def print_3D_solutions(scores):
    """Fonction qui reçoit en paramètre une liste des scores de toutes les solutions
    [prod, prox, comp] = [x, y, z]

    """
    # Créer la figure et l'axe 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('Productivity')
    ax.set_ylabel('Proximity')
    ax.set_zlabel('Compacity')
    ax.set_xlim(1, 3)
    ax.set_ylim(0, 500)
    ax.set_zlim(0, 5000)

    # Les coordonnées des points
    prods = [i[0] for i in scores]
    proxs = [i[1] for i in scores]
    comps = [i[2] for i in scores]

    # Ajouter les points à l'axe 3D
    ax.scatter(prods, proxs, comps, c='r')

    # Afficher le graphique
    plt.show()


if __name__ == "__main__":
    import algo as m
    # print_usagemap_plus_sol_list(m.USAGE_MAP, m.generate_random_solution()[0])
    # print_maps(m.PRODUCTION_MAP, m.COST_MAP)
    print_3D_solutions(scores=0)
