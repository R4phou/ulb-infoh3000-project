from init import *
from tqdm import tqdm

QUANTUM_TIME = 1  # quantum de temps de l'univers simulé
# constante utilisé dans le calcul de la constante de gravitation. doit être < 1
BETA_UNIVERSE_CONSTANT = 0.99
# constante de gravitation après le premier quantum de temps
FIRST_QUANTUM_GRAVITATIONNAL_CONSTANT = 50
EPSILON = 0.1  # constante
EPSILON_2 = 0.0000001  # constante pour éviter la division par 0
PRODUCTION_WEIGHT = 0.5  # poids de la production dans le calcul du score
PROXIMITY_WEIGHT = 0.5  # poids de la proximité dans le calcul du score
MAX_PROD = 2.6
MAX_PROX = 330


def get_agent_score(agent):
    """Renvoie le score d'un agent (parcelle)"""
    return (
        PRODUCTION_WEIGHT * PRODUCTION_MAP[agent[1]][agent[0]] / MAX_PROD
        + PROXIMITY_WEIGHT * PROXIMITY_MAP[agent[1]][agent[0]] / MAX_PROX
    )


def get_agent_worse_score(individual):
    """Renvoie la moins bonne parcelle de l'individu"""
    max = -1
    for i in range(len(individual)):
        agent_score = get_agent_score(individual[i])
        if agent_score > max or max == -1:
            max = agent_score
    return max


def get_agent_best_score(individual):
    """Renvoie la meilleure parcelle de l'individu"""
    min = -1
    for i in range(len(individual)):
        agent_score = get_agent_score(individual[i])
        if agent_score < min or min == -1:
            min = agent_score
    return min


def get_agent_mass(individual):
    """Renvoie la masse de chaque parcelle d'un individu (matrice 1xn)"""
    mass_list = []
    for i in range(len(individual)):
        """ "Calcul de la masse de chaque individu (le calcul a été découpé pour + de lisibilité)"""
        delta1 = (
            get_agent_score(individual[i])
            - get_agent_worse_score(individual)
            + EPSILON_2
        )
        delta2 = get_agent_best_score(individual) - get_agent_worse_score(individual)
        individual_mass = delta1 / delta2
        mass_list.append(individual_mass)
    return mass_list


def generate_agent_masses(individual):
    """Génère la masse de chaque individu (matrice 1xn)"""
    masses = get_agent_mass(individual)
    result = []
    tot = sum(masses)
    for i in range(len(masses)):
        result.append(masses[i] / tot)
    return result


def calculate_gravitationnal_constant(universe_time):
    """Calcul de la constante gravitationnelle au temps universe_time ( > QUANTUM_TIME)"""
    return FIRST_QUANTUM_GRAVITATIONNAL_CONSTANT * (
        (QUANTUM_TIME / (universe_time + 1)) ** BETA_UNIVERSE_CONSTANT
    )


def generate_force_matrix(indiviual, universe_time):
    """Génère la matrice des forces (taille 1xn)"""
    matrix_forces = []
    gravitational_constant = calculate_gravitationnal_constant(universe_time)
    matrix_masses = generate_agent_masses(indiviual)
    # Besoin de: G, M, R, x
    for i in range(len(indiviual)):
        force_x = 0
        force_y = 0
        for j in range(len(indiviual)):
            if i != j:
                # Calcul de la distance entre les deux individus (= R_ij)
                distance = distance_between_tuple(indiviual[i], indiviual[j])
                # Calcul de la force gravitationnelle
                force_x += (
                    r.random()
                    * gravitational_constant
                    * matrix_masses[i]
                    * matrix_masses[j]
                    * (indiviual[j][0] - indiviual[i][0])
                    / (distance + EPSILON)
                )
                force_y += (
                    r.random()
                    * gravitational_constant
                    * matrix_masses[i]
                    * matrix_masses[j]
                    * (indiviual[j][1] - indiviual[i][1])
                    / (distance + EPSILON)
                )
        matrix_forces.append([force_x, force_y])
    return matrix_forces


def generate_acceleration_matrix(individual, universe_time):
    """Génère la matrice des accélérations (taille 1xn)"""
    matrix_accelerations = []
    matrix_masses = generate_agent_masses(individual)
    matrix_forces = generate_force_matrix(individual, universe_time)
    for i in range(len(individual)):
        matrix_accelerations.append(
            [
                matrix_forces[i][0] / matrix_masses[i],
                matrix_forces[i][1] / matrix_masses[i],
            ]
        )
    return matrix_accelerations


def generate_velocity_matrix(individual, old_velocity_matrix, universe_time):
    """Génère la matrice des vitesses (taille 1xn)"""
    matrix_velocities = []
    matrix_accelerations = generate_acceleration_matrix(individual, universe_time)
    for i in range(len(individual)):
        velocity_x = r.random() * (
            old_velocity_matrix[i][0] + matrix_accelerations[i][0]
        )
        velocity_y = r.random() * (
            old_velocity_matrix[i][1] + matrix_accelerations[i][1]
        )
        matrix_velocities.append([velocity_x, velocity_y])
    return matrix_velocities


def update_coordinates(individual, old_velocity_matrix, universe_time):
    """Génère la matrice des positions (taille 1xn)"""
    matrix_velocities = generate_velocity_matrix(
        individual, old_velocity_matrix, universe_time
    )

    for i in range(len(individual)):
        individual[i][0] += int(matrix_velocities[i][0])
        individual[i][1] += int(matrix_velocities[i][1])
    old_velocity_matrix = matrix_velocities
    check_no_doubles(individual)


def is_budget_ok(individual):
    """Vérifie si le budget est respecté"""
    price = get_price(individual)
    if price < 43:
        individual.append(get_initial_pos())
    elif price > 50:
        individual.pop(-1)


def init_velocity_matrix(individual):
    """Génère la matrice des vitesses initiales (taille 1xn)"""
    matrix_velocities = []
    for i in range(len(individual)):
        matrix_velocities.append([0, 0])
    return matrix_velocities


def pos_in_individu(individual, pos):
    """Vérifie si la position pos est déjà occupée par un individu"""
    for i in range(len(individual)):
        if individual[i][0] == pos[0] and individual[i][1] == pos[1]:
            return True
    return False


def check_no_doubles(individual):
    """Vérifie qu'il n'y a pas de doublons dans l'individu"""
    for i in range(len(individual)):
        if pos_in_individu(individual, individual[i]):
            individual[i] = get_initial_pos()


def generate_solution(nb_iterations):
    """Génère une solution aléatoire"""
    individual = generate_random_solution()[0]
    # print(individual)
    for i in range(nb_iterations):
        update_coordinates(individual, init_velocity_matrix(individual), i)
        is_budget_ok(individual)
    return individual


def get_initial_population(nb_individuals=100, nb_iterations=1000):
    """Génère une population de solutions aléatoires"""
    population = []
    for i in tqdm(range(nb_individuals), desc="INDIVIDUS GSA"):
        population.append(generate_solution(nb_iterations))
    return population


if __name__ == "__main__":
    NB_ITERATIONS = 1000
    POPULATION_SIZE = 100
    population = get_initial_population(POPULATION_SIZE, NB_ITERATIONS)
    scores = get_scores(population)

    import visualize as v

    # v.print_usagemap_plus_sol_list(USAGE_MAP, individu)
    v.print_3D_solutions(scores)
    v.save_pop(population, NB_ITERATIONS, POPULATION_SIZE)
