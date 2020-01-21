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
# LICZBA EWOLUCJI MIĘDZY MIGRACJAMI (częstotliowść migracji) - argv[1]
# LICZBA WYSP - argv[2]
# LICZBA EWOLUCJI - argv[3]
# LICZBA POWTÓRZEŃ ALGORYTMU - argv[4]

# Nazwa pliku - nazwa benchmarka
benchmarkName = sys.argv[0]

# jak często następuje migracja (co ile zmian całej populacji)
FREQ = int(sys.argv[1])

# Początkowa liczba wysp
ISLANDS = int(sys.argv[2])

# liczba generacji
NGEN = int(sys.argv[3])

# Liczba powtórzeń algorytmu
numOfIterations = int(sys.argv[4])

# Dla każdej wyspy
POPULATION_SIZE = 100

# Każdy osobnik - individual ma liczbę atrybutów = len(weights), jeżeli -1 - minimaliazcja, jeżeli 1 - maksymalizacja
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()


ATTRIBUTES = 20
# Atrybut typu bool - 0 albo 1
toolbox.register("attr_float", random.uniform, -500, 500)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_float, ATTRIBUTES)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Funkcja celu


def evalOneMax(individual):
    return sum(benchmarks.schwefel(individual)),


toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

toolbox.register("map", map)


# dodanie migracji - mig.migSel to funkcja migracji selekcji konwekcyjnej
toolbox.register("migrate", mig.migSel, numOfIslands=ISLANDS)

stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)


CXPB, MUTPB = 0.5, 0.2
# ngen = FREQ oznacza ile wykonań algorytmu się wykona przy jednym uruchomieniu funkcji
toolbox.register("algorithm", algorithms.eaSimple, toolbox=toolbox,
                 stats=stats, cxpb=CXPB, mutpb=MUTPB, ngen=FREQ, verbose=False)

benchmarkResults = []

for algNum in range(0, numOfIterations):
    print("Iteracja algorytmu:", algNum + 1)
    logbooks = []
    # Zapisuje n najlepszych osobników (tutaj n = 1)
    hallOfFame = tools.HallOfFame(1)
    bestIndividuals = []
    start_time = time.time()
    islands = [toolbox.population(n=POPULATION_SIZE) for i in range(ISLANDS)]
    for i in range(0, NGEN, FREQ):
        print("Postęp iteracji:", (i / NGEN) * 100, "%")
        results = toolbox.map(toolbox.algorithm, islands)

        ziped = list(map(list, zip(*results)))

        islands = ziped[0]

        # Jeżeli znajdzie lepszego osobnika niż najlepszy obecnie, to nadpisuje go
        for island in islands:
            hallOfFame.update(island)

        bestIndividuals.append(hallOfFame)

        if i == 0:
            for logbook in ziped[1]:
                logbooks.append(logbook)
        else:
            for k, logbook in enumerate(ziped[1]):
                logbooks[k] += logbook

        # Jeżeli wartość funkcji celu najlepszego osobnika jest optymalna to kończymy przetwarzanie
        if(all(v == 0 for v in hallOfFame[0].fitness.values)):
            break

        toolbox.migrate(islands)

    # Save results
    benchmarkResults.append(utils.result(
        logbooks, bestIndividuals, time.time() - start_time))


# Jeden logbook to zapis z jednej wyspy
# 0 - stan przed mutacjami i krzyżowaniem, ale po migracji z porzedniej iteracji
# for logbook in logbooks:
#    print(logbook)

print("Hall of fame:", hallOfFame[0], hallOfFame[0].fitness)

pickleOut = open("./out/" + benchmarkName + "_" + str(FREQ) + "_" + str(ISLANDS) +
                 "_" + str(NGEN) + "_" + str(numOfIterations) + ".pickle", "wb")
pickle.dump(benchmarkResults, pickleOut)
pickleOut.close()
