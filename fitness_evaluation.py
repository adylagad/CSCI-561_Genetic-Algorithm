from GATypes import Tour, FloatList, Population
from utils import euclideanDistance


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
    total_distance = sum(distances)
    if total_distance == 0:
        return [float('inf')] * len(distances)
    return [distance / total_distance for distance in distances]
