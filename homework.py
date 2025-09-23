from typing import List, Dict, Tuple
from itertools import accumulate
from random import random, sample, choice
from bisect import bisect
from math import sqrt, isfinite
from dataclasses import dataclass

INPUT_FILE = "input.txt"
OUTPUT_FILE = "output.txt"
INFINITY = float('infinity')
AUTO = 'auto'
SWAP = 'swap'
INVERT = 'invert'
ENCODING = 'utf-8'


@dataclass
class Params:
    population: int
    generations: int
    mutationRate: float
    threshold: int
    nearestFraction: float


City = Tuple[int, int, int]
Tour = List[Tuple[int, int, int]]
Population = List[List[Tuple[int, int, int]]]
Input = Tuple[int, List[Tuple[int, int, int]]]
FloatList = List[float]
Parents = Tuple[Tour, Tour]
CityIndex = Dict[City, int]
DistanceMatrix = List[List[float]]
Presets = Dict[int, 'Params']


def getParams(n: int) -> Params:
    presets: Presets = {
        50: Params(200, 500, 0.08, 50, 0.7),
        100: Params(150, 400, 0.07, 40, 0.7),
        200: Params(100, 300, 0.06, 30, 0.6),
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

    return Params(population=max(20, n // 5),
                  generations=max(50, 1000 // (n // 100 + 1)),
                  mutationRate=0.05,
                  threshold=30,
                  nearestFraction=0.5)


def euclideanDistance(city1: City, city2: City) -> float:
    city1_x, city1_y, city1_z = city1
    city2_x, city2_y, city2_z = city2
    xDistance = city1_x - city2_x
    yDistance = city1_y - city2_y
    zDistance = city1_z - city2_z
    return sqrt(xDistance * xDistance + yDistance * yDistance +
                zDistance * zDistance)


def readInput(inputPath: str = INPUT_FILE) -> Input:
    with open(inputPath, "r", encoding=ENCODING) as f:
        nLine = f.readline()
        numberOfCities = int(nLine.split()[0])
        cities: Tour = []
        for _ in range(numberOfCities):
            a, b, c = map(int, f.readline().split())
            cities.append((a, b, c))
    return (numberOfCities, cities)


def writeOutput(cost: float,
                tour: Tour,
                outputPath: str = OUTPUT_FILE) -> None:
    with open(outputPath, "w", encoding=ENCODING) as f:
        f.write(f"{cost}\n")
        for city in tour:
            f.write(f"{city[0]} {city[1]} {city[2]}\n")


cityIndex: CityIndex = {}
distanceMatrix: DistanceMatrix = []


def buildDistanceMatrix(cities: Tour) -> None:
    global cityIndex, distanceMatrix
    cityIndex = {city: i for i, city in enumerate(cities)}
    n = len(cities)
    distanceMatrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = euclideanDistance(cities[i], cities[j])
            distanceMatrix[i][j] = d
            distanceMatrix[j][i] = d


def tourIndexList(tour: Tour) -> List[int]:
    return [cityIndex[c] for c in tour]


def calculateTotalDistance(tour: Tour) -> float:
    n = len(tour)
    if n == 0:
        return 0.0
    try:
        indices = [cityIndex[c] for c in tour]
        total = 0.0
        for i in range(n):
            a = indices[i]
            b = indices[(i + 1) % n]
            total += distanceMatrix[a][b]
        return total
    except Exception:
        totalDistance = 0.0
        for i in range(n):
            city1 = tour[i]
            city2 = tour[(i + 1) % n]
            totalDistance += euclideanDistance(city1, city2)
        return totalDistance


def calculateFitness(population: Population) -> FloatList:
    distances: FloatList = [
        calculateTotalDistance(tour) for tour in population
    ]
    rawFitness: FloatList = []
    for d in distances:
        if d <= 0 or not isfinite(d):
            rawFitness.append(1e12)
        else:
            rawFitness.append(1.0 / d)

    totalFitness = sum(rawFitness)
    if totalFitness <= 0 or not isfinite(totalFitness):
        n = len(rawFitness) or 1
        return [1.0 / n] * n

    return [f / totalFitness for f in rawFitness]


def randomInitialPopulation(cities: Tour,
                            populationSize: int = 5) -> Population:
    result: Population = []
    for _ in range(populationSize):
        randomList = sample(cities, len(cities))
        result.append(randomList)
    return result


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
                nxt = min(remaining,
                          key=lambda c: euclideanDistance(lastCity, c))
                visitedCities.append(nxt)
                remaining.remove(nxt)
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
        inv = {v: k for k, v in cityIndex.items()}
        visitedCities = [inv[i] for i in visitedIndices]
        result.append(visitedCities)
    return result


def initialPopulation(cities: Tour,
                      populationSize: int = 5,
                      nearestFraction: float = 0.7) -> Population:
    if populationSize <= 0:
        return []

    if nearestFraction < 0.0:
        nearestFraction = 0.0
    if nearestFraction > 1.0:
        nearestFraction = 1.0

    nearestCount = int(populationSize * nearestFraction)
    randomCount = populationSize - nearestCount

    result: Population = []
    if nearestCount > 0:
        result.extend(nearestHeuristicInitialPopulation(cities, nearestCount))
    if randomCount > 0:
        result.extend(randomInitialPopulation(cities, randomCount))

    return result


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

    def pickOne() -> int:
        r = random() * total
        idx = bisect(cumulative, r)
        if idx >= n:
            idx = n - 1
        return idx

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


def makeChildren(p1: Tour, p2: Tour) -> List[Tour]:
    size = len(p1)
    child1 = orderCrossover(p1, p2, size)
    child2 = pmxCrossover(p1, p2, size)
    return [child1, child2]


def crossover(population: Population, populationSize: int = 5) -> Population:
    try:
        hp = getParams(len(population[0]))
        eliteSize = max(1, int(0.05 * hp.population))
    except Exception:
        eliteSize = 1

    probabilities: FloatList = calculateFitness(population)

    indexed = list(enumerate(population))
    indexed.sort(key=lambda iv: probabilities[iv[0]], reverse=True)
    elites = [tour for (_, tour) in indexed[:eliteSize]]

    result: Population = []
    for e in elites:
        result.append(e)

    while len(result) < populationSize:
        parent1, parent2 = selectionRouletteWheel(probabilities, population)
        children = makeChildren(parent1, parent2)
        for c in children:
            if len(result) < populationSize:
                result.append(twoOptDelta(c, maxIterations=8))
            else:
                break

    return result


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
    inv = {v: k for k, v in cityIndex.items()}
    return [inv[i] for i in indices]


def twoOpt(tour: Tour, maxIterations: int = 50) -> Tour:
    return twoOptDelta(tour, maxIterations=maxIterations)


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
        improved = twoOptDelta(newPop[idx], maxIterations=maxIterations)
        newPop[idx] = improved

    return newPop


def main() -> None:
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

    for _ in range(generations):
        if count > runThreshold:
            break

        children = crossover(population, popSize)
        newPopulation = mutate(children, mutRate, tourSize)

        probabilities = calculateFitness(newPopulation)

        try:
            parameters = getParams(tourSize)
            eliteSize = max(1, int(0.05 * parameters.population))
        except Exception:
            eliteSize = 1
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
        noDuplicatesTour = bestTour[:-1] if len(
            bestTour) > 1 and bestTour[0] == bestTour[-1] else bestTour

        actualCost = calculateTotalDistance(noDuplicatesTour)

        if not isfinite(actualCost) or abs(actualCost - bestCost) > 1e-6:
            bestCost = actualCost

        outputTour = noDuplicatesTour + [noDuplicatesTour[0]
                                         ] if noDuplicatesTour else []
        writeOutput(bestCost, outputTour, OUTPUT_FILE)


if __name__ == "__main__":
    main()
