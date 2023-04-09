import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def print_usagemap_plus_sol(usage, sol):
    """
    USAGE_MAP: 0 libre/ 1 Route/ 2 Construction
    """
    mat = usage
    # [vide, route, constru, acheté, erreur]
    couleurs = ['white', 'lightblue', 'red',  'blue', 'green']
    cmap = ListedColormap(couleurs)
    for i in range(len(usage)):
        for j in range(len(usage[0])):
            if (sol[i][j] == 1 and usage[i][j] == 0):
                mat[i][j] = 3
            elif sol[i][j] == 1 and usage[i][j] != 0:
                mat[i][j] = 4
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


if __name__ == "__main__":
    import algo as m
    print_usagemap_plus_sol(m.USAGE_MAP, m.generate_solution()[0])
    # print_maps(m.PRODUCTION_MAP, m.COST_MAP)
