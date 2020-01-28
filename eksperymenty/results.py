import utils
import pickle
import matplotlib.pyplot as plt
import statistics
import numpy as np
import pprint as pp
import math
import sys


class IslandResults():

    def __init__(self, fit_mins, fit_avgs, fit_stds, fit_maxs, islandNumber):
        self.fit_mins = fit_mins
        self.fit_avgs = fit_avgs
        self.fit_stds = fit_stds
        self.fit_maxs = fit_maxs
        self.islandNumber = islandNumber


class Benchmark():

    def __init__(self):
        self.islands = []

    def addIsland(self, island):
        self.islands.append(island)


num_of_iterations = ["10000"]

num_of_islands = ["5", "10"]
migration_ratio = ["2", "10", "20"]

models = [
    "convection",
    "island"
]

benchmarks = [
    "h1",
    "ackley",
    "himmelblau",
    "schwefel",
    "rastrigin"
]

# nazwa benchmarka
benchmarkName = sys.argv[1]

# Początkowa liczba wysp
islandNum = sys.argv[2]

# Mnożnik migracji
ratio = sys.argv[3]

# max liczba wywołań bez poprawy
max_iterations_wo_improvement = sys.argv[4]

# model
model = sys.argv[5]


pickleIn = open("./out/" + benchmarkName + "_" + islandNum +
                "_" + ratio + "_" + model + ".pickle", "rb")

result = pickle.load(pickleIn)

pickleIn.close()

logbooks = result.logbooks
hallOfFamers = result.hallOfFamers
time = result.time


benchmark = Benchmark()

for islandNumber, logbook in enumerate(logbooks):

    gen = logbook.select("gen")
    fit_mins = logbook.select("min")
    fit_avgs = logbook.select("avg")
    fit_stds = logbook.select("std")
    fit_maxs = logbook.select("max")

    benchmark.addIsland(IslandResults(
        fit_mins, fit_avgs, fit_stds, fit_maxs, islandNumber))


fit_maxs = list(
    map(min, zip(*[island.fit_maxs for island in benchmark.islands])))


maximum = fit_maxs[0]

for index, elem in enumerate(fit_maxs):
    maximum = max(maximum, elem)
    fit_maxs[index] = maximum

pp.pprint(benchmarkName + "_" + islandNum +
          "_" + ratio + "_" + model + " Min: " + str(min(hallOfFamers)))
