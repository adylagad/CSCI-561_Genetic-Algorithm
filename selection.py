from GATypes import FloatList, Parents, Population
from itertools import accumulate
from random import random
from bisect import bisect

# step 1: calculate cumulative sum of probabilities
# step 2: generate a random number between 0 and 1
# step 3: select the parent based on the random number and cumulative sum


# probablities is the same as the rank list, that is which tour has the highest change of getting picked
def selectionRouletteWheel(probabilities: FloatList,
                           population: Population) -> Parents:
    parent: Population = []
    for _ in range(2):
        cululativeSum: FloatList = list(accumulate(probabilities))
        randomNumber: float = random()
        index: int = bisect(cululativeSum, randomNumber)
        # print(cululativeSum)
        # print(randomNumber, index)
        parent.append(population[index])
    return (
        parent[0],
        parent[1],
    )
