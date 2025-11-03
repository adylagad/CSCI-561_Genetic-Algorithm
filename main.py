"""
Main entry point for the Genetic Algorithm TSP Solver.

This program uses a modular genetic algorithm framework to solve
the Traveling Salesman Problem (TSP) for cities in 3D space.
"""
import logging
from genetic_algorithm.core import GeneticAlgorithm
from genetic_algorithm.operators import OrderCrossover, SwapMutation, RouletteWheelSelection
from genetic_algorithm.evaluation import DistanceBasedFitness
from genetic_algorithm.initialization import RandomInitializer
from genetic_algorithm.utils import read_input
from config.config import GAConfig


def main() -> None:
    """Run the Genetic Algorithm to solve TSP."""
    
    # Load configuration
    config = GAConfig()
    
    # Setup logging
    logging.basicConfig(
        level=getattr(logging, config.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    # Read input
    logger.info(f"Reading input from: {config.input_file}")
    tour_size, cities = read_input(config.input_file)
    logger.info(f"Loaded {tour_size} cities")
    
    # Initialize operators
    selection = RouletteWheelSelection()
    crossover = OrderCrossover(selection)
    mutation = SwapMutation(config.mutation_rate)
    fitness = DistanceBasedFitness()
    initializer = RandomInitializer()
    
    # Create and run GA
    ga = GeneticAlgorithm(
        config=config,
        crossover_operator=crossover,
        mutation_operator=mutation,
        fitness_evaluator=fitness,
        population_initializer=initializer,
        logger=logger
    )
    
    logger.info("Starting Genetic Algorithm...")
    optimal_tour, optimal_cost, optimal_probability = ga.run(cities, tour_size)
    
    # Display results
    print("\n" + "="*60)
    print("GENETIC ALGORITHM TSP SOLVER - RESULTS")
    print("="*60)
    print(f"\nOptimal Tour Cost: {optimal_cost:.2f}")
    print(f"Optimal Probability: {optimal_probability:.6f}")
    print(f"\nOptimal Tour Path:")
    for i, city in enumerate(optimal_tour, 1):
        print(f"  {i}. {city}")
    print("="*60)
    
    # Get and display statistics
    stats = ga.get_statistics()
    print(f"\nAlgorithm Statistics:")
    print(f"  Total Generations: {stats.get('total_generations')}")
    print(f"  Convergence Generation: {stats.get('convergence_generation')}")
    print(f"  Best Cost: {stats.get('best_cost'):.2f}")
    print(f"  Average Cost: {stats.get('average_cost'):.2f}")
    print(f"  Worst Cost: {stats.get('worst_cost'):.2f}")
    print(f"  Converged: {stats.get('converged')}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
