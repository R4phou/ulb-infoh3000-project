import numpy as np
from sklearn.datasets import make_regression  # pip install scikit-learn
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
Generate a model of the form f(x) = ax²+bx+c
For a multi variable problem (x1, x2, ..., xn)

In order to do so, just change n_features( = number of variables you need)

It must be printed in 3D (matplotlib not used)
"""
"""1. Dataset"""

N = 2
# Putting n_features=2 sets 2 variables (x1 and x2)
mat = np.loadtxt("results/scores_gen300_pop100.csv",
                 dtype=float, delimiter=",")
# print("mat", mat)
x = mat[:, 1:3]
y = mat[:, 0]
# print("x", x)
# y = y + abs(y/2)  # On n'a plus qqch de linéaire
y = y.reshape(y.shape[0], 1)  # Redimensionner y


# Création de la matrice X (Ici x c'est x1 et x2 et puis on lui colle des 1)
X = np.hstack((x, np.ones((x.shape[0], 1))))
print(X)


# Vecteur Theta de dimension (n+1, 1) avec n le nombre de variables
theta = np.random.randn(N+1, 1)
print(theta)
"""Modèle"""


def model(X, theta):
    """Fonction F(X)= X x THETA
    X = variables
    THETA = constantes à déterminer pour minimiser le coût
    """
    return X.dot(theta)


def cost_function(X, y, theta):
    """Formule du coût (erreur quadratique), renvoie le coût total/erreur total"""
    m = len(y)
    return 1/(2*m)*np.sum((model(X, theta) - y)**2)


def grad(X, y, theta):
    m = len(y)
    return 1/m * X.T.dot(model(X, theta)-y)


def gradient_descent(X, y, theta, learning_rate, n_iterations):
    for i in range(0, n_iterations):
        theta = theta - learning_rate * grad(X, y, theta)
    return theta


def gradient_descent_with_min_graph(X, y, theta, learning_rate, n_iterations):
    """Même fonction mais qui permet de montrer l'efficacité suite au nombre d'itérations"""
    cost_history = np.zeros(n_iterations)
    for i in range(0, n_iterations):
        theta = theta - learning_rate * grad(X, y, theta)
        cost_history[i] = cost_function(X, y, theta)
    return theta, cost_history


def coef_determination(y, pred):
    """7. Evaluer la performance du modèle en évaluant un coefficient de détermination
    R² =  1 - sum(y-f(x))²/ sum(y-y')²
    """
    u = ((y-pred)**2).sum()
    v = ((y-y.mean())**2).sum()
    return 1-u/v


"""5. Entraînement du modèle"""
theta_final, cost_history = gradient_descent_with_min_graph(
    X, y, theta, learning_rate=0.004, n_iterations=1000)

print(theta_final)

predictions = model(X, theta_final)
print(coef_determination(y, predictions))


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('Productivity')
ax.set_ylabel('Proximity')
ax.set_zlabel('Compacity')

ax.scatter(x[:, 0], x[:, 1], y, c='b')
ax.scatter(x[:, 0], x[:, 1], predictions, c='r')
plt.show()
plt.plot(range(1000), cost_history)
plt.show()
