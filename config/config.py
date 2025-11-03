"""Configuration management for the Genetic Algorithm."""
from dataclasses import dataclass
from typing import Any, Dict
import json
import os

# Type alias for configuration dictionaries
ConfigDict = Dict[str, Any]


@dataclass
class GAConfig:
    """Configuration parameters for the Genetic Algorithm."""
    
    # Algorithm parameters
    mutation_rate: float = 0.05
    number_of_generations: int = 3500
    convergence_threshold: int = 50
    
    # Population parameters
    population_size_multiplier: int = 1  # multiplied by tour size
    
    # Input/Output
    input_file: str = "input/input1.txt"
    output_dir: str = "output"
    
    # Logging
    log_level: str = "INFO"
    verbose: bool = True
    log_interval: int = 100  # Log every N generations
    
    @classmethod
    def from_dict(cls, config_dict: ConfigDict) -> 'GAConfig':
        """Create config from dictionary."""
        return cls(**{k: v for k, v in config_dict.items() if k in cls.__annotations__})
    
    @classmethod
    def from_json(cls, json_path: str) -> 'GAConfig':
        """Load configuration from JSON file."""
        with open(json_path, 'r') as f:
            config_dict: ConfigDict = json.load(f)
        return cls.from_dict(config_dict)
    
    def to_dict(self) -> ConfigDict:
        """Convert config to dictionary."""
        return {
            'mutation_rate': self.mutation_rate,
            'number_of_generations': self.number_of_generations,
            'convergence_threshold': self.convergence_threshold,
            'population_size_multiplier': self.population_size_multiplier,
            'input_file': self.input_file,
            'output_dir': self.output_dir,
            'log_level': self.log_level,
            'verbose': self.verbose,
            'log_interval': self.log_interval
        }
    
    def to_json(self, json_path: str) -> None:
        """Save configuration to JSON file."""
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)
    
    def population_size(self, tour_size: int) -> int:
        """Calculate population size based on tour size."""
        return tour_size * self.population_size_multiplier
