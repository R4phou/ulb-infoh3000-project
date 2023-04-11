from algo import *
from visualize import *

if __name__ == "__main__":
    solution, budget = generate_compact_solution()
    print_usagemap_plus_sol_list(USAGE_MAP, solution)
    print(budget)
