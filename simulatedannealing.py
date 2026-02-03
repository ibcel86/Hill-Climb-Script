import csv
import random
import math
import matplotlib.pyplot as plt

def load_cities(filename):
    cities = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 2:
                continue
            try:
                x = float(row[0])
                y = float(row[1])
                cities.append((x, y))
            except ValueError:
                continue
    return cities

def initial_solution(cities):
    solution = list(range(len(cities)))
    random.shuffle(solution)
    return solution

def swap_adjacent(solution):
    if len(solution) < 2:
        return solution[:]
    new_solution = solution[:]
    i = random.randint(0, len(solution) - 2)
    new_solution[i], new_solution[i + 1] = new_solution[i + 1], new_solution[i]
    return new_solution


def inversion(solution):
    if len(solution) < 2:
        return solution[:]
    new_solution = solution[:]
    i, j = sorted(random.sample(range(len(solution)), 2))
    new_solution[i:j + 1] = reversed(new_solution[i:j + 1])
    return new_solution

def tour_cost(solution, cities):
    cost = 0
    for i in range(len(solution)):
        x1, y1 = cities[solution[i]]
        x2, y2 = cities[solution[(i + 1) % len(solution)]]
        cost += math.hypot(x2 - x1, y2 - y1)
    return cost

def simulated_annealing(
    cities,
    Tmax=10.0,
    Tmin=0.0005,
    alpha=0.995,
    neighborhood=inversion
):
    initial = initial_solution(cities)
    current = initial[:]
    current_cost = tour_cost(current, cities)

    best = current[:]
    best_cost = current_cost

    T = Tmax
    costs = [best_cost]

    while T > Tmin:
        candidate = neighborhood(current)
        candidate_cost = tour_cost(candidate, cities)
        delta = candidate_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / T):
            current = candidate
            current_cost = candidate_cost

        if current_cost < best_cost:
            best = current[:]
            best_cost = current_cost

        costs.append(best_cost)
        T *= alpha

    return initial, best, best_cost, costs

def plot_tour(cities, solution, title, color="red"):
    x = [cities[i][0] for i in solution]
    y = [cities[i][1] for i in solution]

    # Close the loop
    x.append(cities[solution[0]][0])
    y.append(cities[solution[0]][1])

    plt.figure(figsize=(6, 6))
    plt.scatter(
        [c[0] for c in cities],
        [c[1] for c in cities],
        color="blue",
        label="Cities"
    )
    plt.plot(x, y, color=color, linewidth=2, label=title)

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(title)
    plt.axis("equal")
    plt.legend()
    plt.show()

def main():
    cities = load_cities("TSP Matrix.csv")
    print("Loaded cities:", len(cities))

    all_runs = []
    best_overall = None
    best_overall_cost = float("inf")
    best_initial = None

    plt.figure()

    for i in range(10):
        initial, best, cost, costs = simulated_annealing(cities)

        all_runs.append(cost)

        if cost < best_overall_cost:
            best_overall = best
            best_overall_cost = cost
            best_initial = initial

        plt.plot(costs, alpha=0.6)

    plt.xlabel("Iterations")
    plt.ylabel("Best tour cost")
    plt.title("Simulated Annealing Convergence (10 runs)")
    plt.show()

    print("Best costs from 10 runs:", all_runs)
    print("Best overall cost:", best_overall_cost)

    plot_tour(
        cities,
        best_initial,
        title="Initial Random Tour",
        color="gray"
    )

    plot_tour(
        cities,
        best_overall,
        title=f"Best Tour (Cost = {best_overall_cost:.2f})",
        color="red"
    )


if __name__ == "__main__":
    main()
