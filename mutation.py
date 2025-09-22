from GATypes import Population
from random import random, sample


# swaps the mutation cities in place
def mutate(population: Population,
           mutationRate: float = 0.05,
           tourSize: int = 5) -> Population:
    for tour in population:
        rate = random()
        if (rate <= mutationRate):
            index1, index2 = sample(range(tourSize), 2)
            tour[index1], tour[index2] = tour[index2], tour[index1]
    return population
