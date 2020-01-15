from __future__ import division
import random
from deap import tools, creator
import statistics
# sortuje według fitness niemalejąco
# do selekcji konwekcyjnej dla problemów jednokryterialnych


def sortByFitness(wholePopulation):
    wholePopulation.sort(key=lambda x: x.fitness, reverse=False)


def getMinFitness(island):

    minFit = island[0].fitness

    for individual in island[1:]:
        if individual.fitness < minFit:
            minFit = individual.fitness

    return minFit


def getMaxFitness(island):

    maxFit = island[0].fitness

    for individual in island[1:]:
        if individual.fitness > maxFit:
            maxFit = individual.fitness

    return maxFit


def getMeanFitness(island):

    fitnesses = []

    for individual in island:
        fitnesses.append(individual.fitness.values[0])

    return statistics.mean(fitnesses)


def isDominating(individual, other):
    count = 0
    for x, y in zip(individual, other):
        if x < y:
            return False
        if x == y:
            count += 1

    if count == len(individual):
        return False
    return True


# jeszcze nie gotowe - użyjemy wbudownej funckji jak będzie działać


def getParetoFronts(wholePopulation):
    fronts = []

    currentFront = []
    for individual in wholePopulation:
        for otherIndividual in wholePopulation:
            if(isDominating(otherIndividual, individual)):
                continue
    return fronts

# Migracja frontami pareto ze stałą liczbą wysp


def migSelFrontsContsInslands(populations, numOfIslands):
    wholePopulation = []

    for population in populations:
        wholePopulation += population

    pareto_fronts = tools.sortNondominated(
        wholePopulation, len(wholePopulation))

    wholePopulation = []

    for population in pareto_fronts:
        wholePopulation += population

    islandSize = int(len(wholePopulation) / numOfIslands)

    newIslands = []

    for i in range(0, len(wholePopulation), islandSize):
        newIslands.append(wholePopulation[i:i + islandSize])
        lastIndex = i + islandSize

    newIslands[-1] += wholePopulation[lastIndex:]

    for i, newIs in enumerate(newIslands):
        if(i >= len(populations)):
            populations.append(newIs)
        else:
            populations[i] = newIs

    if(len(populations) > len(newIslands)):
        del populations[len(newIslands):]

# Migracja między wyspami w selekcji konwekcyjnej dla problemów WIELOKRYTERIALNYCH


def migSelOneFrontOneIsland(populations):
    wholePopulation = []

    for population in populations:
        wholePopulation += population

    pareto_fronts = tools.sortNondominated(
        wholePopulation, len(wholePopulation))

    for i, newIs in enumerate(pareto_fronts):
        if(i >= len(populations)):
            populations.append(newIs)
        else:
            populations[i] = newIs

    if(len(populations) > len(pareto_fronts)):
        del populations[len(pareto_fronts):]

# Migracja między wyspami w selekcji konwekcyjnej dla problemów JEDNOKRYTERIALNYCH


def migSel(populations, numOfIslands):
    wholePopulation = []

    for population in populations:
        wholePopulation += population

    islandSize = int(len(wholePopulation) / numOfIslands)

    newIslands = []

    sortByFitness(wholePopulation)

    for i in range(0, len(wholePopulation), islandSize):
        newIslands.append(wholePopulation[i:i + islandSize])
        lastIndex = i + islandSize

    newIslands[-1] += wholePopulation[lastIndex:]

    for i, newIs in enumerate(newIslands):
        if(i >= len(populations)):
            populations.append(newIs)
        else:
            populations[i] = newIs

    if(len(populations) > len(newIslands)):
        del populations[len(newIslands):]
