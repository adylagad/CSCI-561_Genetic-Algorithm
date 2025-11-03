"""Population initialization strategies."""
from ..core.interfaces import PopulationInitializer
from ..core.types import Tour, Population, City
from ..utils.helpers import euclidean_distance
from random import sample, choice


class RandomInitializer(PopulationInitializer):
    """Random initialization of population."""
    
    def initialize(self, cities: Tour, population_size: int = 5) -> Population:
        """Create initial population with random permutations."""
        result: Population = []
        for _ in range(population_size):
            random_list = sample(cities, len(cities))
            result.append(random_list)
        return result


class NearestNeighborInitializer(PopulationInitializer):
    """Nearest neighbor heuristic initialization."""
    
    def initialize(self, cities: Tour, population_size: int = 5) -> Population:
        """Create initial population using nearest neighbor heuristic."""
        result: Population = []
        for _ in range(population_size):
            visited_cities: Tour = []
            start_city: City = choice(cities)
            visited_cities.append(start_city)
            
            for _ in range(len(cities) - 1):
                closest_city: City = start_city
                distance: float = float('infinity')
                
                for city in cities:
                    if city not in visited_cities:
                        distance_between_cities: float = euclidean_distance(
                            start_city, city)
                        if distance_between_cities < distance:
                            distance = distance_between_cities
                            closest_city = city
                
                visited_cities.append(closest_city)
                start_city = closest_city
            
            result.append(visited_cities)
        return result


class InsertionHeuristicInitializer(PopulationInitializer):
    """Insertion heuristic initialization (to be implemented)."""
    
    def initialize(self, cities: Tour, population_size: int = 5) -> Population:
        """Create initial population using insertion heuristic."""
        # TODO: Implement insertion heuristic
        result: Population = []
        return result
