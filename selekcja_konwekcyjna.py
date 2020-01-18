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


# Funkcja celu - suma wartości atrybutów, odległość każdego atrybutu od wartości 0.5
def evalOneMax(individual):
    return (sum(individual), lenFromMid(individual))


toolbox.register("evaluate", evalOneMax)

# test
BOUND_LOW, BOUND_UP = 0.0, 1.0
toolbox.register("mate", tools.cxSimulatedBinaryBounded,
                 low=BOUND_LOW, up=BOUND_UP, eta=30.0)
toolbox.register("mutate", tools.mutPolynomialBounded,
                 low=BOUND_LOW, up=BOUND_UP, eta=20.0, indpb=0.05)
toolbox.register("select", tools.selNSGA2)

toolbox.register("map", map)

stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean, axis=0)
stats.register("std", numpy.std, axis=0)
stats.register("min", numpy.min, axis=0)
stats.register("max", numpy.max, axis=0)

# Początkowa liczba wysp
ISLANDS = 10


# dodanie migracji - mig.migSelOneFrontOneIsland - kazdy front pareto na innej wyspie
toolbox.register("migrate", mig.migSelOneFrontOneIsland)


# liczba generacji, jak często następuje migracja (co ile zmian całej populacji)
NGEN, FREQ = 40, 1

# ngen = FREQ oznacza ile wykonań algorytmu się wykona przy jednym uruchomieniu funkcji
toolbox.register("algorithm", algorithms.eaSimple, toolbox=toolbox,
                 stats=stats, cxpb=0.5, mutpb=0.2, ngen=FREQ, verbose=False)


hallOfFame = tools.ParetoFront()
logbooks = []

# utworzenie populacji początkowej
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
            if k >= len(logbooks):
                logbooks.append(logbook)
            logbooks[k] += logbook

    # Jeżeli wartość funkcji celu najlepszego osobnika jest optymalna to kończymy przetwarzanie
    if(hallOfFame[0].fitness.values[0] == 100):
        break

    toolbox.migrate(islands)

for logbook in logbooks:
    print(logbook)

print("Hall of fame:")
for individual in hallOfFame:
    print(individual.fitness)
