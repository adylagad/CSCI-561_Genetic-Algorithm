"""Crossover operators for the Genetic Algorithm."""
from ..core.interfaces import CrossoverOperator
from ..core.types import Tour, Population, FloatList, City
from ..operators.selection import RouletteWheelSelection
from random import sample
from typing import List, Dict, Optional


class OrderCrossover(CrossoverOperator):
    """Order crossover (OX) operator."""
    
    def __init__(self, selection_operator: Optional[RouletteWheelSelection] = None):
        """Initialize with a selection operator."""
        self.selection_operator = selection_operator or RouletteWheelSelection()
    
    def cross(self, parent1: Tour, parent2: Tour) -> Tour:
        """
        Perform order crossover between two parent tours.
        Returns a single child tour.
        """
        tour_size = len(parent1)
        child: Tour = [(-1, -1, -1)] * tour_size
        positions: List[int] = sample(range(tour_size), 2)
        start_position = min(positions)
        end_position = max(positions)
        
        # Copy segment from parent1
        child[start_position:end_position] = parent1[start_position:end_position]
        
        # Fill remaining positions from parent2
        i: int = 0
        for j in range(len(child)):
            if child[j][0] == -1:
                while parent2[i] in child:
                    i += 1
                child[j] = parent2[i]
        
        return child
    
    def apply(self, population: Population, population_size: int, 
              probabilities: FloatList) -> Population:
        """Apply crossover to create a new population."""
        result: Population = []
        for _ in range(population_size):
            parent1, parent2 = self.selection_operator.select(probabilities, population)
            result.append(self.cross(parent1, parent2))
        return result


class PMXCrossover(CrossoverOperator):
    """Partially Mapped Crossover (PMX) operator."""
    
    def __init__(self, selection_operator: Optional[RouletteWheelSelection] = None):
        """Initialize with a selection operator."""
        self.selection_operator = selection_operator or RouletteWheelSelection()
    
    def cross(self, parent1: Tour, parent2: Tour) -> Tour:
        """
        Perform PMX crossover between two parent tours.
        Returns a single child tour.
        """
        tour_size = len(parent1)
        child: Tour = [(-1, -1, -1)] * tour_size
        positions: List[int] = sample(range(tour_size), 2)
        start_position = min(positions)
        end_position = max(positions)
        
        # Copy segment from parent1
        child[start_position:end_position] = parent1[start_position:end_position]
        
        # Create mapping
        mapping: Dict[City, City] = {}
        for i in range(start_position, end_position):
            if parent2[i] not in child:
                mapping[parent2[i]] = parent1[i]
        
        # Apply mapping
        for key in mapping:
            index = parent2.index(key)
            while child[index][0] != -1:
                new_index = parent2.index(parent1[index])
                index = new_index
            child[index] = key
        
        # Fill remaining positions
        i: int = 0
        for j in range(len(child)):
            if child[j][0] == -1:
                while parent2[i] in child:
                    i += 1
                child[j] = parent2[i]
        
        return child
    
    def apply(self, population: Population, population_size: int, 
              probabilities: FloatList) -> Population:
        """Apply crossover to create a new population."""
        result: Population = []
        for _ in range(population_size):
            parent1, parent2 = self.selection_operator.select(probabilities, population)
            result.append(self.cross(parent1, parent2))
        return result
