from dataclasses import dataclass
from typing import Dict

# Legacy defaults (kept for backwards compatibility)
mutationRate = 0.05
numberOfGenerations = 3500
threshold = 50


@dataclass
class HyperParams:
    population: int
    generations: int
    mutation_rate: float
    threshold: int
    nearest_fraction: float


def get_hyperparams(n: int) -> HyperParams:
    """Return tuned GA hyperparameters for the given number of cities `n`.

	Supported sizes with tuned presets: 50, 100, 200, 500.
	If `n` does not match one of those exact sizes, a sensible fallback
	is returned based on `n`.
	"""
    presets: Dict[int, HyperParams] = {
        50:
        HyperParams(population=200,
                    generations=500,
                    mutation_rate=0.08,
                    threshold=50,
                    nearest_fraction=0.7),
        100:
        HyperParams(population=150,
                    generations=400,
                    mutation_rate=0.07,
                    threshold=40,
                    nearest_fraction=0.7),
        200:
        HyperParams(population=100,
                    generations=300,
                    mutation_rate=0.06,
                    threshold=30,
                    nearest_fraction=0.6),
        500:
        HyperParams(population=60,
                    generations=200,
                    mutation_rate=0.05,
                    threshold=20,
                    nearest_fraction=0.5),
    }

    if n in presets:
        return presets[n]

    # fallback heuristic scaling: reduce population and generations as n increases
    if n <= 50:
        return presets[50]
    if n <= 100:
        return presets[100]
    if n <= 200:
        return presets[200]

    # default fallback for very large n
    return HyperParams(population=max(20, n // 5),
                       generations=max(50, 1000 // (n // 100 + 1)),
                       mutation_rate=0.05,
                       threshold=30,
                       nearest_fraction=0.5)
