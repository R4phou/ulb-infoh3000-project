from algo import *
from visualize import *

if __name__ == "__main__":
    solution, budget = generate_solution()
    print_usagemap_plus_sol(USAGE_MAP, PRODUCTION_MAP, solution)
    print(budget)
