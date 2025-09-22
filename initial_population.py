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
