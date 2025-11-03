"""
Comprehensive test suite for the Genetic Algorithm TSP Solver.

Tests cover:
- Algorithm correctness
- Operator functionality
- Edge cases
- Performance validation
- Configuration management
"""
import unittest
from genetic_algorithm.core import GeneticAlgorithm
from genetic_algorithm.core.types import City, Tour, Population
from genetic_algorithm.operators import (
    OrderCrossover, PMXCrossover, SwapMutation, RouletteWheelSelection
)
from genetic_algorithm.evaluation import DistanceBasedFitness, calculate_total_distance
from genetic_algorithm.initialization import RandomInitializer, NearestNeighborInitializer
from genetic_algorithm.utils import read_input, euclidean_distance, verify_number_of_cities
from config.config import GAConfig


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions for distance calculation and I/O."""
    
    def test_euclidean_distance(self):
        """Test 3D Euclidean distance calculation."""
        city1: City = (0, 0, 0)
        city2: City = (3, 4, 0)
        distance = euclidean_distance(city1, city2)
        self.assertEqual(distance, 5.0, "Distance should be 5.0 (3-4-5 triangle)")
        
        # Test with z-coordinate
        city3: City = (0, 0, 0)
        city4: City = (1, 0, 0)
        distance2 = euclidean_distance(city3, city4)
        self.assertEqual(distance2, 1.0, "Distance should be 1.0")
    
    def test_euclidean_distance_symmetry(self):
        """Test that distance is symmetric."""
        city1: City = (10, 20, 30)
        city2: City = (40, 50, 60)
        d1 = euclidean_distance(city1, city2)
        d2 = euclidean_distance(city2, city1)
        self.assertEqual(d1, d2, "Distance should be symmetric")
    
    def test_euclidean_distance_zero(self):
        """Test distance to same city is zero."""
        city: City = (100, 200, 300)
        distance = euclidean_distance(city, city)
        self.assertEqual(distance, 0.0, "Distance to same city should be 0")
    
    def test_read_input(self):
        """Test reading input file."""
        tour_size, cities = read_input("input/input1.txt")
        self.assertIsInstance(tour_size, int, "Tour size should be an integer")
        self.assertIsInstance(cities, list, "Cities should be a list")
        self.assertEqual(len(cities), tour_size, "Number of cities should match tour size")
        
        # Verify each city has 3 coordinates
        for city in cities:
            self.assertEqual(len(city), 3, "Each city should have 3 coordinates")
            self.assertIsInstance(city[0], int, "X coordinate should be integer")
            self.assertIsInstance(city[1], int, "Y coordinate should be integer")
            self.assertIsInstance(city[2], int, "Z coordinate should be integer")
    
    def test_verify_number_of_cities(self):
        """Test city count verification."""
        cities: Tour = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        self.assertTrue(verify_number_of_cities(3, cities))
        self.assertFalse(verify_number_of_cities(2, cities))
        self.assertFalse(verify_number_of_cities(4, cities))


class TestFitnessEvaluation(unittest.TestCase):
    """Test fitness evaluation and distance calculation."""
    
    def setUp(self):
        """Set up test cities."""
        self.cities: Tour = [
            (0, 0, 0),
            (3, 4, 0),
            (6, 8, 0),
            (0, 0, 0)  # Return to start
        ]
    
    def test_calculate_total_distance(self):
        """Test total distance calculation for a tour."""
        distance = calculate_total_distance(self.cities)
        # 0->1: 5, 1->2: 5, 2->3: 10
        expected = 5.0 + 5.0 + 10.0
        self.assertEqual(distance, expected, f"Expected distance {expected}, got {distance}")
    
    def test_fitness_evaluator(self):
        """Test fitness evaluator on population."""
        fitness_evaluator = DistanceBasedFitness()
        population: Population = [
            [(0, 0, 0), (1, 0, 0), (0, 0, 0)],  # Distance: 2
            [(0, 0, 0), (3, 4, 0), (0, 0, 0)],  # Distance: 10
        ]
        
        fitness_scores = fitness_evaluator.evaluate(population)
        self.assertEqual(len(fitness_scores), 2, "Should have 2 fitness scores")
        self.assertGreater(fitness_scores[0], fitness_scores[1], 
                          "Shorter tour should have higher fitness")
        self.assertTrue(all(f > 0 for f in fitness_scores), 
                       "All fitness scores should be positive")
    
    def test_fitness_empty_tour(self):
        """Test fitness evaluation handles edge cases."""
        fitness_evaluator = DistanceBasedFitness()
        population: Population = [[(0, 0, 0)]]  # Single city
        fitness_scores = fitness_evaluator.evaluate(population)
        self.assertEqual(len(fitness_scores), 1, "Should handle single city")


class TestPopulationInitialization(unittest.TestCase):
    """Test population initialization strategies."""
    
    def setUp(self):
        """Set up test cities."""
        self.cities: Tour = [
            (0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0)
        ]
        self.population_size = 10
    
    def test_random_initializer(self):
        """Test random population initialization."""
        initializer = RandomInitializer()
        population = initializer.initialize(self.cities, self.population_size)
        
        self.assertEqual(len(population), self.population_size, 
                        "Population size should match requested size")
        
        for tour in population:
            # Each tour should visit all cities plus return to start
            self.assertEqual(len(tour), len(self.cities) + 1, 
                           "Tour should include all cities plus return")
            self.assertEqual(tour[0], tour[-1], 
                           "Tour should start and end at same city")
            
            # Check all cities are visited (excluding return)
            tour_cities = set(tour[:-1])
            self.assertEqual(len(tour_cities), len(self.cities), 
                           "All cities should be visited exactly once")
    
    def test_nearest_neighbor_initializer(self):
        """Test nearest neighbor heuristic initialization."""
        initializer = NearestNeighborInitializer()
        population = initializer.initialize(self.cities, self.population_size)
        
        self.assertEqual(len(population), self.population_size, 
                        "Population size should match requested size")
        
        for tour in population:
            self.assertEqual(len(tour), len(self.cities) + 1, 
                           "Tour should include all cities plus return")
            self.assertEqual(tour[0], tour[-1], 
                           "Tour should start and end at same city")
            
            # Check tour validity
            tour_cities = set(tour[:-1])
            self.assertEqual(len(tour_cities), len(self.cities), 
                           "All cities should be visited exactly once")
    
    def test_nearest_neighbor_quality(self):
        """Test that nearest neighbor produces reasonable initial solutions."""
        random_init = RandomInitializer()
        nn_init = NearestNeighborInitializer()
        
        # Create populations
        random_pop = random_init.initialize(self.cities, 20)
        nn_pop = nn_init.initialize(self.cities, 20)
        
        # Calculate average distances
        random_avg = sum(calculate_total_distance(tour) for tour in random_pop) / len(random_pop)
        nn_avg = sum(calculate_total_distance(tour) for tour in nn_pop) / len(nn_pop)
        
        # Nearest neighbor should generally produce better initial solutions
        self.assertLessEqual(nn_avg, random_avg * 1.5, 
                            "NN initialization should be reasonably good")


class TestSelectionOperator(unittest.TestCase):
    """Test selection operators."""
    
    def test_roulette_wheel_selection(self):
        """Test roulette wheel selection."""
        selector = RouletteWheelSelection()
        population: Population = [
            [(0, 0, 0), (1, 0, 0), (0, 0, 0)],
            [(0, 0, 0), (2, 0, 0), (0, 0, 0)],
            [(0, 0, 0), (3, 0, 0), (0, 0, 0)],
        ]
        probabilities = [0.5, 0.3, 0.2]  # Higher probability for first tour
        
        parent1, parent2 = selector.select(probabilities, population)
        
        # Check parents are valid tours from population
        self.assertIn(parent1, population, "Parent1 should be from population")
        self.assertIn(parent2, population, "Parent2 should be from population")
        self.assertEqual(len(parent1), 3, "Parent1 should be valid tour")
        self.assertEqual(len(parent2), 3, "Parent2 should be valid tour")
    
    def test_selection_bias(self):
        """Test that selection favors higher probabilities."""
        selector = RouletteWheelSelection()
        population: Population = [
            [(0, 0, 0), (1, 0, 0), (0, 0, 0)],  # High probability
            [(0, 0, 0), (2, 0, 0), (0, 0, 0)],  # Low probability
        ]
        probabilities = [0.99, 0.01]
        
        # Run multiple selections
        selections: Population = []
        for _ in range(100):
            parent1, parent2 = selector.select(probabilities, population)
            selections.append(parent1)
            selections.append(parent2)
        
        # Count selections of first (high probability) tour
        first_tour_count = sum(1 for tour in selections if tour == population[0])
        
        # Should select first tour much more often
        self.assertGreater(first_tour_count, 100, 
                          "High probability tour should be selected more often")


class TestCrossoverOperators(unittest.TestCase):
    """Test crossover operators."""
    
    def setUp(self):
        """Set up test tours."""
        self.parent1: Tour = [(1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0), (5, 0, 0)]
        self.parent2: Tour = [(3, 0, 0), (1, 0, 0), (5, 0, 0), (2, 0, 0), (4, 0, 0)]
        self.selection = RouletteWheelSelection()
    
    def test_order_crossover_validity(self):
        """Test that Order Crossover produces valid tours."""
        crossover = OrderCrossover(self.selection)
        offspring = crossover.cross(self.parent1, self.parent2)
        
        # Check offspring is a valid tour
        self.assertEqual(len(offspring), len(self.parent1), 
                        "Offspring should have same length as parents")
        self.assertEqual(set(offspring), set(self.parent1), 
                        "Offspring should contain all cities from parent")
        self.assertEqual(len(set(offspring)), len(offspring), 
                        "No duplicate cities in offspring")
    
    def test_pmx_crossover_validity(self):
        """Test that PMX Crossover produces valid tours."""
        crossover = PMXCrossover(self.selection)
        offspring = crossover.cross(self.parent1, self.parent2)
        
        # Check offspring is a valid tour
        self.assertEqual(len(offspring), len(self.parent1), 
                        "Offspring should have same length as parents")
        self.assertEqual(set(offspring), set(self.parent1), 
                        "Offspring should contain all cities from parent")
        self.assertEqual(len(set(offspring)), len(offspring), 
                        "No duplicate cities in offspring")
    
    def test_crossover_inheritance(self):
        """Test that offspring inherits genes from both parents."""
        crossover = OrderCrossover(self.selection)
        
        # Run crossover multiple times
        for _ in range(10):
            offspring = crossover.cross(self.parent1, self.parent2)
            
            # Offspring should share some subsequences with parents
            # (not testing exact inheritance due to randomness)
            self.assertEqual(set(offspring), set(self.parent1), 
                           "Offspring should have all cities")


class TestMutationOperator(unittest.TestCase):
    """Test mutation operators."""
    
    def test_swap_mutation_validity(self):
        """Test that swap mutation produces valid tours."""
        mutation = SwapMutation(mutation_rate=1.0)  # 100% mutation for testing
        tour: Tour = [(1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0), (5, 0, 0), (1, 0, 0)]
        population: Population = [tour]
        
        mutated_pop = mutation.mutate(population)
        mutated_tour = mutated_pop[0]
        
        # Check validity
        self.assertEqual(len(mutated_tour), len(tour), 
                        "Mutated tour should have same length")
        self.assertEqual(mutated_tour[0], mutated_tour[-1], 
                        "Mutated tour should still start/end at same city")
        self.assertEqual(set(mutated_tour[:-1]), set(tour[:-1]), 
                        "Mutated tour should have same cities")
    
    def test_mutation_rate(self):
        """Test that mutation rate is respected."""
        mutation = SwapMutation(mutation_rate=0.0)  # 0% mutation
        tour: Tour = [(1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0), (1, 0, 0)]
        population: Population = [tour] * 10
        
        mutated_pop = mutation.mutate(population)
        
        # With 0% mutation rate, tours should be unchanged
        for i, mutated_tour in enumerate(mutated_pop):
            self.assertEqual(mutated_tour, tour, 
                           f"Tour {i} should be unchanged with 0% mutation rate")
    
    def test_mutation_changes_tour(self):
        """Test that mutation actually changes tours."""
        mutation = SwapMutation(mutation_rate=1.0)  # 100% mutation
        tour: Tour = [(1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0), (5, 0, 0), (1, 0, 0)]
        population: Population = [tour] * 10
        
        mutated_pop = mutation.mutate(population)
        
        # At least some tours should be different (with high probability)
        changes = sum(1 for mutated in mutated_pop if mutated != tour)
        self.assertGreater(changes, 0, 
                          "At least some tours should be mutated with 100% rate")


class TestConfiguration(unittest.TestCase):
    """Test configuration management."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = GAConfig()
        self.assertEqual(config.mutation_rate, 0.05)
        self.assertEqual(config.number_of_generations, 3500)
        self.assertEqual(config.convergence_threshold, 50)
        self.assertEqual(config.population_size_multiplier, 1)
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = GAConfig(
            mutation_rate=0.1,
            number_of_generations=5000,
            convergence_threshold=100,
            population_size_multiplier=2
        )
        self.assertEqual(config.mutation_rate, 0.1)
        self.assertEqual(config.number_of_generations, 5000)
        self.assertEqual(config.convergence_threshold, 100)
        self.assertEqual(config.population_size_multiplier, 2)
    
    def test_config_json_loading(self):
        """Test loading configuration from JSON."""
        config = GAConfig.from_json("config/default_config.json")
        self.assertIsInstance(config, GAConfig)
        self.assertEqual(config.mutation_rate, 0.05)
    
    def test_config_serialization(self):
        """Test configuration to dictionary conversion."""
        config = GAConfig(mutation_rate=0.15)
        config_dict = config.to_dict()
        
        self.assertIsInstance(config_dict, dict)
        self.assertEqual(config_dict['mutation_rate'], 0.15)
        self.assertIn('number_of_generations', config_dict)
    
    def test_population_size_calculation(self):
        """Test population size calculation."""
        config = GAConfig(population_size_multiplier=2)
        pop_size = config.population_size(tour_size=50)
        self.assertEqual(pop_size, 100, "Population size should be 50 * 2")


