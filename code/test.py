import numpy as np

a = [[1, 2, 3], [4, 5, 6]]
b = [[1, 2, 3], [4, 5, 6]]
c = np.concatenate((a, b), axis=0)
print(c)
