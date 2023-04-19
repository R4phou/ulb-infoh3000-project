from init import *

QUANTUM_TIME = 1 # quantum de temps de l'univers simulé
BETA_UNIVERSE_CONSTANT = 0.5 # constante utilisé dans le calcul de la constante de gravitation. doit être < 1
FIRST_QUANTUM_GRAVITATIONNAL_CONSTANT = 0.5 # constante de gravitation après le premier quantum de temps


def get_worse_score_individual(population):
    """Renvoie l'individu le moins bon de la population"""
    max = -1
    index = -1
    for i in range(len(population)):
        if get_score(population[i]) > max or max == -1:
            max = get_score(population[i])
            index = i
    return max

def get_best_score_individual(population):
    """Renvoie l'individu le moins bon de la population"""
    min = -1
    index = -1
    for i in range(len(population)):
        if get_score(population[i]) < min or min == -1:
            max = get_score(population[i])
            index = i
    return min

def get_individual_mass(population):
    """Renvoie la masse de chaque individu"""
    mass_list = []
    for i in range(len(population)):
        """"Calcul de la masse de chaque individu (le calcul a été découpé pour + de lisibilité)"""
        delta1 = get_score(population[i])-get_best_score_individual(population)
        delta2 = get_best_score_individual(population[i])-get_worse_score_individual(population)
        individual_mass = delta1/delta2
        mass_list.append(individual_mass)
    return mass_list

def generate_individual_masses(population):
    """Génère la masse de chaque individu"""
    masses = get_individual_mass(population)
    result = []
    for i in range(len(masses)):
        result.append(masses[i]/sum(masses))
    return result

def calculate_gravitationnal_constant(universe_time):
    """Calcul de la constante gravitationnelle au temps universe_time ( > QUANTUM_TIME)"""
    return FIRST_QUANTUM_GRAVITATIONNAL_CONSTANT*((QUANTUM_TIME/universe_time)**BETA_UNIVERSE_CONSTANT)

#A CODER:

def generate_force_matrix(population,individual_masses):
    """Génère la matrice des forces (taille nxn, les valeurs en diagonales n'ont aucune signification (non sens))"""
    matrix_forces = []
    return matrix_forces

def generate_acceleration_matrix(population,individual_masses):
    """Génère la matrice des accélérations (taille 1xn)"""
    matrix_accelerations = []
    return matrix_accelerations

