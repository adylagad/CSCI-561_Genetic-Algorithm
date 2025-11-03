"""Type definitions for the Genetic Algorithm."""
from typing import Tuple, List, Dict, Any

# Basic types
City = Tuple[int, int, int]
Tour = List[Tuple[int, int, int]]
Population = List[List[Tuple[int, int, int]]]
Input = Tuple[int, List[Tuple[int, int, int]]]
FloatList = List[float]
Parents = Tuple[Tour, Tour]

# Additional utility types
Statistics = Dict[str, Any]
ConfigDict = Dict[str, Any]
