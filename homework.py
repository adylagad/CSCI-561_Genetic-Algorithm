from typing import Tuple, List, cast
from itertools import accumulate
from random import random, sample, choice
from bisect import bisect
from math import sqrt
from dataclasses import dataclass

City = Tuple[int, int, int]
Tour = List[Tuple[int, int, int]]
Population = List[List[Tuple[int, int, int]]]
Input = Tuple[int, List[Tuple[int, int, int]]]
FloatList = List[float]
Parents = Tuple[Tour, Tour]


@dataclass
class HyperParams:
    population: int
    generations: int
    mutation_rate: float
    threshold: int
    nearest_fraction: float


# a good mutation rate would be 5% (atleast as of now)
mutationRate = 0.05
# a good number of generations would be 5000 (atleasta as of now)
numberOfGenerations = 3000
# a good threshold would be 50 (atleast as of now)
threshold = 50


# to do:
# create a function which selects the size of the intial population based on the number of cities
# what is a good population size?
def populationSize(tourSize: int) -> int:
    if tourSize == 50:
        return 200
    if tourSize > 300:
        return 260
    return tourSize


# Euclidean distance between two cities
def euclideanDistance(city1: City, city2: City) -> float:
    city1_x, city1_y, city1_z = city1

    city2_x, city2_y, city2_z = city2

    xDistance = city1_x - city2_x
    yDistance = city1_y - city2_y
    zDistance = city1_z - city2_z

    return sqrt(xDistance * xDistance + yDistance * yDistance +
                zDistance * zDistance)


