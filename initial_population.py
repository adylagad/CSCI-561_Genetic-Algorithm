from GATypes import Tour, Population, City
from random import sample, choice
from utils import euclideanDistance


# random initialization
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


# to do: implement the following function
def insertionHeuristicInitialPopulation(cities: Tour,
                                        populationSize: int = 5) -> Population:
    result: Population = []
    return result


def initialPopulation(cities: Tour,
                      populationSize: int = 5,
                      nearest_fraction: float = 0.7) -> Population:
    """Create an initial population mixing nearest-neighbor and random tours.

    - `nearest_fraction` controls the fraction (0..1) of the population generated
      using the nearest-neighbor heuristic. The remainder is random tours.
    - Returns a `Population` of length `populationSize`.
    """
    if populationSize <= 0:
        return []

    # clamp fraction to [0,1]
    if nearest_fraction < 0.0:
        nearest_fraction = 0.0
    if nearest_fraction > 1.0:
        nearest_fraction = 1.0

    nearest_count = int(populationSize * nearest_fraction)
    random_count = populationSize - nearest_count

    result: Population = []
    if nearest_count > 0:
        result.extend(nearestHeuristicInitialPopulation(cities, nearest_count))
    if random_count > 0:
        result.extend(randomInitialPopulation(cities, random_count))

    return result
