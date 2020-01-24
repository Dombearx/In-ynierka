import utils
import pickle
import matplotlib.pyplot as plt
import statistics
import numpy as np
import pprint as pp
import math


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

benchmarkName = benchmarks[3]
islandNum = num_of_islands[0]
ratio = migration_ratio[0]
model = models[0]

pickleIn = open("./out/" + benchmarkName + "_" + islandNum +
                "_" + ratio + "_" + model + ".pickle", "rb")

result = pickle.load(pickleIn)

pickleIn.close()

logbooks = result.logbooks
hallOfFamers = result.hallOfFamers
time = result.time


fig, axs = plt.subplots(math.ceil(int(num_of_islands[0]) / 2), 2)

benchmark = Benchmark()

for islandNumber, logbook in enumerate(logbooks):

    gen = logbook.select("gen")
    fit_mins = logbook.select("min")
    fit_avgs = logbook.select("avg")
    fit_stds = logbook.select("std")
    fit_maxs = logbook.select("max")

    benchmark.addIsland(IslandResults(
        fit_mins, fit_avgs, fit_stds, fit_maxs, islandNumber))


benchmarkName = benchmarks[3]
islandNum = num_of_islands[0]
ratio = migration_ratio[0]
model = models[0]
fig.tight_layout()
fig.suptitle("Benchmark: " + benchmarks[3] + " Number of islands: " +
             islandNum + " Migration every " + str(int(ratio)*100) + " iterations Model: " + model)
for island in benchmark.islands:

    # Wykres liniowy
    #fit_mins = hallOfFamers
    islandNumber = 0
    x = int(island.islandNumber / 2)
    y = int(island.islandNumber % 2)

    line1 = axs[x, y].plot([_ for _ in range(0, len(island.fit_mins))],
                           island.fit_mins, "b-", label="Minimum Fitness")
    # line2 = axs[x, y].plot([_ for _ in range(0, len(fit_mins))],
    #                       fit_avgs, "r-", label="Average Fitness")
    axs[x, y].set_xlabel("Generation")
    #axs[x, y].set_yscale('log')
    axs[x, y].set_ylabel("Fitness", color="b")
    axs[x, y].set_title("ISLAND " + str(island.islandNumber))
    for tl in axs[x, y].get_yticklabels():
        tl.set_color("b")

        lns = line1  # + line2
        labs = [l.get_label() for l in lns]
        axs[x, y].legend(lns, labs, loc="center right")

fit_mins = hallOfFamers
x = int(2)
y = int(1)

line1 = axs[x, y].plot([_ for _ in range(0, len(fit_mins))],
                       fit_mins, "b-", label="Minimum Fitness")
# line2 = axs[x, y].plot([_ for _ in range(0, len(fit_mins))],
#                       fit_avgs, "r-", label="Average Fitness")
axs[x, y].set_xlabel("Generation")
#axs[x, y].set_yscale('log')
axs[x, y].set_ylabel("Fitness", color="b")
axs[x, y].set_title("GLOBAL")
for tl in axs[x, y].get_yticklabels():
    tl.set_color("b")

    lns = line1  # + line2
    labs = [l.get_label() for l in lns]
    axs[x, y].legend(lns, labs, loc="center right")


plt.show()

'''
# Wykres słupkowy

fig, ax1 = plt.subplots()

# Tylko ostatnie pokolenie
# fit_mins = [fit_mins[-FREQ - 1], ]
# fit_avgs = [fit_avgs[-FREQ - 1], ]
# fit_maxs = [fit_maxs[-FREQ - 1], ]

for islandNumber, fit_mins in enumerate(islandsAvgMin):
    ind = np.arange(len(islandsAvgMin))  # the x locations for the groups
    width = 0.3

    bar1 = ax1.bar(ind - width, fit_mins, width, label="Minimum Fitness")
    # bar2 = ax1.bar(ind, islands_avg, width, label="Average Fitness")
    # bar3 = ax1.bar(ind + width, islands_max, width, label="Maximum Fitness")

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax1.set_ylabel("Fitness")
    ax1.set_xlabel("Islands")
    ax1.set_title('Islands ' + benchmarkName)
    ax1.set_xticks(ind)
    ax1.set_yscale('log')
    ax1.set_xticklabels(("ISLAND " + str(i) for i in range(0, ISLANDS)))
    ax1.legend()

    # bars = bar1 + bar2 + bar3

    plt.show()
'''
