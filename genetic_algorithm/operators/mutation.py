"""Mutation operators for the Genetic Algorithm."""
from ..core.interfaces import MutationOperator
from ..core.types import Population
from random import random, sample


class SwapMutation(MutationOperator):
    """Swap mutation operator that exchanges two cities in a tour."""
    
    def __init__(self, mutation_rate: float = 0.05):
        """Initialize with mutation rate."""
        self.mutation_rate = mutation_rate
    
    def mutate(self, population: Population) -> Population:
        """
        Apply swap mutation to population.
        Swaps two random cities in place for each tour based on mutation rate.
        """
        for tour in population:
            rate = random()
            if rate <= self.mutation_rate:
                tour_size = len(tour)
                index1, index2 = sample(range(tour_size), 2)
                tour[index1], tour[index2] = tour[index2], tour[index1]
        return population
