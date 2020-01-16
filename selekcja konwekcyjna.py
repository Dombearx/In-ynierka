import random
from deap import creator, base, tools, algorithms
import migration as mig
import numpy

# Każdy osobnik - individual ma liczbę atrybutów = len(weights), jeżeli -1 - minimaliazcja, jeżeli 1 - maksymalizacja
creator.create("FitnessMax", base.Fitness, weights=(1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Atrybut typu bool - 0 albo 1
toolbox.register("attr_float", random.uniform, 0, 1)
toolbox.register("individual", tools.initRepeat,
                 creator.Individual, toolbox.attr_float, n=100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def lenFromMid(individual):
    average = 0
    for v in individual:
        average += abs(0.5 - v)

    return average / len(individual)
    # Funkcja celu - suma wartości atrybutów


def evalOneMax(individual):
    return (sum(individual), lenFromMid(individual))


toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selNSGA2)

toolbox.register("map", map)

stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)

# Początkowa liczba wysp
ISLANDS = 10

# Domyślna funkcja migracji - pierścień
# toolbox.register("migrate", tools.migRing, k=15, selection=tools.selBest)

# dodanie migracji - mig.migSel to funkcja migracji selekcji konwekcyjnej
# toolbox.register("migrate", mig.migSel,
#                 numOfIslands=ISLANDS)

# dodanie migracji - mig.migSelOneFrontOneIsland - kazdy front pareto na innej wyspie
toolbox.register("migrate", mig.migSelOneFrontOneIsland)


# liczba generacji, jak często następuje migracja (co ile zmian całej populacji)
NGEN, FREQ = 20, 1

# ngen = FREQ oznacza ile wykonań algorytmu się wykona przy jednym uruchomieniu funkcji
toolbox.register("algorithm", algorithms.eaSimple, toolbox=toolbox,
                 stats=stats, cxpb=0.5, mutpb=0.2, ngen=FREQ, verbose=False)

# toolbox.register("algorithm", algorithms.varAnd, toolbox=toolbox,
#                 cxpb=0.5, mutpb=0.2)

hallOfFame = tools.HallOfFame(1)
logbooks = []

# utworzenie populacji początkowej
islands = [toolbox.population(n=20) for i in range(ISLANDS)]
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
            if k >= len(logbooks):
                logbooks.append(logbook)
            logbooks[k] += logbook

    # Jeżeli wartość funkcji celu najlepszego osobnika jest optymalna to kończymy przetwarzanie
    if(hallOfFame[0].fitness.values[0] == 100):
        break

    toolbox.migrate(islands)

for logbook in logbooks:
    print(logbook)

print("HallOfFamer:", hallOfFame[0].fitness)
