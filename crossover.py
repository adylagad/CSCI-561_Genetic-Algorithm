from GATypes import Tour, Population, FloatList
from random import sample
from typing import List
from fitness_evaluation import calculateFitness
from selection import selectionRouletteWheel


# order crossover -> returns single child tour given 2 parent tours
def orderCrossover(parent1: Tour, parent2: Tour, tourSize: int = 5) -> Tour:
    child: Tour = [(-1, -1, -1)] * len(parent1)
    positions: List[int] = sample(range(tourSize), 2)
    startPosition = min(positions)
    endPosition = max(positions)
    child[startPosition:endPosition] = parent1[startPosition:endPosition]
    i: int = 0
    # improve the for loop below with some pythonista stuff
    for j in range(len(child)):
        if child[j][0] == -1:
            while parent2[i] in child:
                i += 1
            child[j] = parent2[i]
    return child


# partially mapped crossover
def pmxCrossover(parent1: Tour, parent2: Tour, tourSize: int = 5) -> Tour:
    child: Tour = [(-1, -1, -1)] * len(parent1)
    positions: List[int] = sample(range(tourSize), 2)
    startPosition = min(positions)
    endPosition = max(positions)
    child[startPosition:endPosition] = parent1[startPosition:endPosition]
    mapping = {
        parent2[i]: parent1[i]
        for i in range(startPosition, endPosition)
    }
    for key in mapping:
        index = parent2.index(key)
        while child[index][0] != -1:
            newIndex = parent2.index(parent1[index])
            index = newIndex
        child[index] = key
    i: int = 0
    for j in range(len(child)):
        if child[j][0] == -1:
            while parent2[i] in child:
                i += 1
            child[j] = parent2[i]
    return child


# create new population while randomly selecting parents based on roulette wheel and randomly selecting the tour from order corssover
def crossover(population: Population, populationSize: int = 5) -> Population:
    result: Population = []
    probabilities: FloatList = calculateFitness(population)
    for _ in range(populationSize):
        parent1, parent2 = selectionRouletteWheel(probabilities, population)
        result.append(orderCrossover(parent1, parent2, len(parent1)))
    return result


# implement other crossovers if time permits
