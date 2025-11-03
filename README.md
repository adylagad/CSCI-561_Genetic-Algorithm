# CSCI-561 Genetic Algorithm - TSP Solver

A professional, modular Genetic Algorithm framework for solving the Traveling Salesman Problem (TSP) using evolutionary computation techniques.

## ⚠️ Academic Integrity Notice

**Important**: This repository contains a **significantly refactored and enhanced version** that is **completely different** from the code I originally submitted for the CSCI-561 course assignment.

**Key Differences from My Original Submission:**

-   **Original submission**: Monolithic, procedural implementation with functions in separate files
-   **This version**: Professional modular architecture with object-oriented design patterns
-   **Added**: Strategy Pattern, Dependency Injection, comprehensive testing suite (40+ tests), extensive documentation
-   **Restructured**: 30+ files with proper package organization vs. original 9 simple files
-   **Implementation**: Entirely rewritten with different algorithms, data structures, and design approach

This refactoring was performed **after the assignment deadline and submission** as a learning exercise in software engineering best practices. The code shown here is **fundamentally different from what I submitted** and does **not** violate any academic integrity policies. This public repository represents a portfolio piece demonstrating advanced software engineering concepts, distinct from the original coursework.

## 📋 Table of Contents

-   [Overview](#overview)
-   [Features](#features)
-   [Architecture](#architecture)
-   [Project Structure](#project-structure)
-   [Installation & Setup](#installation--setup)
-   [How to Run](#how-to-run)
-   [Input/Output Format](#inputoutput-format)
-   [Configuration](#configuration)
-   [Available Components](#available-components)
-   [Code Examples](#code-examples)
-   [Extending the Framework](#extending-the-framework)
-   [Testing](#testing)

## 🎯 Overview

This Genetic Algorithm implementation solves the Traveling Salesman Problem (TSP) using a modular, extensible architecture built on software engineering best practices. The framework allows easy experimentation with different genetic operators through pluggable components and comprehensive configuration management.

**Algorithm Flow:**

1. Initialize population with random or heuristic-based tours
2. Evaluate fitness of each individual (based on tour distance)
3. Select parents using selection operators (e.g., Roulette Wheel)
4. Create offspring through crossover (e.g., Order Crossover, PMX)
5. Apply mutation to maintain genetic diversity (e.g., Swap Mutation)
6. Repeat until convergence or maximum generations reached

## ✨ Features

-   ✅ **Modular Architecture** - Clean separation of concerns with single responsibility principle
-   ✅ **Strategy Pattern** - Pluggable operators (crossover, mutation, selection, initialization)
-   ✅ **Dependency Injection** - Loose coupling for easy testing and extension
-   ✅ **Type Safety** - Full type hints with custom type aliases
-   ✅ **Configuration Management** - JSON or code-based configuration with dataclasses
-   ✅ **SOLID Principles** - Professional software design patterns
-   ✅ **Abstract Base Classes** - Well-defined interfaces for all operators
-   ✅ **Comprehensive Logging** - Configurable logging with progress tracking
-   ✅ **Test Suite** - Verified functionality
-   ✅ **Multiple Examples** - Working examples for different use cases

## 🏗 Architecture

The framework follows **SOLID principles** and uses **Strategy Pattern** for operator implementation:

### Design Patterns

1. **Strategy Pattern**: Different algorithms (crossover, mutation, selection) are interchangeable through common interfaces
2. **Dependency Injection**: Components are injected rather than hard-coded
3. **Single Responsibility**: Each class/module has one clear purpose
4. **Open/Closed Principle**: Open for extension, closed for modification

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    GeneticAlgorithm                         │
│                   (Main Orchestrator)                        │
└─────────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Crossover   │  │   Mutation   │  │  Selection   │
│   Operator   │  │   Operator   │  │   Operator   │
└──────────────┘  └──────────────┘  └──────────────┘
          │               │               │
          ▼               ▼               ▼
    OrderCrossover   SwapMutation   RouletteWheel
    PMXCrossover                     Selection

          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Fitness    │  │ Population   │  │    Config    │
│  Evaluator   │  │ Initializer  │  │  Management  │
└──────────────┘  └──────────────┘  └──────────────┘
```

### Abstract Base Classes (Interfaces)

All operators implement abstract interfaces ensuring consistency:

-   **CrossoverOperator**: `cross()`, `apply()`
-   **MutationOperator**: `mutate()`
-   **SelectionOperator**: `select()`
-   **FitnessEvaluator**: `evaluate()`
-   **PopulationInitializer**: `initialize()`

## 📁 Project Structure

```
CSCI-561_Genetic-Algorithm/
├── genetic_algorithm/              # Main package
│   ├── __init__.py                # Package exports
│   │
│   ├── core/                      # Core algorithm components
│   │   ├── __init__.py
│   │   ├── algorithm.py           # GeneticAlgorithm class (main orchestrator)
│   │   ├── types.py               # Type definitions (City, Tour, Population, etc.)
│   │   └── interfaces.py          # Abstract base classes (Strategy interfaces)
│   │
│   ├── operators/                 # Genetic operators
│   │   ├── __init__.py
│   │   ├── crossover.py           # OrderCrossover, PMXCrossover
│   │   ├── mutation.py            # SwapMutation
│   │   └── selection.py           # RouletteWheelSelection
│   │
│   ├── initialization/            # Population initialization strategies
│   │   ├── __init__.py
│   │   └── population.py          # RandomInitializer, NearestNeighborInitializer
│   │
│   ├── evaluation/                # Fitness evaluation
│   │   ├── __init__.py
│   │   └── fitness.py             # DistanceBasedFitness, calculate_total_distance
│   │
│   └── utils/                     # Helper utilities
│       ├── __init__.py
│       └── helpers.py             # euclidean_distance, read_input, etc.
│
├── config/                        # Configuration management
│   ├── __init__.py
│   ├── config.py                  # GAConfig dataclass
│   └── default_config.json        # Default configuration settings
│
├── input/                         # Input data files
│   └── input1.txt                 # TSP city coordinates
│
├── main.py                        # Main entry point
├── test_ga.py                     # Comprehensive test suite
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🔧 Installation & Setup

### Prerequisites

-   Python 3.7 or higher
-   pip (Python package manager)

### Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### Verify Installation

```bash
# Run tests to verify setup
python test_ga.py
```

## 🚀 How to Run

### Basic Usage

```bash
# Run with default configuration
python main.py
```

### Run with Custom Configuration

You can modify the configuration in the code or create a custom JSON file:

**Option 1: Modify in code**

```python
from config.config import GAConfig

config = GAConfig(
    mutation_rate=0.1,
    number_of_generations=5000,
    convergence_threshold=100
)
```

**Option 2: Create custom JSON file**

```bash
# Create config/my_config.json with your settings
# Then load it in your code:
config = GAConfig.from_json("config/my_config.json")
```

### Run with Different Operators

```python
# Example: Use PMX crossover and Nearest Neighbor initialization
from genetic_algorithm.operators import PMXCrossover
from genetic_algorithm.initialization import NearestNeighborInitializer

selection = RouletteWheelSelection()
crossover = PMXCrossover(selection)  # Instead of OrderCrossover
initializer = NearestNeighborInitializer()  # Instead of RandomInitializer

# Then create GA with these operators
ga = GeneticAlgorithm(
    config=config,
    crossover_operator=crossover,
    mutation_operator=mutation,
    fitness_evaluator=fitness,
    population_initializer=initializer
)
```

### Expected Output

```
================================================================
RESULTS
================================================================
Optimal Tour: [(66, 153, 121), (116, 152, 189), ...]
Optimal Cost: 12345.67
Optimal Probability: 0.023456
================================================================

Statistics:
  total_generations: 3500
  convergence_generation: 2847
  best_fitness: 12345.67
  ...
```

## 📥 Input/Output Format

### Input File Structure

The input file (`input/input1.txt`) contains city coordinates in 3D space:

```
<number_of_cities>
<x1> <y1> <z1>
<x2> <y2> <z2>
...
<xn> <yn> <zn>
```

**Example:**

```
500
66 153 121
116 152 189
95 47 90
...
```

-   **Line 1**: Total number of cities (integer)
-   **Lines 2-N+1**: Each line contains three space-separated integers representing x, y, z coordinates
-   Coordinates represent cities in 3D Euclidean space

### Output Format

The program outputs three main results:

1. **Optimal Tour**: List of cities in visit order

    - Format: `[(x1, y1, z1), (x2, y2, z2), ...]`
    - Represents the best tour found

2. **Optimal Cost**: Total distance of the tour

    - Format: Floating-point number
    - Calculated using Euclidean distance: $\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2 + (z_2-z_1)^2}$

3. **Optimal Probability**: Selection probability

    - Format: Floating-point number (0-1)
    - Based on fitness in final population

4. **Statistics**: Additional metrics
    - Total generations run
    - Convergence generation (when best solution was found)
    - Best/average/worst fitness values

## ⚙️ Configuration

Configuration can be done via **code** or **JSON file**.

### Configuration Parameters

| Parameter                    | Default            | Description                                 |
| ---------------------------- | ------------------ | ------------------------------------------- |
| `mutation_rate`              | 0.05               | Probability of mutation (5%)                |
| `number_of_generations`      | 3500               | Maximum generations to run                  |
| `convergence_threshold`      | 50                 | Stop after N stagnant generations           |
| `population_size_multiplier` | 1                  | Population size = tour_size × multiplier    |
| `input_file`                 | "input/input1.txt" | Path to input file                          |
| `output_dir`                 | "output"           | Directory for output files                  |
| `log_level`                  | "INFO"             | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `verbose`                    | true               | Enable verbose logging                      |
| `log_interval`               | 100                | Log every N generations                     |

### Code-Based Configuration

```python
from config.config import GAConfig

config = GAConfig(
    mutation_rate=0.1,
    number_of_generations=5000,
    convergence_threshold=100,
    population_size_multiplier=2
)
```

### JSON Configuration

**File: `config/my_config.json`**

```json
{
	"mutation_rate": 0.1,
	"number_of_generations": 5000,
	"convergence_threshold": 100,
	"population_size_multiplier": 2,
	"input_file": "input/input1.txt",
	"log_level": "DEBUG"
}
```

**Load in code:**

```python
config = GAConfig.from_json("config/my_config.json")
```

## 🧩 Available Components

### Crossover Operators

-   **OrderCrossover (OX)** - Default

    -   Preserves relative order of cities from one parent
    -   Fills gaps with cities from other parent
    -   Good for maintaining tour structure

-   **PMXCrossover (PMX)** - Partially Mapped Crossover
    -   Creates mapping between two parent segments
    -   Preserves position information
    -   Better for highly structured problems

### Mutation Operators

-   **SwapMutation**
    -   Randomly swaps two cities in a tour
    -   Controlled by mutation_rate parameter
    -   Maintains tour validity (all cities visited once)

### Selection Operators

-   **RouletteWheelSelection**
    -   Probability-based selection
    -   Higher fitness = higher selection chance
    -   Maintains diversity in population

### Population Initializers

-   **RandomInitializer**

    -   Creates random permutations of cities
    -   Fast and simple
    -   Good for unbiased starting population

-   **NearestNeighborInitializer**
    -   Greedy nearest neighbor heuristic
    -   Creates better initial solutions
    -   Useful for faster convergence

### Fitness Evaluators

-   **DistanceBasedFitness**
    -   Calculates total tour distance
    -   Lower distance = higher fitness
    -   Uses Euclidean distance in 3D space

## 💻 Code Examples

### Example 1: Basic Usage

```python
from genetic_algorithm.core import GeneticAlgorithm
from genetic_algorithm.operators import OrderCrossover, SwapMutation, RouletteWheelSelection
from genetic_algorithm.evaluation import DistanceBasedFitness
from genetic_algorithm.initialization import RandomInitializer
from genetic_algorithm.utils import read_input
from config.config import GAConfig

# Load configuration
config = GAConfig()

# Read input
tour_size, cities = read_input(config.input_file)

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
    population_initializer=initializer
)

optimal_tour, optimal_cost, optimal_probability = ga.run(cities, tour_size)
print(f"Best tour distance: {optimal_cost:.2f}")
```

### Example 2: Using PMX Crossover

```python
from genetic_algorithm.operators import PMXCrossover

# Use PMX instead of Order Crossover
crossover = PMXCrossover(selection)

ga = GeneticAlgorithm(
    config=config,
    crossover_operator=crossover,  # Different operator
    mutation_operator=mutation,
    fitness_evaluator=fitness,
    population_initializer=initializer
)
```

### Example 3: Custom Configuration

```python
# Create custom configuration
config = GAConfig(
    mutation_rate=0.1,              # 10% mutation
    number_of_generations=10000,    # Run longer
    convergence_threshold=200,      # More patience
    population_size_multiplier=2,   # Larger population
    log_level="DEBUG"               # Detailed logging
)
```

### Example 4: Using Nearest Neighbor Initialization

```python
from genetic_algorithm.initialization import NearestNeighborInitializer

# Use heuristic initialization for better starting population
initializer = NearestNeighborInitializer()

ga = GeneticAlgorithm(
    config=config,
    crossover_operator=crossover,
    mutation_operator=mutation,
    fitness_evaluator=fitness,
    population_initializer=initializer  # Better initial solutions
)
```

## 🔌 Extending the Framework

The modular architecture makes it easy to add new operators.

### Adding a New Crossover Operator

```python
from genetic_algorithm.core.interfaces import CrossoverOperator
from genetic_algorithm.core.types import Tour, Population, FloatList

class MyCrossover(CrossoverOperator):
    """Custom crossover operator."""

    def cross(self, parent1: Tour, parent2: Tour) -> Tour:
        """Implement your crossover logic."""
        # Your implementation here
        offspring = []
        # ... crossover logic ...
        return offspring

    def apply(self, population: Population, population_size: int,
              probabilities: FloatList) -> Population:
        """Apply crossover to population."""
        new_population = []
        for _ in range(population_size):
            parent1, parent2 = self.selection.select(probabilities, population)
            offspring = self.cross(parent1, parent2)
            new_population.append(offspring)
        return new_population
```

### Adding a New Mutation Operator

```python
from genetic_algorithm.core.interfaces import MutationOperator
from genetic_algorithm.core.types import Population

class MyMutation(MutationOperator):
    """Custom mutation operator."""

    def __init__(self, mutation_rate: float):
        self.mutation_rate = mutation_rate

    def mutate(self, population: Population) -> Population:
        """Implement your mutation logic."""
        # Your implementation here
        return mutated_population
```

### Adding a New Selection Operator

```python
from genetic_algorithm.core.interfaces import SelectionOperator
from genetic_algorithm.core.types import Parents, FloatList, Population

class MySelection(SelectionOperator):
    """Custom selection operator."""

    def select(self, probabilities: FloatList, population: Population) -> Parents:
        """Implement your selection logic."""
        # Your implementation here
        return (parent1, parent2)
```

### Using Your Custom Operator

```python
# Use your custom operators
my_crossover = MyCrossover(selection)
my_mutation = MyMutation(0.05)

ga = GeneticAlgorithm(
    config=config,
    crossover_operator=my_crossover,  # Your custom operator
    mutation_operator=my_mutation,     # Your custom operator
    fitness_evaluator=fitness,
    population_initializer=initializer
)
```

## 🧪 Testing

### Run All Tests

```bash
python test_ga.py
```

### Test Coverage

The test suite covers:

-   ✅ **Utility Functions**: Distance calculation, input reading, validation
-   ✅ **Fitness Evaluation**: Distance calculation, fitness scoring
-   ✅ **Population Initialization**: Random and nearest neighbor strategies
-   ✅ **Selection Operators**: Roulette wheel selection and probability bias
-   ✅ **Crossover Operators**: Order crossover and PMX validity and inheritance
-   ✅ **Mutation Operators**: Swap mutation validity and rate control
-   ✅ **Configuration Management**: Default, custom, JSON loading, serialization
-   ✅ **Genetic Algorithm**: Complete execution, solution improvement, statistics
-   ✅ **Edge Cases**: Empty tours, single cities, boundary conditions
-   ✅ **Algorithm Correctness**: Tour validity, convergence, operator combinations

### Test Structure

The test suite uses Python's `unittest` framework with the following test classes:

-   **TestUtilityFunctions**: Tests for distance calculation and I/O
-   **TestFitnessEvaluation**: Tests for fitness calculation
-   **TestPopulationInitialization**: Tests for population initialization strategies
-   **TestSelectionOperator**: Tests for parent selection
-   **TestCrossoverOperators**: Tests for crossover operations
-   **TestMutationOperator**: Tests for mutation operations
-   **TestConfiguration**: Tests for configuration management
-   **TestGeneticAlgorithm**: Tests for complete algorithm execution

### Expected Test Output

```
test_config_json_loading (__main__.TestConfiguration) ... ok
test_config_serialization (__main__.TestConfiguration) ... ok
test_custom_config (__main__.TestConfiguration) ... ok
test_default_config (__main__.TestConfiguration) ... ok
test_population_size_calculation (__main__.TestConfiguration) ... ok
test_order_crossover_validity (__main__.TestCrossoverOperators) ... ok
test_pmx_crossover_validity (__main__.TestCrossoverOperators) ... ok
...
test_ga_improves_solution (__main__.TestGeneticAlgorithm) ... ok
test_ga_statistics (__main__.TestGeneticAlgorithm) ... ok
test_ga_with_different_operators (__main__.TestGeneticAlgorithm) ... ok

----------------------------------------------------------------------
Ran 40 tests in 45.234s

OK

======================================================================
🎉 ALL TESTS PASSED! 🎉
Ran 40 tests successfully
======================================================================
```

## 📝 Type System

The framework uses comprehensive type hints for better code quality:

```python
# Core type definitions
City = Tuple[int, int, int]              # 3D coordinates
Tour = List[City]                        # Sequence of cities
Population = List[Tour]                  # Collection of tours
FloatList = List[float]                  # Fitness values, probabilities
Parents = Tuple[Tour, Tour]              # Parent pair
Statistics = Dict[str, Any]              # Algorithm statistics
ConfigDict = Dict[str, Any]              # Configuration dictionary
```

## 📄 License

This project is part of CSCI-561 coursework.

## 👥 Author

Created for CSCI-561 Artificial Intelligence course.

---

**Questions or Issues?** Check the code examples or run the test suite to verify functionality

## 📖 Usage

```python
from genetic_algorithm.core import GeneticAlgorithm
from genetic_algorithm.operators import OrderCrossover, SwapMutation, RouletteWheelSelection
from genetic_algorithm.evaluation import DistanceBasedFitness
from genetic_algorithm.initialization import RandomInitializer
from genetic_algorithm.utils import read_input
from config.config import GAConfig

# Setup
config = GAConfig()
tour_size, cities = read_input("input/input1.txt")

# Create operators
selection = RouletteWheelSelection()
crossover = OrderCrossover(selection)
mutation = SwapMutation(config.mutation_rate)
fitness = DistanceBasedFitness()
initializer = RandomInitializer()

# Run GA
ga = GeneticAlgorithm(config, crossover, mutation, fitness, initializer)
tour, cost, prob = ga.run(cities, tour_size)

print(f"Best tour cost: {cost}")
```

## 🔧 Configuration

Edit `config/default_config.json` or create your own:

```json
{
	"mutation_rate": 0.05,
	"number_of_generations": 3500,
	"convergence_threshold": 50
}
```

## 📊 Architecture

Built with professional design patterns:

-   **Strategy Pattern** for operators
-   **Dependency Injection** for flexibility
-   **SOLID Principles** throughout
-   **Clean Architecture** for maintainability

## 🧪 Testing

```bash
python test_modular.py
```

## 📝 Version History

-   **v2.0.0** - Modular architecture (current)
-   **v1.0.0** - Original implementation (removed)

## 📄 License

This project is part of CSCI-561 coursework.

## 👥 Author

Created for CSCI-561 Artificial Intelligence course.

---

## 📌 Disclaimer

The code in this repository represents a post-assignment refactoring project undertaken to learn professional software engineering practices. **The code shown here is entirely different from what I submitted for the CSCI-561 assignment.** My actual assignment submission used a simpler, procedural approach with basic file organization. This modular implementation demonstrates advanced concepts including:

-   Object-oriented design patterns (Strategy, Dependency Injection)
-   SOLID principles and clean architecture
-   Comprehensive unit testing (40+ tests)
-   Professional documentation and code organization
-   Type safety with full type hints

**This enhanced version serves as a portfolio piece and learning artifact, completely distinct from my original coursework submission. The implementations are fundamentally different.**
