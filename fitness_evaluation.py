from GATypes import Tour, FloatList, Population
from utils import euclideanDistance
from math import isfinite


# total distance of the route
def calculateTotalDistance(tour: Tour) -> float:
    totalDistance = 0.0
    for i in range(len(tour)):
        city1 = tour[i]
        city2 = tour[(i + 1) % len(tour)]
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
