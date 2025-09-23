from utils import readInput
from initial_population import initialPopulation
from fitness_evaluation import calculateFitness, calculateTotalDistance
from crossover import crossover
from mutation import mutate
from GATypes import Tour, Population
from constants import get_hyperparams
from utils import writeOutput


def main() -> None:
    # keeps track of the number of generations that dont produce a good outcome
    count = 0
    tourSize, listOfCities = readInput("input/input1.txt")

    params = get_hyperparams(tourSize)
    pop_size = params.population
    generations = params.generations
    mut_rate = params.mutation_rate
    run_threshold = params.threshold
    nearest_fraction = params.nearest_fraction

    # create hybrid initial population using the params' nearest_fraction
    population: Population = initialPopulation(listOfCities, pop_size,
                                               nearest_fraction)

    probabilities = calculateFitness(population)
    best_cost = float('infinity')
    best_tour: Tour = []

    for _ in range(generations):
        if count > run_threshold:
            break

        # generate next generation
        children = crossover(population, pop_size)
        newPopulation = mutate(children, mut_rate, tourSize)

        probabilities = calculateFitness(newPopulation)

        # locally improve the top elites using 2-opt to speed up convergence
        try:
            # derive elite size similar to crossover (5% of population, min 1)
            hp = get_hyperparams(tourSize)
            elite_size = max(1, int(0.05 * hp.population))
        except Exception:
            elite_size = 1
        # apply 2-opt to elites
        from mutation import apply_two_opt_to_elites
        newPopulation = apply_two_opt_to_elites(newPopulation,
                                                probabilities,
                                                elite_size=elite_size,
                                                max_iterations=20)

        # choose best individual by fitness (higher fitness -> shorter distance)
        max_f = max(probabilities)
        idx = probabilities.index(max_f)
        gen_cost = calculateTotalDistance(newPopulation[idx])
        if gen_cost < best_cost:
            best_cost = gen_cost
            best_tour = newPopulation[idx]
            count = 0
        else:
            count += 1

        population = newPopulation

    if best_tour:
        best_tour.append(best_tour[0])
        # write results to output file
        try:
            writeOutput(best_cost, best_tour, "output.txt")
        except Exception as e:
            pass


if __name__ == "__main__":
    main()
