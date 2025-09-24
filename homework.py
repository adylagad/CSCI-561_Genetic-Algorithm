from typing import List, Dict, Tuple, Optional
from itertools import accumulate
from random import random, sample, choice
from bisect import bisect
from math import sqrt, isfinite
from dataclasses import dataclass

# constants
# used frequently and can be changed from here for all the code
INPUT_FILE = "input.txt"
OUTPUT_FILE = "output.txt"
INFINITY = float('infinity')
AUTO = 'auto'
SWAP = 'swap'
INVERT = 'invert'
ENCODING = 'utf-8'


# parameters for different problem input sizes
@dataclass
class Params:
    population: int  # population size
    generations: int  # number of generations per iteration
    mutationRate: float  # probability of child tour to be mutated
    threshold: int  # threshold for number of tries to get the best solution
    nearestFraction: float  # fraction of initial population to be generated from the nearest heuristic initial population


# types for better clarity and code quality
City = Tuple[int, int, int]
Tour = List[Tuple[int, int, int]]
Population = List[List[Tuple[int, int, int]]]
Input = Tuple[int, List[Tuple[int, int, int]]]
FloatList = List[float]
Parents = Tuple[Tour, Tour]
CityIndex = Dict[City, int]
DistanceMatrix = List[List[float]]
Presets = Dict[int, 'Params']


