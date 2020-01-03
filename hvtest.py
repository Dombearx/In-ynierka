import random
from deap import creator, base, tools, algorithms

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

def getFixedValues(values):
    return values

#tools.initIterate

toolbox.register("attr_bool", random.randint, 0, 1)
#toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=ATRR_NUM)



#toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.first, n=ATRR_NUM)

IND_SIZE=10

toolbox = base.Toolbox()
toolbox.register("first", getFixedValues, (10.0, 5.0, 3.5))
toolbox.register("second", getFixedValues, (5.5, 3.0, 2.0))
toolbox.register("third", getFixedValues, (3.0, 10.0, 5.5))
toolbox.register("fourth", getFixedValues, (3.0, 10.0, 6.0))

toolbox.register("individual", tools.initIterate, creator.Individual,
                 toolbox.first)

ind1 = toolbox.individual()
print(ind1)


print(tools.hypervolume(ind1))

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

'''
def evalOneMax(individual):
    return sum(individual),

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=300)

NGEN=40
for gen in range(NGEN):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    population = toolbox.select(offspring, k=len(population))
top10 = tools.selBest(population, k=10)
'''