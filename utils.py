from math import sqrt
from typing import cast
from GATypes import City, Input, Tour, Population


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
    inputArray: Tour = []
    with open(inputPath, "r") as file:
        for line in file:
            city = cast(City, tuple(map(int, line.split(" "))))
            inputArray.append(city)
    numberOfCities: int = inputArray[0][0]
    cities: Tour = inputArray[1:]

    return (numberOfCities, cities)


# verify if number of cities is correct
def verifyNumberOfCities(numberOfCities: int, cities: Tour) -> bool:
    return numberOfCities == len(cities)


# print population with each tours on new line
def printPopulation(population: Population) -> None:
    for tour in population:
        print(tour)
