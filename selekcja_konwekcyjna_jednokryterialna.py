import random
from deap import creator, base, tools, algorithms, benchmarks
import migration as mig
import time
import utils
import numpy
import pickle

# Każdy osobnik - individual ma liczbę atrybutó3 = len(weights), jeżeli -1 - minimaliazcja, jeżeli 1 - maksymalizacja
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Atrybut typu bool - 0 albo 1
toolbox.register("attr_float", random.uniform, -100, 100)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_float, 2)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Funkcja celu - suma wartości atrybutów

benchmarkName = "h1"


def evalOneMax(individual):
    return sum(benchmarks.h1(individual)),


toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

toolbox.register("map", map)

# Początkowa liczba wysp
ISLANDS = 10

# dodanie migracji - mig.migSel to funkcja migracji selekcji konwekcyjnej
toolbox.register("migrate", mig.migSel, numOfIslands=ISLANDS)

stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)

# liczba generacji, jak często następuje migracja (co ile zmian całej populacji)
NGEN, FREQ = 200, 1

CXPB, MUTPB = 0.5, 0.2
# ngen = FREQ oznacza ile wykonań algorytmu się wykona przy jednym uruchomieniu funkcji
toolbox.register("algorithm", algorithms.eaSimple, toolbox=toolbox,
                 stats=stats, cxpb=CXPB, mutpb=MUTPB, ngen=FREQ, verbose=False)

# utworzenie populacji początkowej
numOfIterations = 10
benchmarkResults = []


for _ in range(0, numOfIterations):
    logbooks = []
    # Zapisuje n najlepszych osobników (tutaj n = 1)
    hallOfFame = tools.HallOfFame(1)
    start_time = time.time()
    islands = [toolbox.population(n=300) for i in range(ISLANDS)]
    for i in range(0, NGEN, FREQ):

        results = toolbox.map(toolbox.algorithm, islands)

        ziped = list(map(list, zip(*results)))

        islands = ziped[0]

        # Jeżeli znajdzie lepszego osobnika niż najlepszy obecnie, to nadpisuje go
        for island in islands:
            hallOfFame.update(island)

        if i == 0:
            for logbook in ziped[1]:
                logbooks.append(logbook)
        else:
            for k, logbook in enumerate(ziped[1]):
                logbooks[k] += logbook

        # Jeżeli wartość funkcji celu najlepszego osobnika jest optymalna to kończymy przetwarzanie
        if(hallOfFame[0].fitness.values[0] == 100):
            break

        toolbox.migrate(islands)

    # Save results
    benchmarkResults.append(utils.result(logbooks, hallOfFame))

'''
# Jeden logbook to zapis z jednej wyspy
# 0 - stan przed mutacjami i krzyżowaniem, ale po migracji z porzedniej iteracji
for logbook in logbooks:
    print(logbook)

print("Hall of fame:", hallOfFame[0], hallOfFame[0].fitness)
'''

pickleOut = open("selKonw_" + benchmarkName + ".pickle", "wb")
pickle.dump(benchmarkResults, pickleOut)
pickleOut.close()
