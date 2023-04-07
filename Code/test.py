import numpy as np
import matplotlib.pyplot as plt

matrice = np.loadtxt("Results/sol_claq.txt")
fig, ax = plt.subplots()

min_val, max_val = 0, 70

intersection_matrix = np.random.randint(0, 10, size=(max_val, max_val))

ax.matshow(intersection_matrix, cmap=plt.cm.Blues)

for i in range(15):
    for j in range(15):
        c = intersection_matrix[j,i]
        ax.text(i, j, str(c), va='center', ha='center')
plt.show()
print(matrice)