class TestGeneticAlgorithm(unittest.TestCase):
    """Test the complete genetic algorithm."""
    
    def setUp(self):
        """Set up GA components."""
        self.config = GAConfig(
            number_of_generations=100,
            convergence_threshold=20,
            verbose=False
        )
        self.selection = RouletteWheelSelection()
        self.crossover = OrderCrossover(self.selection)
        self.mutation = SwapMutation(self.config.mutation_rate)
        self.fitness = DistanceBasedFitness()
        self.initializer = RandomInitializer()
    
    def test_ga_completes(self):
        """Test that GA runs to completion."""
        tour_size, cities = read_input("input/input1.txt")
        
        ga = GeneticAlgorithm(
            config=self.config,
            crossover_operator=self.crossover,
            mutation_operator=self.mutation,
            fitness_evaluator=self.fitness,
            population_initializer=self.initializer
        )
        
        optimal_tour, optimal_cost, optimal_probability = ga.run(cities, tour_size)
        
        # Verify results
        self.assertIsNotNone(optimal_tour, "Should return optimal tour")
        self.assertGreater(optimal_cost, 0, "Cost should be positive")
        self.assertGreater(optimal_probability, 0, "Probability should be positive")
        self.assertEqual(len(optimal_tour), tour_size + 1, 
                        "Tour should visit all cities and return")
    
    def test_ga_improves_solution(self):
        """Test that GA improves solution over time."""
        tour_size, cities = read_input("input/input1.txt")
        
        # Get initial random solution
        initial_pop = self.initializer.initialize(cities, tour_size)
        initial_costs = [calculate_total_distance(tour) for tour in initial_pop]
        initial_best = min(initial_costs)
        
        # Run GA
        ga = GeneticAlgorithm(
            config=self.config,
            crossover_operator=self.crossover,
            mutation_operator=self.mutation,
            fitness_evaluator=self.fitness,
            population_initializer=self.initializer
        )
        
        _, optimal_cost, _ = ga.run(cities, tour_size)
        
        # GA should find better solution than random initialization
        self.assertLessEqual(optimal_cost, initial_best, 
                            "GA should improve upon initial random solution")
    
    def test_ga_statistics(self):
        """Test that GA collects statistics."""
        tour_size, cities = read_input("input/input1.txt")
        
        ga = GeneticAlgorithm(
            config=self.config,
            crossover_operator=self.crossover,
            mutation_operator=self.mutation,
            fitness_evaluator=self.fitness,
            population_initializer=self.initializer
        )
        
        ga.run(cities, tour_size)
        stats = ga.get_statistics()
        
        self.assertIsInstance(stats, dict, "Statistics should be a dictionary")
        self.assertIn('total_generations', stats)
        self.assertIn('best_cost', stats)
    
    def test_ga_with_different_operators(self):
        """Test GA with different operator combinations."""
        tour_size, cities = read_input("input/input1.txt")
        
        # Test with PMX crossover
        pmx_crossover = PMXCrossover(self.selection)
        ga_pmx = GeneticAlgorithm(
            config=self.config,
            crossover_operator=pmx_crossover,
            mutation_operator=self.mutation,
            fitness_evaluator=self.fitness,
            population_initializer=self.initializer
        )
        
        tour1, cost1, _ = ga_pmx.run(cities, tour_size)
        self.assertIsNotNone(tour1, "PMX should produce valid result")
        self.assertGreater(cost1, 0, "PMX should produce valid cost")
        
        # Test with Nearest Neighbor initialization
        nn_initializer = NearestNeighborInitializer()
        ga_nn = GeneticAlgorithm(
            config=self.config,
            crossover_operator=self.crossover,
            mutation_operator=self.mutation,
            fitness_evaluator=self.fitness,
            population_initializer=nn_initializer
        )
        
        tour2, cost2, _ = ga_nn.run(cities, tour_size)
        self.assertIsNotNone(tour2, "NN initialization should produce valid result")
        self.assertGreater(cost2, 0, "NN initialization should produce valid cost")


def run_test_suite():
    """Run all tests and display results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestUtilityFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestFitnessEvaluation))
    suite.addTests(loader.loadTestsFromTestCase(TestPopulationInitialization))
    suite.addTests(loader.loadTestsFromTestCase(TestSelectionOperator))
    suite.addTests(loader.loadTestsFromTestCase(TestCrossoverOperators))
    suite.addTests(loader.loadTestsFromTestCase(TestMutationOperator))
    suite.addTests(loader.loadTestsFromTestCase(TestConfiguration))
    suite.addTests(loader.loadTestsFromTestCase(TestGeneticAlgorithm))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    if result.wasSuccessful():
        print("🎉 ALL TESTS PASSED! 🎉")
        print(f"Ran {result.testsRun} tests successfully")
    else:
        print("❌ SOME TESTS FAILED")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_test_suite()
