import numpy as np

# Définir les deux tuples d'entiers
a = (3, 4)
b = (0, 0)

# Convertir les tuples en tableaux numpy
a_np = np.array(a)
b_np = np.array(b)

# Calculer la distance entre les deux tuples
distance = np.linalg.norm(a_np - b_np)

# Afficher la distance
print("Distance entre", a, "et", b, ":", distance)
