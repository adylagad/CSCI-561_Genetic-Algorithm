from utils import readInput, populationSize
from initial_population import randomInitialPopulation
from fitness_evaluation import calculateFitness, calculateTotalDistance
from crossover import crossover
from mutation import mutate
from GATypes import Tour, FloatList
from constants import numberOfGenerations, mutationRate, threshold


def main() -> None:
    optimalProbability = float('infinity')
    optimalTour: Tour = []
    optimalCost = float('infinity')
    # keeps track of the number of generations that dont produce a good outcome
    count = 0
    tourSize, listOfCities = readInput("input/input1.txt")
    initialPopulationRandom = randomInitialPopulation(listOfCities)
    probabilities = calculateFitness(initialPopulationRandom)
    print("Initial Population: ", min(probabilities))
    for _ in range(numberOfGenerations):
        if count > threshold:
            break
        newPopulation = mutate(
            crossover(initialPopulationRandom, populationSize(tourSize)),
            mutationRate, tourSize)
        probabilities = calculateFitness(newPopulation)
        localMinimum = min(probabilities)
        if localMinimum < optimalProbability:
            distances: FloatList = [
                calculateTotalDistance(tour) for tour in newPopulation
            ]
            optimalProbability = localMinimum
            index = probabilities.index(optimalProbability)
            optimalCost = distances[index]
            optimalTour = newPopulation[index]
            count = 0
        count += 1
    print("Optimal Probability: ", optimalProbability)
    print("Optimal Cost: ", optimalCost)
    optimalTour.append(optimalTour[0])
    print("Optimal Tour: ", optimalTour)


if __name__ == "__main__":
    main()
