import random
from deap import creator, base, tools, algorithms, benchmarks
import migration as mig
import time
import utils
import numpy
import pickle
import sys


# Przetwarzanie parametrów
# argv[0] to nazwa programu - tak jest domyślnie
# WSPÓŁCZYNNIK MIGRACJI (to * N - liczba ewolucji między migracjami) - argv[1]
# LICZBA WYSP - argv[2]
# LICZBA EWOLUCJI - argv[3]
# LICZBA POWTÓRZEŃ ALGORYTMU - argv[4]

# Nazwa pliku - nazwa benchmarka
benchmarkName = sys.argv[0]

# współczynnik migracji
NUM_OF_MIGRATIONS = int(sys.argv[1])

# Początkowa liczba wysp
ISLANDS = int(sys.argv[2])

# liczba generacji
NGEN = int(sys.argv[3])

# Liczba powtórzeń algorytmu
numOfIterations = int(sys.argv[4])

# Dla każdej wyspy
POPULATION_SIZE = 100
ISLAND_POPULATION_SIZE = int(POPULATION_SIZE / ISLANDS)

FREQ = NUM_OF_MIGRATIONS * POPULATION_SIZE

# Każdy osobnik - individual ma liczbę atrybutów = len(weights), jeżeli -1 - minimaliazcja, jeżeli 1 - maksymalizacja
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()


ATTRIBUTES = 2
toolbox.register("attr_float", random.uniform, -6, 6)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_float, ATTRIBUTES)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Funkcja celu


def evalBenchmark(individual):
    return benchmarks.himmelblau(individual)


toolbox.register("evaluate", evalBenchmark)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutPolynomialBounded,
                 low=-100, up=100, indpb=0.1, eta=3.5)

toolbox.register("select", tools.selTournament, tournsize=3)

toolbox.register("map", map)


# dodanie migracji - mig.migSel to funkcja migracji selekcji konwekcyjnej
toolbox.register("migrate", mig.migSel, numOfIslands=ISLANDS)

stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)


CXPB, MUTPB = 0.5, 0.1
# ngen = FREQ oznacza ile wykonań algorytmu się wykona przy jednym uruchomieniu funkcji
toolbox.register("algorithm", algorithms.eaSimple, toolbox=toolbox,
                 stats=stats, cxpb=CXPB, mutpb=MUTPB, ngen=FREQ, verbose=False)


for algNum in range(0, numOfIterations):
    print("Iteracja algorytmu:", algNum + 1)
    logbooks = []
    # Zapisuje n najlepszych osobników (tutaj n = 1)
    hallOfFame = tools.HallOfFame(1)
    bestIndividuals = []
    start_time = time.time()
    iterations_wo_improvement = 0
    previous_fitness = 99999

    islands = [toolbox.population(n=ISLAND_POPULATION_SIZE)
               for i in range(ISLANDS)]
    for i in range(0, NGEN, FREQ):
        print("Postęp iteracji:", round((i / NGEN) * 100, 2), "%")

        results = toolbox.map(toolbox.algorithm, islands)

        ziped = list(map(list, zip(*results)))
        islands = ziped[0]

        # Jeżeli znajdzie lepszego osobnika niż najlepszy obecnie, to nadpisuje go
        for island in islands:
            hallOfFame.update(island)

        if previous_fitness == hallOfFame[0].fitness.values:
            iterations_wo_improvement += 1
        else:
            iterations_wo_improvement = 0
            previous_fitness = hallOfFame[0].fitness.values

        if(round((i / NGEN) * 100, 2) % 10 == 0):
            print("Hall of fame:", hallOfFame[0], hallOfFame[0].fitness)

        bestIndividuals.append(hallOfFame[0].fitness.values)

        if i == 0:
            for logbook in ziped[1]:
                logbooks.append(logbook)
        else:
            for k, logbook in enumerate(ziped[1]):
                # print(logbook)
                logbooks[k] += logbook

        # Jeżeli wartość funkcji celu najlepszego osobnika jest optymalna to kończymy przetwarzanie
        if(all(v == 0 for v in hallOfFame[0].fitness.values)):
            break

        if iterations_wo_improvement >= NGEN / 4:
            print(NGEN / 4, " iterations without improvement: ending...")
            break

        toolbox.migrate(islands)

    # Save results

    pickleOut = open("./out/" + benchmarkName + "_" + str(FREQ) + "_" + str(ISLANDS) +
                     "_" + str(NGEN) + "_" + str(numOfIterations) + "_" + str(algNum) + ".pickle", "wb")
    pickle.dump(utils.result(
        logbooks, bestIndividuals, time.time() - start_time), pickleOut)
    pickleOut.close()


# Jeden logbook to zapis z jednej wyspy
# 0 - stan przed mutacjami i krzyżowaniem, ale po migracji z porzedniej iteracji
# for logbook in logbooks:
#    print(logbook)

print("Hall of fame:", hallOfFame[0], hallOfFame[0].fitness)
