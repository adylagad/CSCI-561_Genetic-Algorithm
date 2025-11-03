"""Genetic Algorithm package for solving the Traveling Salesman Problem."""
from .core.algorithm import GeneticAlgorithm
from .core.types import City, Tour, Population, Statistics, ConfigDict
from .core.interfaces import (
    CrossoverOperator,
    MutationOperator,
    SelectionOperator,
    FitnessEvaluator,
    PopulationInitializer
)

__version__ = "2.0.0"
__all__ = [
    "GeneticAlgorithm",
    "City",
    "Tour",
    "Population",
    "Statistics",
    "ConfigDict",
    "CrossoverOperator",
    "MutationOperator",
    "SelectionOperator",
    "FitnessEvaluator",
    "PopulationInitializer",
]
