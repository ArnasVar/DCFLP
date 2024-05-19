import math
import pandas as pd
import itertools
def distance(X, Y):
    # Get coordinates by indices in the set I
    lat1 = X.iloc[0]
    lon1 = X.iloc[1]
    lat2 = Y.iloc[0]
    lon2 = Y.iloc[1]

    # distance between latitudes and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0

    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0

    # apply formula
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
         math.cos(lat1) * math.cos(lat2))
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return float(rad * c)
# ==============================================================================
# Attractiveness that customer i feels to the facility j in I
# ==============================================================================


def find_best_combinations(I, J, X, theta, output_file, num_combinations, utility_function, mode):
    best_combinations = []
    best_demand_captured = []

    # Generate all possible combinations of 3 points
    combinations = list(itertools.combinations(range(len(I)), 3))

    with open(output_file, 'w') as file:
        file.write("Combination\tDemand captured\n")
        for combination in combinations:
            # Create subsets of I, containing only the facilities in the current combination
            subset_I = I.iloc[list(combination)]

            # Calculate utility percentage for the current combination
            captured_demand = utility_function(subset_I, J, X, mode)

            # Check if current combination should be included in the best combinations
            if len(best_combinations) < num_combinations:
                best_combinations.append(list(combination))
                best_demand_captured.append(captured_demand)
            else:
                min_utility_index = best_demand_captured.index(min(best_demand_captured))
                if captured_demand > best_demand_captured[min_utility_index]:
                    best_combinations[min_utility_index] = list(combination)
                    best_demand_captured[min_utility_index] = captured_demand

            # Write the combination and its utility percentage to the file
            file.write(f"{combination}\t{captured_demand}\n")
            print(f"{combination}\t{captured_demand}\n")

        file.write(f"{best_combinations}\t{best_demand_captured}\n")
        print(f"{best_combinations}\t{best_demand_captured}\n")
    return best_combinations, best_demand_captured
