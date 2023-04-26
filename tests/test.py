import matplotlib.pyplot as plt
import numpy as np

# Données à tracer
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.tan(x)
y4 = np.exp(x)

# Création des subplots en 2 colonnes
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))

# Tracé des données dans chaque subplot
axs[0, 0].plot(x, y1)
axs[0, 0].set_title('Sin(x)')

axs[0, 1].plot(x, y2)
axs[0, 1].set_title('Cos(x)')

axs[1, 0].plot(x, y3)
axs[1, 0].set_title('Tan(x)')

axs[1, 1].plot(x, y4)
axs[1, 1].set_title('Exp(x)')

# Affichage des subplots
plt.tight_layout()
plt.show()
