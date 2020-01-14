import random
from deap import creator, base, tools, algorithms
import migration as mig
import time
import utils
import numpy

# Każdy osobnik - individual ma liczbę atrybutó3 = len(weights), jeżeli -1 - minimaliazcja, jeżeli 1 - maksymalizacja
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Atrybut typu bool - 0 albo 1
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_bool, 100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Funkcja celu - suma wartości atrybutów


def evalOneMax(individual):
    return sum(individual),


toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

toolbox.register("map", map)

# Początkowa liczba wysp
ISLANDS = 10

# Domyślna funkcja migracji - pierścień
toolbox.register("migrate", tools.migRing, k=15, selection=tools.selBest)

# dodanie migracji - mig.migSel to funkcja migracji selekcji konwekcyjnej
#toolbox.register("migrate", mig.migSel, numOfIslands=ISLANDS)

stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)

logbook = tools.Logbook()
logbook.header = "gen", "evals", "std", "min", "avg", "max"


# liczba generacji, jak często następuje migracja (co ile zmian całej populacji)
NGEN, FREQ = 10, 2

CXPB, MUTPB = 0.5, 0.2
# ngen = FREQ oznacza ile wykonań algorytmu się wykona przy jednym uruchomieniu funkcji
toolbox.register("algorithm", algorithms.eaSimple, toolbox=toolbox,
                 stats=stats, cxpb=CXPB, mutpb=MUTPB, ngen=FREQ, verbose=False)

# toolbox.register("algorithm", algorithms.varAnd, toolbox=toolbox,
#                 cxpb=0.5, mutpb=0.2)

# utworzenie populacji początkowej
res = []
numOfIterations = 1
logbooks = []


for _ in range(0, numOfIterations):
    start_time = time.time()
    islands = [toolbox.population(n=300) for i in range(ISLANDS)]
    for i in range(0, NGEN, FREQ):

        results = toolbox.map(toolbox.algorithm, islands)

        #islands = [island for island, logbook in results]
        #logbooks = [logbook for island, logbook in results]

        ziped = list(map(list, zip(*results)))

        islands = ziped[0]

        if i == 0:
            for logbook in ziped[1]:
                logbooks.append(logbook)
        else:
            for i, logbook in enumerate(ziped[1]):
                logbooks[i].append(logbook)

        toolbox.migrate(islands)

for logbook in logbooks:
    print(logbook)
