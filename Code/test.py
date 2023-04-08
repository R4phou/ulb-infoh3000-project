import numpy as np
import matplotlib.pyplot as plt

# Données pour les graphes
x = np.linspace(0, 2*np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.tan(x)

# Création de la figure et des sous-figures
fig, axs = plt.subplots(3, 1, figsize=(8, 8))

# Tracé des graphes sur les sous-figures
axs[0].plot(x, y1)
axs[0].set_title('Sinus')
axs[1].plot(x, y2)
axs[1].set_title('Cosinus')
axs[2].plot(x, y3)
axs[2].set_title('Tangente')

# Affichage de la figure
plt.show()
