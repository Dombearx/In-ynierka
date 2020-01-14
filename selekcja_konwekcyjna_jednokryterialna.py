import random
from deap import creator, base, tools, algorithms
import migration as mig
import time
import utils

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
#toolbox.register("migrate", tools.migRing, k=15, selection=tools.selBest)

# dodanie migracji - mig.migSel to funkcja migracji selekcji konwekcyjnej
toolbox.register("migrate", mig.migSel, numOfIslands=ISLANDS)


# liczba generacji, jak często następuje migracja (co ile zmian całej populacji)
NGEN, FREQ = 200, 10

CXPB, MUTPB = 0.5, 0.2
# ngen = FREQ oznacza ile wykonań algorytmu się wykona przy jednym uruchomieniu funkcji
toolbox.register("algorithm", algorithms.eaSimple, toolbox=toolbox,
                 stats=stats, cxpb=CXPB, mutpb=MUTPB, ngen=FREQ, verbose=False)

# toolbox.register("algorithm", algorithms.varAnd, toolbox=toolbox,
#                 cxpb=0.5, mutpb=0.2)

# utworzenie populacji początkowej

res = []
numOfIterations = 1
shouldEnd = False
for _ in range(0, numOfIterations):
    start_time = time.time()
    islands = [toolbox.population(n=300) for i in range(ISLANDS)]
    for i in range(0, NGEN, FREQ):

        results = toolbox.map(toolbox.algorithm, islands)

        islands = [island for island, logbook in results]

        toolbox.migrate(islands)

        print("Islands: ")
        for island in islands:
            print("Min fittnes: ", mig.getMinFitness(island))
            print("Mean fittnes: ", mig.getMeanFitness(island))
            print("Max fittnes: ", mig.getMaxFitness(island))
            print("---------------------------")
            if mig.getMaxFitness(island).values[0] == 100:
                print("Optimal individual in", i, "generations")
                res.append((i, time.time() - start_time))
                shouldEnd = True
                break

        if shouldEnd == True:
            break


for r in res:
    print(r)
utils.makelogFile(res, "konw.txt")
