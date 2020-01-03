import random
from deap import creator, base, tools, algorithms
import migration as mig

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    return sum(individual),

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

toolbox.register("map", map)
ISLANDS = 10
#toolbox.register("migrate", tools.migRing, k=15, selection=tools.selBest)
toolbox.register("migrate", mig.migSel, numOfIslands=ISLANDS - 5)
NGEN, FREQ = 2, 1
toolbox.register("algorithm",algorithms.eaSimple, toolbox=toolbox, cxpb=0.5, mutpb=0.2, ngen=FREQ, verbose=False)
islands = [toolbox.population(n=20) for i in range(ISLANDS)]
for i in range(0,NGEN,FREQ):
    results = toolbox.map(toolbox.algorithm, islands)
    islands = [island for island, logbook in results]

    print("in main before: ")
    for island in islands:
        print(mig.getMaxFitness(island))

    toolbox.migrate(islands)

    print("in main: ")
    for island in islands:
        print(mig.getMaxFitness(island))

    print("--------------")

