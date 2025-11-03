"""Main Genetic Algorithm implementation."""
import logging
from typing import Optional, Tuple
from ..core.types import Tour, Population, FloatList, Statistics
from ..core.interfaces import (
    CrossoverOperator, MutationOperator, 
    FitnessEvaluator, PopulationInitializer
)
from ..evaluation.fitness import calculate_total_distance
from config.config import GAConfig


class GeneticAlgorithm:
    """
    Genetic Algorithm for solving the Traveling Salesman Problem.
    
    This class encapsulates the entire GA workflow and allows for
    pluggable operators (crossover, mutation, selection, fitness).
    """
    
    def __init__(
        self,
        config: GAConfig,
        crossover_operator: CrossoverOperator,
        mutation_operator: MutationOperator,
        fitness_evaluator: FitnessEvaluator,
        population_initializer: PopulationInitializer,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the Genetic Algorithm.
        
        Args:
            config: Configuration object
            crossover_operator: Strategy for crossover
            mutation_operator: Strategy for mutation
            fitness_evaluator: Strategy for fitness evaluation
            population_initializer: Strategy for population initialization
            logger: Optional logger for tracking progress
        """
        self.config = config
        self.crossover = crossover_operator
        self.mutation = mutation_operator
        self.fitness = fitness_evaluator
        self.initializer = population_initializer
        self.logger = logger or self._setup_logger()
        
        # Tracking best solution
        self.best_probability = float('infinity')
        self.best_tour: Tour = []
        self.best_cost = float('infinity')
        self.generation_count = 0
        self.stagnation_count = 0
        self.convergence_generation = 0
        
        # Track population statistics
        self.worst_cost = float('infinity')
        self.average_cost = 0.0
    
    def _setup_logger(self) -> logging.Logger:
        """Set up default logger."""
        logger = logging.getLogger('GeneticAlgorithm')
        logger.setLevel(getattr(logging, self.config.log_level))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def run(self, cities: Tour, tour_size: int) -> Tuple[Tour, float, float]:
        """
        Run the genetic algorithm.
        
        Args:
            cities: List of cities to visit
            tour_size: Number of cities
            
        Returns:
            Tuple of (best_tour, best_cost, best_probability)
        """
        population_size = self.config.population_size(tour_size)
        
        # Initialize population
        population = self.initializer.initialize(cities, population_size)
        probabilities = self.fitness.evaluate(population)
        
        initial_min = min(probabilities)
        self.logger.info(f"Initial Population Best Fitness: {initial_min}")
        
        # Evolution loop
        for generation in range(self.config.number_of_generations):
            self.generation_count = generation
            
            # Check convergence
            if self.stagnation_count > self.config.convergence_threshold:
                self.logger.info(
                    f"Converged at generation {generation} "
                    f"(no improvement for {self.config.convergence_threshold} generations)"
                )
                break
            
            # Create new generation
            new_population = self._evolve(population, population_size, tour_size)
            probabilities = self.fitness.evaluate(new_population)
            
            # Update best solution
            local_minimum = min(probabilities)
            if local_minimum < self.best_probability:
                self._update_best_solution(new_population, probabilities, local_minimum)
                self.stagnation_count = 0
                self.convergence_generation = generation  # Track when best was found
            else:
                self.stagnation_count += 1
            
            # Logging
            if self.config.verbose and generation % self.config.log_interval == 0:
                self.logger.info(
                    f"Generation {generation}: "
                    f"Best Fitness = {self.best_probability:.6f}, "
                    f"Best Cost = {self.best_cost:.2f}, "
                    f"Stagnation = {self.stagnation_count}"
                )
            
            population = new_population
        
        # Final logging
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"Algorithm Complete!")
        self.logger.info(f"Total Generations: {self.generation_count + 1}")
        self.logger.info(f"Optimal Fitness: {self.best_probability:.6f}")
        self.logger.info(f"Optimal Cost: {self.best_cost:.2f}")
        self.logger.info(f"{'='*60}\n")
        
        # Complete the tour by returning to start
        complete_tour = self.best_tour + [self.best_tour[0]]
        
        return complete_tour, self.best_cost, self.best_probability
    
    def _evolve(self, population: Population, population_size: int, tour_size: int) -> Population:
        """Perform one evolution step (crossover + mutation)."""
        # Get fitness for selection
        probabilities = self.fitness.evaluate(population)
        
        # Crossover
        offspring = self.crossover.apply(population, population_size, probabilities)
        
        # Mutation
        mutated_population = self.mutation.mutate(offspring)
        
        return mutated_population
    
    def _update_best_solution(
        self, 
        population: Population, 
        probabilities: FloatList, 
        best_prob: float
    ) -> None:
        """Update the best solution found so far."""
        distances: FloatList = [
            calculate_total_distance(tour) for tour in population
        ]
        
        self.best_probability = best_prob
        index = probabilities.index(self.best_probability)
        self.best_cost = distances[index]
        self.best_tour = population[index]
        
        # Update population statistics
        self.worst_cost = max(distances)
        self.average_cost = sum(distances) / len(distances)
    
    def get_statistics(self) -> Statistics:
        """Get algorithm statistics."""
        return {
            'total_generations': self.generation_count + 1,
            'convergence_generation': self.convergence_generation,
            'best_cost': self.best_cost,
            'average_cost': self.average_cost,
            'worst_cost': self.worst_cost,
            'best_probability': self.best_probability,
            'stagnation_count': self.stagnation_count,
            'converged': self.stagnation_count > self.config.convergence_threshold
        }
