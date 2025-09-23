from typing import List, Dict, Tuple
from itertools import accumulate
from random import random, sample, choice
from bisect import bisect
from math import sqrt, isfinite
from dataclasses import dataclass

City = Tuple[int, int, int]
Tour = List[Tuple[int, int, int]]
Population = List[List[Tuple[int, int, int]]]
Input = Tuple[int, List[Tuple[int, int, int]]]
FloatList = List[float]
Parents = Tuple[Tour, Tour]
CityIndex = Dict[City, int]
DistanceMatrix = List[List[float]]

# can i remove this?
mutationRate = 0.05
numberOfGenerations = 3500
threshold = 50


@dataclass
class Params:
    population: int
    generations: int
    mutationRate: float
    threshold: int
    nearestFraction: float


def getParams(n: int) -> Params:
    presets: Dict[int, Params] = {
        50:
        Params(population=200,
               generations=500,
               mutationRate=0.08,
               threshold=50,
               nearestFraction=0.7),
        100:
        Params(population=150,
               generations=400,
               mutationRate=0.07,
               threshold=40,
               nearestFraction=0.7),
        200:
        Params(population=100,
               generations=300,
               mutationRate=0.06,
               threshold=30,
               nearestFraction=0.6),
        500:
        Params(population=60,
               generations=200,
               mutationRate=0.05,
               threshold=20,
               nearestFraction=0.5),
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


def readInput(inputPath: str) -> Input:
    with open(inputPath, "r", encoding="utf-8") as f:
        nLine = f.readline()
        numberOfCities = int(nLine.split()[0])
        cities: Tour = []
        for _ in range(numberOfCities):
            a, b, c = map(int, f.readline().split())
            cities.append((a, b, c))
    return (numberOfCities, cities)


def writeOutput(cost: float,
                tour: Tour,
                outputPath: str = "output.txt") -> None:
    with open(outputPath, "w", encoding="utf-8") as f:
        f.write(f"{cost}\n")
        for city in tour:
            f.write(f"{city[0]} {city[1]} {city[2]}\n")


def calculateTotalDistance(tour: Tour) -> float:
    # Use precomputed distanceMatrix when available for speed.
    n = len(tour)
    if n == 0:
        return 0.0
    try:
        idxs = [cityIndex[c] for c in tour]
        total = 0.0
        for i in range(n):
            a = idxs[i]
            b = idxs[(i + 1) % n]
            total += distanceMatrix[a][b]
        return total
    except Exception:
        # Fallback to Euclidean if indexing not available
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
        # Use index-based nearest neighbour to avoid repeated tuple comparisons
        n = len(cities)
        if n == 0:
            result.append([])
            continue
        start_idx = cityIndex.get(choice(cities), None)
        if start_idx is None:
            startCity = choice(cities)
            visitedCities = [startCity]
            remaining = set(cities) - set(visitedCities)
            while remaining:
                last_city = visitedCities[-1]
                nxt = min(remaining,
                          key=lambda c: euclideanDistance(last_city, c))
                visitedCities.append(nxt)
                remaining.remove(nxt)
            result.append(visitedCities)
            continue

        visited_idxs = [start_idx]
        remaining = set(range(n)) - set(visited_idxs)
        while remaining:
            last_idx = visited_idxs[-1]
            # find nearest by scanning distanceMatrix row for last_idx
            nearest = min(remaining, key=lambda r: distanceMatrix[last_idx][r])
            visited_idxs.append(nearest)
            remaining.remove(nearest)
        inv = {v: k for k, v in cityIndex.items()}
        visitedCities = [inv[i] for i in visited_idxs]
        result.append(visitedCities)
    return result


def insertionHeuristicInitialPopulation(cities: Tour,
                                        populationSize: int = 5) -> Population:
    result: Population = []
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
    if n == 0:
        raise ValueError("population must contain at least one tour")

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
                # apply a quick local improvement to child
                result.append(twoOptDelta(c, max_iterations=8))
            else:
                break

    return result


def mutate(population: Population,
           mutationRate: float = 0.05,
           tourSize: int = 0,
           method: str = 'auto') -> Population:
    for tour in population:
        size = tourSize if tourSize != 0 else len(tour)
        if size < 2:
            continue
        if random() <= mutationRate:
            op = method
            if method == 'auto':
                op = 'invert' if size >= 8 else 'swap'

            if op == 'swap':
                i, j = sample(range(size), 2)
                tour[i], tour[j] = tour[j], tour[i]
            elif op == 'invert':
                i, j = sorted(sample(range(size), 2))
                tour[i:j + 1] = reversed(tour[i:j + 1])
            else:
                i, j = sample(range(size), 2)
                tour[i], tour[j] = tour[j], tour[i]

    return population


def twoOptDelta(tour: Tour, max_iterations: int = 50) -> Tour:
    n = len(tour)
    if n < 4:
        return tour
    idxs = tourIndexList(tour)

    # adapt iterations based on problem size to avoid excessive runtimes
    if n >= 500:
        max_it = max(8, max_iterations // 8)
    elif n >= 200:
        max_it = max(12, max_iterations // 4)
    else:
        max_it = max_iterations

    improved = True
    iterations = 0
    while improved and iterations < max_it:
        improved = False
        iterations += 1
        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                a, b = idxs[i - 1], idxs[i]
                c, d = idxs[j], idxs[(j + 1) % n]
                before = distanceMatrix[a][b] + distanceMatrix[c][d]
                after = distanceMatrix[a][c] + distanceMatrix[b][d]
                if after < before:
                    idxs[i:j + 1] = list(reversed(idxs[i:j + 1]))
                    improved = True
                    break
            if improved:
                break
    inv = {v: k for k, v in cityIndex.items()}
    return [inv[i] for i in idxs]


def twoOpt(tour: Tour, maxIterations: int = 50) -> Tour:
    # simple wrapper to keep compatibility; delegate to twoOptDelta
    return twoOptDelta(tour, max_iterations=maxIterations)


def applyTwoOptElites(population: Population,
                      probabilities: FloatList,
                      eliteSize: int = 1,
                      maxIterations: int = 50) -> Population:
    if not population or eliteSize <= 0:
        return population

    indexed = list(enumerate(population))
    indexed.sort(key=lambda iv: probabilities[iv[0]], reverse=True)
    new_pop = [tour.copy() for tour in population]
    for idx, _ in indexed[:eliteSize]:
        improved = twoOptDelta(new_pop[idx], max_iterations=maxIterations)
        new_pop[idx] = improved

    return new_pop


def main() -> None:
    count = 0
    tourSize, listOfCities = readInput("input.txt")
    buildDistanceMatrix(listOfCities)

    params = getParams(tourSize)
    popSize = params.population
    generations = params.generations
    mutRate = params.mutationRate
    run_threshold = params.threshold
    nearestFraction = params.nearestFraction

    population: Population = initialPopulation(listOfCities, popSize,
                                               nearestFraction)

    probabilities = calculateFitness(population)
    bestCost = float('infinity')
    bestTour: Tour = []

    for _ in range(generations):
        if count > run_threshold:
            break

        children = crossover(population, popSize)
        newPopulation = mutate(children, mutRate, tourSize)

        probabilities = calculateFitness(newPopulation)

        try:
            hyperParams = getParams(tourSize)
            eliteSize = max(1, int(0.05 * hyperParams.population))
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
        # Ensure we do not double-count the closing edge when recomputing cost.
        tour_no_dup = bestTour[:-1] if len(
            bestTour) > 1 and bestTour[0] == bestTour[-1] else bestTour

        # Recompute actual cost from the final tour (without duplicate end)
        actual_cost = calculateTotalDistance(tour_no_dup)
        if not isfinite(actual_cost):
            print("Warning: computed non-finite cost for final tour")
        if abs(actual_cost - bestCost) > 1e-6:
            # Report and correct mismatch
            print(
                "Notice: reported bestCost did not match recomputed cost. Using recomputed value."
            )
            bestCost = actual_cost

        # Prepare output tour with explicit return-to-start as required by some judges
        output_tour = tour_no_dup + [tour_no_dup[0]] if tour_no_dup else []
        try:
            writeOutput(bestCost, output_tour, "output.txt")
        except Exception as e:
            print("Failed to write output:", e)


if __name__ == "__main__":
    main()
