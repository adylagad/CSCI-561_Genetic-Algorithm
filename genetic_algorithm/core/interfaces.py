"""Abstract base classes for genetic algorithm operators."""
from abc import ABC, abstractmethod
from .types import Tour, Population, FloatList, Parents


class CrossoverOperator(ABC):
    """Abstract base class for crossover operators."""
    
    @abstractmethod
    def cross(self, parent1: Tour, parent2: Tour) -> Tour:
        """Perform crossover between two parent tours."""
        pass
    
    @abstractmethod
    def apply(self, population: Population, population_size: int, 
              probabilities: FloatList) -> Population:
        """Apply crossover to create a new population."""
        pass


class MutationOperator(ABC):
    """Abstract base class for mutation operators."""
    
    @abstractmethod
    def mutate(self, population: Population) -> Population:
        """Apply mutation to a population."""
        pass


class SelectionOperator(ABC):
    """Abstract base class for selection operators."""
    
    @abstractmethod
    def select(self, probabilities: FloatList, population: Population) -> Parents:
        """Select two parents from the population."""
        pass


class FitnessEvaluator(ABC):
    """Abstract base class for fitness evaluation."""
    
    @abstractmethod
    def evaluate(self, population: Population) -> FloatList:
        """Evaluate fitness for each individual in the population."""
        pass


class PopulationInitializer(ABC):
    """Abstract base class for population initialization."""
    
    @abstractmethod
    def initialize(self, cities: Tour, population_size: int) -> Population:
        """Initialize a population."""
        pass
