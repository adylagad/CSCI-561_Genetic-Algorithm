from GATypes import Tour, Population, FloatList, City
from random import sample
from typing import List, Dict
from fitness_evaluation import calculateFitness
from selection import selectionRouletteWheel
from constants import get_hyperparams


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
    mapping: Dict[City, City] = {}
    for i in range(startPosition, endPosition):
        if parent2[i] not in child:
            mapping[parent2[i]] = parent1[i]

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
def _make_children(p1: Tour, p2: Tour) -> List[Tour]:
    # produce two children using OX and PMX for diversity
    size = len(p1)
    child1 = orderCrossover(p1, p2, size)
    child2 = pmxCrossover(p1, p2, size)
    return [child1, child2]


def crossover(population: Population, populationSize: int = 5) -> Population:
    """Create a new population.

    - Preserve a small elite set (top tours) as-is.
    - Use roulette selection to pick parents and produce two children per pair
      (OrderX and PMX) to increase genetic diversity.
    The returned population will have exactly `populationSize` members.
    """
    # determine elite size from hyperparams if available, default to 1
    try:
        hp = get_hyperparams(len(population[0]))
        elite_size = max(1, int(0.05 * hp.population))
    except Exception:
        elite_size = 1

    # compute probabilities once
    probabilities: FloatList = calculateFitness(population)

    # select elites (best tours by fitness probability)
    # we map probabilities back to population indices
    indexed = list(enumerate(population))
    indexed.sort(key=lambda iv: probabilities[iv[0]], reverse=True)
    elites = [tour for (_, tour) in indexed[:elite_size]]

    result: Population = []
    # keep elites first
    for e in elites:
        result.append(e)

    # remaining slots
    # produce children in pairs until we fill remaining slots
    while len(result) < populationSize:
        parent1, parent2 = selectionRouletteWheel(probabilities, population)
        children = _make_children(parent1, parent2)
        for c in children:
            if len(result) < populationSize:
                result.append(c)
            else:
                break

    return result


# implement other crossovers if time permits
