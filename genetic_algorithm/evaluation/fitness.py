"""Fitness evaluation for the Genetic Algorithm."""
from ..core.interfaces import FitnessEvaluator
from ..core.types import Tour, FloatList, Population
from ..utils.helpers import euclidean_distance


def calculate_total_distance(tour: Tour) -> float:
    """Calculate total distance of a route."""
    total_distance = 0.0
    for i in range(len(tour)):
        city1 = tour[i]
        city2 = tour[(i + 1) % len(tour)]
        total_distance += euclidean_distance(city1, city2)
    return total_distance


class DistanceBasedFitness(FitnessEvaluator):
    """Fitness evaluator based on total distance."""
    
    def evaluate(self, population: Population) -> FloatList:
        """
        Calculate fitness as percentage of total distance.
        Lower distance = lower fitness value (better).
        """
        distances: FloatList = [
            calculate_total_distance(tour) for tour in population
        ]
        total_distance = sum(distances)
        if total_distance == 0:
            return [float('inf')] * len(distances)
        return [distance / total_distance for distance in distances]
