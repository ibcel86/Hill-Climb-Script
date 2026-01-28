import random
import pandas as pd
import matplotlib.pyplot as plt
import math


def load_matrix(filename):
    df = pd.read_csv(filename, header=None, names=["x", "y"])
    coords = df.values.tolist()

    n = len(coords)
    matrix = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            x1, y1 = coords[i]
            x2, y2 = coords[j]
            dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            matrix[i][j] = dist

    return matrix

def initial_solution(n):
    tour = list(range(n))
    random.shuffle(tour)
    return tour

def get_neighbors(tour):
    neighbors = []
    for i in range(len(tour) - 1):
        new_tour = tour[:]
        new_tour[i], new_tour[i+1] = new_tour[i+1], new_tour[i]
        neighbors.append(new_tour)
    return neighbors

def tour_cost(tour, matrix):
    cost = 0
    for i in range(len(tour) - 1):
        cost += matrix[tour[i]][tour[i+1]]
    cost += matrix[tour[-1]][tour[0]]  
    return cost

def steepest_hill_climb(matrix, max_no_improve=100):
    n = len(matrix)
    current = initial_solution(n)
    current_cost = tour_cost(current, matrix)

    no_improve_count = 0
    iteration = 0
    history = []

    while no_improve_count < max_no_improve:
        neighbors = get_neighbors(current)

        best_neighbor = current
        best_cost = current_cost

        for neighbor in neighbors:
            cost = tour_cost(neighbor, matrix)
            if cost < best_cost:
                best_neighbor = neighbor
                best_cost = cost

        history.append({"iteration": iteration, "cost": current_cost})

        if best_cost < current_cost:
            current = best_neighbor
            current_cost = best_cost
            no_improve_count = 0
        else:
            no_improve_count += 1

        iteration += 1

    return current, current_cost, history

RUNS = 10
matrix = load_matrix("TSP Matrix.csv")

all_runs_data = []

plt.figure()

for run in range(RUNS):
    best_tour, best_cost, history = steepest_hill_climb(matrix)

    df = pd.DataFrame(history)
    csv_name = f"steepest_hill_climb_run_{run+1}.csv"
    df.to_csv(csv_name, index=False)

    plt.plot(df["iteration"], df["cost"], label=f"Run {run+1}")

    all_runs_data.append((run+1, best_cost))

    print(f"Run {run+1} Best Cost:", best_cost)


plt.title("Steepest Hill Climbing TSP — Cost vs Iterations (10 Runs)")
plt.xlabel("Iteration")
plt.ylabel("Cost")
plt.legend()
plt.grid(True)
plt.show()

summary_df = pd.DataFrame(all_runs_data, columns=["Run", "Best Cost"])
print("\nSummary of Runs:")
print(summary_df)
