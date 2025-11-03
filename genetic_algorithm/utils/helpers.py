"""Utility functions for distance calculations and I/O operations."""
from math import sqrt
from typing import cast
from ..core.types import City, Input, Tour


def euclidean_distance(city1: City, city2: City) -> float:
    """Calculate Euclidean distance between two cities."""
    city1_x, city1_y, city1_z = city1
    city2_x, city2_y, city2_z = city2

    x_distance = city1_x - city2_x
    y_distance = city1_y - city2_y
    z_distance = city1_z - city2_z

    return sqrt(x_distance * x_distance + y_distance * y_distance + z_distance * z_distance)


def read_input(input_path: str) -> Input:
    """Read input from file."""
    input_array: Tour = []
    with open(input_path, "r") as file:
        for line in file:
            city = cast(City, tuple(map(int, line.split(" "))))
            input_array.append(city)
    
    number_of_cities: int = input_array[0][0]
    cities: Tour = input_array[1:]

    return (number_of_cities, cities)


def verify_number_of_cities(number_of_cities: int, cities: Tour) -> bool:
    """Verify if number of cities is correct."""
    return number_of_cities == len(cities)
