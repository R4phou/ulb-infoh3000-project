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
