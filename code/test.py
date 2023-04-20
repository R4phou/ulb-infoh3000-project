import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata


def normalize(x, max):
    return [i/max for i in x]


# Charger le nuage de points
mat = np.loadtxt("results/scores_gen300_pop500.csv",
                 dtype=float, delimiter=",")


MAX_COMP = 5500
MAX_PROD = 2.6
MAX_PROX = 330

# Diviser les points en coordonnées x, y et z
x = mat[:, 0]
y = mat[:, 1]
z = mat[:, 2]
x = normalize(x, MAX_PROD)
y = normalize(y, MAX_PROX)
z = normalize(z, MAX_COMP)


# Créer une grille régulière pour la surface
xi = np.linspace(min(x), max(x), 100)
yi = np.linspace(min(y), max(y), 100)
xi, yi = np.meshgrid(xi, yi)

# Interpoler les valeurs de z sur la grille régulière à l'aide de la méthode de l'interpolation
zi = griddata((x, y), z, (xi, yi), method='linear')

# Visualiser la surface interpolée à l'aide de Matplotlib
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(xi, yi, zi)
plt.show()