# based on the input tour size, will return the parameters to optimize the solution
# all the parameters are defined in the Params data class
def getParams(n: int) -> Params:
    presets: Presets = {
        50: Params(200, 500, 0.08, 50, 1),
        100: Params(140, 380, 0.07, 35, 0.7),
        200: Params(90, 250, 0.06, 25, 0.6),
        500: Params(60, 200, 0.05, 20, 0.5),
    }

    if n in presets:
        return presets[n]

    if n <= 50:
        return presets[50]
    if n <= 100:
        return presets[100]
    if n <= 200:
        return presets[200]

    # default case
    return Params(population=max(20, n // 5),
                  generations=max(50, 1000 // (n // 100 + 1)),
                  mutationRate=0.05,
                  threshold=20,
                  nearestFraction=0.5)


# calculate the Euclidean distance between two cities/points
def euclideanDistance(city1: City, city2: City) -> float:
    city1_x, city1_y, city1_z = city1
    city2_x, city2_y, city2_z = city2
    xDistance = city1_x - city2_x
    yDistance = city1_y - city2_y
    zDistance = city1_z - city2_z
    return sqrt(xDistance * xDistance + yDistance * yDistance +
                zDistance * zDistance)


# read input from the input file and return the tour size and cities in the tour
def readInput(inputPath: str = INPUT_FILE) -> Input:
    with open(inputPath, "r", encoding=ENCODING) as f:
        nLine = f.readline()
        numberOfCities = int(nLine.split()[0])
        cities: Tour = []
        for _ in range(numberOfCities):
            a, b, c = map(int, f.readline().split())
            cities.append((a, b, c))
    return (numberOfCities, cities)


# write the output in the output file in the given format
def writeOutput(cost: float,
                tour: Tour,
                outputPath: str = OUTPUT_FILE) -> None:
    with open(outputPath, "w", encoding=ENCODING) as f:
        f.write(f"{cost}\n")
        for city in tour:
            f.write(f"{city[0]} {city[1]} {city[2]}\n")


# city index pair
cityIndex: CityIndex = {}
# record the distances between every pair of cities in the tour
distanceMatrix: DistanceMatrix = []


# calculate the distance between evert pair of cities and store it in a matrix
# also used to calculate the two opt where the weight of the edges is calculated to see if there is an overlap
def buildDistanceMatrix(cities: Tour) -> None:
    global cityIndex, distanceMatrix
    cityIndex = {city: i for i, city in enumerate(cities)}
    n = len(cities)
    distanceMatrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            distance = euclideanDistance(cities[i], cities[j])
            distanceMatrix[i][j] = distance
            distanceMatrix[j][i] = distance


# return a list of indices associated with the cities in the tour
def tourIndexList(tour: Tour) -> List[int]:
    return [cityIndex[c] for c in tour]


def calculateTotalDistance(tour: Tour) -> float:
    n = len(tour)
    if n == 0:
        return 0.0
    # try calculating the distance from the distance matrix
    try:
        indices = [cityIndex[c] for c in tour]
        total = 0.0
        for i in range(n):
            a = indices[i]
            b = indices[(i + 1) % n]
            total += distanceMatrix[a][b]
        return total
    # if calculating distance from the matrix fails, calculate the distance by calculating the distance between every pair of cities
    except Exception:
        totalDistance = 0.0
        for i in range(n):
            city1 = tour[i]
            city2 = tour[(i + 1) % n]
            totalDistance += euclideanDistance(city1, city2)
        return totalDistance


# calculate the fitness of the population
# more the cost of the tour, less the fitness
# also the fitness represesnts the probability of getting picked from the roulette wheel in the selection step
def calculateFitness(population: Population) -> FloatList:
    distances: FloatList = [
        calculateTotalDistance(tour) for tour in population
    ]
    rawFitness: FloatList = []
    for dist in distances:
        rawFitness.append(1.0 / dist)

    totalFitness = sum(rawFitness)
    if totalFitness <= 0 or not isfinite(totalFitness):
        n = len(rawFitness) or 1
        return [1.0 / n] * n

    return [fitness / totalFitness for fitness in rawFitness]


# randomly create the initial population for diversity
def randomInitialPopulation(cities: Tour,
                            populationSize: int = 5) -> Population:
    result: Population = []
    for _ in range(populationSize):
        randomList = sample(cities, len(cities))
        result.append(randomList)
    return result


# calculate the initial population by selecting a random city
# creating the tour by selecting the cities which are closest to the current city in the tour
def nearestHeuristicInitialPopulation(cities: Tour,
                                      populationSize: int = 5) -> Population:
    result: Population = []
    for _ in range(populationSize):
        n = len(cities)
        if n == 0:
            result.append([])
            continue
        startIndex = cityIndex.get(choice(cities), None)
        if startIndex is None:
            startCity = choice(cities)
            visitedCities = [startCity]
            remaining = set(cities) - set(visitedCities)
            while remaining:
                lastCity = visitedCities[-1]
                next = min(remaining,
                           key=lambda c: euclideanDistance(lastCity, c))
                visitedCities.append(next)
                remaining.remove(next)
            result.append(visitedCities)
            continue

        visitedIndices = [startIndex]
        remaining = set(range(n)) - set(visitedIndices)
        while remaining:
            lastIndex = visitedIndices[-1]
            nearest = min(remaining,
                          key=lambda r: distanceMatrix[lastIndex][r])
            visitedIndices.append(nearest)
            remaining.remove(nearest)
        inv = {index: city for city, index in cityIndex.items()}
        visitedCities = [inv[i] for i in visitedIndices]
        result.append(visitedCities)
    return result


# hybrid initial population
# combines random and nearest heuristic methods to create the initial population
def initialPopulation(cities: Tour,
                      populationSize: int = 5,
                      nearestFraction: float = 0.7) -> Population:
    if populationSize <= 0:
        return []

    nearestCount = int(populationSize * nearestFraction)
    randomCount = populationSize - nearestCount

    result: Population = []
    if nearestCount > 0:
        result.extend(nearestHeuristicInitialPopulation(cities, nearestCount))
    if randomCount > 0:
        result.extend(randomInitialPopulation(cities, randomCount))

    return result


# select the parents based on the fitness
# treats the fitness like probability of the parent tour getting picked
def selectionRouletteWheel(probabilities: FloatList,
                           population: Population) -> Parents:
    n = len(population)

    if len(probabilities) != n:
        if n == 1:
            return (population[0], population[0])
        a, b = sample(population, 2)
        return (a, b)

    cumulative: FloatList = list(accumulate(
        max(0.0, p) for p in probabilities))
    total = cumulative[-1] if cumulative else 0.0

    if total <= 0 or not cumulative:
        if n == 1:
            return (population[0], population[0])
        a, b = sample(population, 2)
        return (a, b)

    # pick a city in the tour based on the probability
    # heart of the roulette wheel selection
    def pickOne() -> int:
        r = random() * total
        index = bisect(cumulative, r)
        if index >= n:
            index = n - 1
        return index

    i1 = pickOne()
    i2 = pickOne()
    if n > 1 and i1 == i2:
        for _ in range(3):
            i2 = pickOne()
            if i2 != i1:
                break
        else:
            choices = [i for i in range(n) if i != i1]
            if choices:
                i2 = choices[int(random() * len(choices))]

    return (population[i1], population[i2])


# implementation of order crossover
# randomly picks sub array from parent 1 and fill the city in child tour in order as they appear in parent 2
def orderCrossover(parent1: Tour, parent2: Tour, tourSize: int = 5) -> Tour:
    child: Tour = [(-1, -1, -1)] * len(parent1)
    positions: List[int] = sample(range(tourSize), 2)
    startPosition = min(positions)
    endPosition = max(positions)
    child[startPosition:endPosition] = parent1[startPosition:endPosition]
    i: int = 0
    for j in range(len(child)):
        if child[j][0] == -1:
            while parent2[i] in child:
                i += 1
            child[j] = parent2[i]
    return child


# implementation of partially mapped crossover
# randomly picks sub array from parent 1
# create a mapping of cities from parent 2 to parent 1 in the same range as the sub array
# fill the cities in the child tour based on the mapping
# fill the remaining positions in the child tour in order as they appear in the parent 2
def pmxCrossover(parent1: Tour, parent2: Tour, tourSize: int = 5) -> Tour:
    child: Tour = [(-1, -1, -1)] * len(parent1)
    positions: List[int] = sample(range(tourSize), 2)
    startPosition = min(positions)
    endPosition = max(positions)
    child[startPosition:endPosition] = parent1[startPosition:endPosition]
    mapping: Dict[City, City] = {}
    for i in range(startPosition, endPosition):
        if parent2[i] not in child:
            mapping[parent2[i]] = parent1[i]

    for key in mapping:
        index = parent2.index(key)
        while child[index][0] != -1:
            newIndex = parent2.index(parent1[index])
            index = newIndex
        child[index] = key
    i: int = 0
    for j in range(len(child)):
        if child[j][0] == -1:
            while parent2[i] in child:
                i += 1
            child[j] = parent2[i]
    return child


# hybrid implementation of order crossover and pmx crossover
def makeChildren(p1: Tour, p2: Tour) -> List[Tour]:
    size = len(p1)
    child1 = orderCrossover(p1, p2, size)
    child2 = pmxCrossover(p1, p2, size)
    return [child1, child2]


# crossover implementation to produce new population
def crossover(population: Population,
              populationSize: int = 5,
              probabilities: Optional[FloatList] = None) -> Population:

    parameters = getParams(len(population[0]))
    eliteSize = max(1, int(0.05 * parameters.population))

    if probabilities is None:
        probabilities = calculateFitness(population)

    indexed = list(enumerate(population))
    indexed.sort(key=lambda iv: probabilities[iv[0]], reverse=True)
    elites = [tour for (_, tour) in indexed[:eliteSize]]

    result: Population = []
    for e in elites:
        result.append(e)

    tourSize = len(population[0]) if population else 0
    childTwoOptBudget = 6 if tourSize <= 50 else 8

    while len(result) < populationSize:
        parent1, parent2 = selectionRouletteWheel(probabilities, population)
        children = makeChildren(parent1, parent2)
        for c in children:
            if len(result) < populationSize:
                result.append(twoOptDelta(c, maxIterations=childTwoOptBudget))
            else:
                break

    return result


# implement mutation at the given mutation rate
# hybrid implementation, combines swap and insertion mutation based on the tour size
def mutate(population: Population,
           mutationRate: float = 0.05,
           tourSize: int = 0,
           method: str = AUTO) -> Population:
    for tour in population:
        size = tourSize if tourSize != 0 else len(tour)
        if size < 2:
            continue
        if random() <= mutationRate:
            op = method
            if method == AUTO:
                op = INVERT if size >= 8 else SWAP

            if op == SWAP:
                i, j = sample(range(size), 2)
                tour[i], tour[j] = tour[j], tour[i]
            elif op == INVERT:
                i, j = sorted(sample(range(size), 2))
                tour[i:j + 1] = reversed(tour[i:j + 1])
            else:
                i, j = sample(range(size), 2)
                tour[i], tour[j] = tour[j], tour[i]

    return population


def twoOptDelta(tour: Tour, maxIterations: int = 50) -> Tour:
    n = len(tour)
    if n < 4:
        return tour
    indices = tourIndexList(tour)

    if n >= 500:
        maxIt = max(8, maxIterations // 8)
    elif n >= 200:
        maxIt = max(12, maxIterations // 4)
    else:
        maxIt = maxIterations

    improved = True
    iterations = 0
    while improved and iterations < maxIt:
        improved = False
        iterations += 1
        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                a, b = indices[i - 1], indices[i]
                c, d = indices[j], indices[(j + 1) % n]
                before = distanceMatrix[a][b] + distanceMatrix[c][d]
                after = distanceMatrix[a][c] + distanceMatrix[b][d]
                if after < before:
                    indices[i:j + 1] = list(reversed(indices[i:j + 1]))
                    improved = True
                    break
            if improved:
                break
    inv = {index: city for city, index in cityIndex.items()}
    return [inv[i] for i in indices]


# elitism: keep the tours with good fitness in the new population to get optimal results
def applyTwoOptElites(population: Population,
                      probabilities: FloatList,
                      eliteSize: int = 1,
                      maxIterations: int = 50) -> Population:
    if not population or eliteSize <= 0:
        return population

    indexed = list(enumerate(population))
    indexed.sort(key=lambda iv: probabilities[iv[0]], reverse=True)
    newPop = [tour.copy() for tour in population]
    for idx, _ in indexed[:eliteSize]:
        improved = twoOptDelta(newPop[idx], maxIterations)
        newPop[idx] = improved

    return newPop


def main() -> None:
    # to keep track of iterations it took to get a better solution
    # if the count exceed the threshold, terminate the program
    count = 0
    tourSize, listOfCities = readInput(INPUT_FILE)
    buildDistanceMatrix(listOfCities)

    params = getParams(tourSize)
    popSize = params.population
    generations = params.generations
    mutRate = params.mutationRate
    runThreshold = params.threshold
    nearestFraction = params.nearestFraction

    population: Population = initialPopulation(listOfCities, popSize,
                                               nearestFraction)

    probabilities = calculateFitness(population)
    bestCost = INFINITY
    bestTour: Tour = []

    for generation in range(generations):
        # stop the code count exceeds the threshold
        if count > runThreshold:
            break

        probabilities = calculateFitness(population)

        children = crossover(population, popSize, probabilities)
        newPopulation = mutate(children, mutRate, tourSize)

        parameters = getParams(tourSize)
        eliteSize = max(1, int(0.05 * parameters.population))

        if tourSize <= 50:
            if generation % 5 == 0:
                newPopulation = applyTwoOptElites(newPopulation,
                                                  probabilities,
                                                  eliteSize=eliteSize,
                                                  maxIterations=10)
        else:
            newPopulation = applyTwoOptElites(newPopulation,
                                              probabilities,
                                              eliteSize=eliteSize,
                                              maxIterations=20)

        maxFitness = max(probabilities)
        idx = probabilities.index(maxFitness)
        genCost = calculateTotalDistance(newPopulation[idx])
        if genCost < bestCost:
            bestCost = genCost
            bestTour = newPopulation[idx]
            count = 0
        else:
            count += 1

        population = newPopulation

    if bestTour:
        # remove the duplicate city if present at the end of the tour, which is also the first city
        noDuplicatesTour = bestTour[:-1] if len(
            bestTour) > 1 and bestTour[0] == bestTour[-1] else bestTour

        actualCost = calculateTotalDistance(noDuplicatesTour)

        if actualCost > bestCost:
            bestCost = actualCost

        # append the first city at the n+1 position to complete the tour
        outputTour = noDuplicatesTour + [noDuplicatesTour[0]
                                         ] if noDuplicatesTour else []
        writeOutput(bestCost, outputTour, OUTPUT_FILE)


if __name__ == "__main__":
    main()
