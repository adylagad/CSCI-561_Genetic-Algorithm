from GATypes import FloatList, Parents, Population
from itertools import accumulate
from random import random, sample
from bisect import bisect

# step 1: calculate cumulative sum of probabilities
# step 2: generate a random number between 0 and 1
# step 3: select the parent based on the random number and cumulative sum


# probablities is the same as the rank list, that is which tour has the highest change of getting picked
def selectionRouletteWheel(probabilities: FloatList,
                           population: Population) -> Parents:
    n = len(population)
    if n == 0:
        raise ValueError("population must contain at least one tour")

    # defensive: ensure probabilities matches population length
    if len(probabilities) != n:
        # fallback: uniform probabilities
        if n == 1:
            return (population[0], population[0])
        a, b = sample(population, 2)
        return (a, b)

    cumulative: FloatList = list(accumulate(
        max(0.0, p) for p in probabilities))
    total = cumulative[-1] if cumulative else 0.0

    if total <= 0 or not cumulative:
        # degenerate case: choose two random distinct parents
        if n == 1:
            return (population[0], population[0])
        a, b = sample(population, 2)
        return (a, b)

    def pick_one() -> int:
        r = random() * total
        idx = bisect(cumulative, r)
        if idx >= n:
            idx = n - 1
        return idx

    i1 = pick_one()
    i2 = pick_one()
    # try to get distinct parents when possible
    if n > 1 and i1 == i2:
        # attempt a few reselections
        for _ in range(3):
            i2 = pick_one()
            if i2 != i1:
                break
        else:
            # final fallback: pick any other index
            choices = [i for i in range(n) if i != i1]
            if choices:
                i2 = choices[int(random() * len(choices))]

    return (population[i1], population[i2])
