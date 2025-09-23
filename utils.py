from math import sqrt
from typing import cast
from GATypes import City, Input, Tour
from typing import List


# to do:
# create a function which selects the size of the intial population based on the number of cities
# what is a good population size?
def populationSize(tourSize: int) -> int:
    return tourSize


# Euclidean distance between two cities
def euclideanDistance(city1: City, city2: City) -> float:
    city1_x, city1_y, city1_z = city1

    city2_x, city2_y, city2_z = city2

    xDistance = city1_x - city2_x
    yDistance = city1_y - city2_y
    zDistance = city1_z - city2_z

    return sqrt(xDistance * xDistance + yDistance * yDistance +
                zDistance * zDistance)


# read input from file
def readInput(inputPath: str) -> Input:
    lines: List[str] = []
    with open(inputPath, "r", encoding="utf-8") as f:
        for raw in f:
            s = raw.strip()
            if not s:
                continue
            lines.append(s)

    if not lines:
        raise ValueError(f"Empty input file: {inputPath}")

    try:
        numberOfCities = int(lines[0].split()[0])
    except Exception as e:
        raise ValueError(f"First line must contain number of cities: {e}")

    cities: Tour = []
    for line in lines[1:1 + numberOfCities]:
        parts = line.split()
        if len(parts) < 3:
            raise ValueError(f"Invalid city line (expected 3 ints): '{line}'")
        city = cast(City, tuple(map(int, parts[:3])))
        cities.append(city)

    return (numberOfCities, cities)


def writeOutput(cost: float,
                tour: Tour,
                outputPath: str = "output.txt") -> None:
    with open(outputPath, "w", encoding="utf-8") as f:
        f.write(f"{cost}\n")
        for city in tour:
            # write coordinates without brackets, space-separated
            f.write(f"{city[0]} {city[1]} {city[2]}\n")
