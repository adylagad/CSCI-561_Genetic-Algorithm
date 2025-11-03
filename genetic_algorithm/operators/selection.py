"""Selection operators for the Genetic Algorithm."""
from ..core.interfaces import SelectionOperator
from ..core.types import FloatList, Parents, Population
from itertools import accumulate
from random import random
from bisect import bisect


class RouletteWheelSelection(SelectionOperator):
    """Roulette wheel selection operator."""
    
    def select(self, probabilities: FloatList, population: Population) -> Parents:
        """
        Select two parents using roulette wheel selection.
        
        Steps:
        1. Calculate cumulative sum of probabilities
        2. Generate a random number between 0 and 1
        3. Select the parent based on the random number and cumulative sum
        """
        parents: Population = []
        for _ in range(2):
            cumulative_sum: FloatList = list(accumulate(probabilities))
            random_number: float = random()
            index: int = bisect(cumulative_sum, random_number)
            parents.append(population[index])
        
        return (parents[0], parents[1])