# read input from file
def readInput(inputPath: str) -> Input:
    inputArray: Tour = []
    with open(inputPath, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            city = cast(City, tuple(map(int, parts)))
            inputArray.append(city)
    numberOfCities: int = inputArray[0][0]
    cities: Tour = inputArray[1:]

    return (numberOfCities, cities)


# write output to file
def writeOutput(cost: float, tour: Tour) -> None:
    with open("output.txt", "w") as file:
        file.write(str(cost) + "\n")
        for city in tour:
            file.write(" ".join(map(str, city)) + "\n")


# random initialization (used by initialPopulation)
def randomInitialPopulation(cities: Tour,
                            populationSize: int = 5) -> Population:
    result: Population = []
    for _ in range(populationSize):
        randomList = sample(cities, len(cities))
        result.append(randomList)
    return result


# calculate initial population using nearest neighbor heuristics
def nearestHeuristicInitialPopulation(cities: Tour,
                                      populationSize: int = 5) -> Population:
    result: Population = []
    for _ in range(populationSize):
        visitedCities: Tour = []
        startCity: City = choice(cities)
        visitedCities.append(startCity)
        for _ in range(len(cities) - 1):
            closestCity: City = startCity
            distance: float = float('infinity')
            for city in cities:
                if city not in visitedCities:
                    distanceBetweenTwoCities: float = euclideanDistance(
                        startCity, city)
                    if distanceBetweenTwoCities < distance:
                        distance = distanceBetweenTwoCities
                        closestCity = city
            visitedCities.append(closestCity)
        result.append(visitedCities)
    return result


def initialPopulation(cities: Tour, populationSize: int = 5) -> Population:
    # Uses 70% nearest-neighbor and 30% random by default
    return initialPopulation_mix(cities, populationSize, 0.7)


def initialPopulation_mix(cities: Tour,
                          populationSize: int = 5,
                          nearest_fraction: float = 0.7) -> Population:
    result: Population = []
    nearestNeighborSize = int(populationSize * nearest_fraction)
    randomSize = populationSize - nearestNeighborSize
    if nearestNeighborSize > 0:
        result.extend(
            nearestHeuristicInitialPopulation(cities, nearestNeighborSize))
    if randomSize > 0:
        result.extend(randomInitialPopulation(cities, randomSize))
    return result


def get_hyperparams(n: int) -> HyperParams:
    if n == 50:
        return HyperParams(200, 500, 0.08, 50, 0.7)
    if n == 100:
        return HyperParams(150, 400, 0.07, 40, 0.7)
    if n == 200:
        return HyperParams(100, 300, 0.06, 30, 0.6)
    if n == 500:
        return HyperParams(60, 200, 0.05, 20, 0.5)
    # fallback
    return HyperParams(populationSize(n), numberOfGenerations, mutationRate,
                       threshold, 0.7)


# step 1: calculate cumulative sum of probabilities
# step 2: generate a random number between 0 and 1
# step 3: select the parent based on the random number and cumulative sum


# total distance of the route
def calculateTotalDistance(tour: Tour) -> float:
    total_distance = 0.0
    for i in range(len(tour)):
        city1 = tour[i]
        city2 = tour[(i + 1) % len(tour)]
        total_distance += euclideanDistance(city1, city2)

    return total_distance


# percentage of score associated with total distance of the route
# to do: improve the calculate fitness function
def calculateFitness(population: Population) -> FloatList:
    distances: FloatList = [
        calculateTotalDistance(tour) for tour in population
    ]
    # lower distances are better, so use inverse distance as fitness
    fitness: FloatList = []
    for d in distances:
        if d == 0:
            fitness.append(float('inf'))
        else:
            fitness.append(1.0 / d)
    total_fitness = sum(fitness)
    if total_fitness == 0 or total_fitness == float('inf'):
        # avoid division by zero / infinite values
        return [1.0 / len(fitness)] * len(fitness)
    return [f / total_fitness for f in fitness]


# probablities is the same as the rank list, that is which tour has the highest change of getting picked
def selectionRouletteWheel(probabilities: FloatList,
                           population: Population) -> Parents:
    parent: Population = []
    cumulativeSum: FloatList = list(accumulate(probabilities))
    for _ in range(2):
        randomNumber: float = random() * cumulativeSum[-1]
        index: int = bisect(cumulativeSum, randomNumber)
        index = min(index, len(population) - 1)
        parent.append(population[index])
    return (
        parent[0],
        parent[1],
    )


# order crossover -> returns single child tour given 2 parent tours
def orderCrossover(parent1: Tour, parent2: Tour, tourSize: int = 5) -> Tour:
    child: Tour = [(-1, -1, -1)] * len(parent1)
    positions: List[int] = sample(range(tourSize), 2)
    startPosition = min(positions)
    endPosition = max(positions)
    child[startPosition:endPosition] = parent1[startPosition:endPosition]
    i: int = 0
    # improve the for loop below with some pythonista stuff
    for j in range(len(child)):
        if child[j][0] == -1:
            while parent2[i] in child:
                i += 1
            child[j] = parent2[i]
    return child


# create new population while randomly selecting parents based on roulette wheel and randomly selecting the tour from order corssover
def crossover(population: Population, populationSize: int = 5) -> Population:
    result: Population = []
    probabilities: FloatList = calculateFitness(population)
    # keep top 10% as elites
    eliteSize = max(1, populationSize // 2)
    # sort by fitness descending
    paired = sorted(zip(probabilities, population),
                    key=lambda x: x[0],
                    reverse=True)
    elites = [tour for _, tour in paired[:eliteSize]]
    result.extend(elites)
    # produce remaining children
    while len(result) < populationSize:
        parent1, parent2 = selectionRouletteWheel(probabilities, population)
        child = orderCrossover(parent1, parent2, len(parent1))
        result.append(child)
    return result


# implement other crossovers if time permits


# swaps the mutation cities in place
def mutate(population: Population,
           mutationRate: float = 0.05,
           tourSize: int = 5) -> Population:
    for tour in population:
        rate = random()
        if (rate <= mutationRate):
            index1, index2 = sample(range(tourSize), 2)
            tour[index1], tour[index2] = tour[index2], tour[index1]
    return population


def main() -> None:
    # optimalProbability = float('infinity')
    optimalTour: Tour = []
    optimalCost = float('infinity')
    # keeps track of the number of generations that dont produce a good outcome
    count = 0
    tourSize, listOfCities = readInput("input.txt")
    params = get_hyperparams(tourSize)
    popSize = params.population
    generations = params.generations
    mut_rate = params.mutation_rate
    run_threshold = params.threshold
    nearest_fraction = params.nearest_fraction

    initialPopulationRandom = initialPopulation_mix(listOfCities, popSize,
                                                    nearest_fraction)
    probabilities = calculateFitness(initialPopulationRandom)
    best_cost = float('infinity')
    best_tour: Tour = []
    for _ in range(generations):
        if count > run_threshold:
            break
        children = crossover(initialPopulationRandom, popSize)
        newPopulation = mutate(children, mut_rate, tourSize)
        probabilities = calculateFitness(newPopulation)

        # find best in this generation (highest fitness -> shortest distance)
        fitness_values = probabilities
        max_fitness = max(fitness_values)
        idx = fitness_values.index(max_fitness)
        gen_cost = calculateTotalDistance(newPopulation[idx])
        if gen_cost < best_cost:
            best_cost = gen_cost
            best_tour = newPopulation[idx]
            count = 0
        else:
            count += 1

        # prepare for next generation
        initialPopulationRandom = newPopulation
    # print("Optimal Probability: ", optimalProbability)
    # print("Optimal Cost: ", optimalCost)
    if best_tour:
        best_tour.append(best_tour[0])
        writeOutput(best_cost, best_tour)
    else:
        writeOutput(optimalCost, optimalTour)


if __name__ == "__main__":
    main()
