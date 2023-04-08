import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import main


def print_usagemap_plus_sol(usage, production, sol):
    """
    USAGE_MAP: 0 libre/ 1 Route/ 2 Construction
    """
    mat = usage
    # [vide, route, constru, acheté, erreur]
    couleurs = ['white', 'lightblue', 'red',  'blue', 'green']
    cmap = ListedColormap(couleurs)
    for i in range(len(usage)):
        for j in range(len(usage[0])):
            if sol[i][j] == 1 and usage[i][j] == 0:
                mat[i][j] = 3
            elif sol[i][j] == 1 and usage[i][j] != 0:
                mat[i][j] = 4
    fig, ax = plt.subplots()
    ax.matshow(mat, cmap=cmap)
    ax.set_title("USAGE MAP et Achat (vert)")
    # ax[1].set_title("Production Map")
    # im = ax[1].imshow(production, cmap=plt.cm.Blues)
    # ax[1].matshow(production, cmap=plt.cm.Blues)
    # plt.colorbar(im)
    plt.show()


if __name__ == "__main__":
    import main as m
    print_usagemap_plus_sol(
        m.USAGE_MAP, m.PRODUCTION_MAP, m.generate_solution())
