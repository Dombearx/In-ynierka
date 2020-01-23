import utils
import pickle
import matplotlib.pyplot as plt
import statistics
import numpy as np
import pprint as pp
import math


class IslandResults():

    def __init__(self, min, avg, std, max, islandNumber):
        self.min = min
        self.avg = avg
        self.std = std
        self.max = max
        self.islandNumber = islandNumber


class Benchmark():

    def __init__(self, numOfIslands):
        self.benchmarkAverangeMax = []
        self.benchmarkAverangeMin = []
        self.benchmarkAverangeAvg = []
        self.benchmarkAverangeStd = []
        self.numOfIslands = numOfIslands

        for _ in range(0, numOfIslands):
            self.benchmarkAverangeMax.append([])
            self.benchmarkAverangeMin.append([])
            self.benchmarkAverangeAvg.append([])
            self.benchmarkAverangeStd.append([])

    def setIslandData(self, min, avg, std, max, islandNumber):

        self.benchmarkAverangeMax[islandNumber].append(max)
        self.benchmarkAverangeMin[islandNumber].append(min)
        self.benchmarkAverangeAvg[islandNumber].append(avg)
        self.benchmarkAverangeStd[islandNumber].append(std)

    def calcAvgs(self):
        self.islands = []

        for island in range(0, self.numOfIslands):

            avgMax = [sum(x)/len(x)
                      for x in zip(*self.benchmarkAverangeMax[island])]

            avgAvg = [sum(x)/len(x)
                      for x in zip(*self.benchmarkAverangeAvg[island])]

            avgStd = [sum(x)/len(x)
                      for x in zip(*self.benchmarkAverangeStd[island])]

            avgMin = [sum(x)/len(x)
                      for x in zip(*self.benchmarkAverangeMin[island])]

            self.islands.append(IslandResults(
                avgMin, avgAvg, avgStd, avgMax, island))


benchmarkName = "sel_himmelblau.py"
FREQ = 50
ISLANDS = 5
NGEN = 20000
numOfIterations = 1


name = "sel_himmelblau.py_200_5_200000_2_0"

# pickleIn = open("./out/" + benchmarkName + "_" + str(FREQ) + "_" + str(ISLANDS) +
#                "_" + str(NGEN) + "_" + str(numOfIterations) + ".pickle", "rb")

pickleIn = open("./out/" + name + ".pickle", "rb")
result = pickle.load(pickleIn)

pickleIn.close()

logbooks = result.logbooks
hallOfFamers = result.hallOfFamers
time = result.time

islands_max = []
islands_min = []
islands_avg = []
islands_std = []

fig, axs = plt.subplots(int(ISLANDS / 2), 2)

benchmark = Benchmark(ISLANDS)


# for benchmarkResult in benchmarkResults:
'''
for islandNumber, logbook in enumerate(logbooks):

    gen = logbook.select("gen")
    fit_mins = logbook.select("min")
    fit_avgs = logbook.select("avg")
    fit_stds = logbook.select("std")
    fit_maxs = logbook.select("max")

    # islands_max.append(max(fit_maxs))
    # islands_min.append(min(fit_mins))
    # islands_avg.append(statistics.mean(fit_avgs))
    # islands_avg.append(statistics.mean(fit_stds))

    # benchmark.setIslandData(
    #    fit_mins, fit_avgs, fit_stds, fit_maxs, islandNumber)

benchmark.calcAvgs()

islandsAvgMax = benchmark.avgMax
islandsAvgAvg = benchmark.avgAvg
islandsAvgStd = benchmark.avgStd
islandsAvgMin = benchmark.avgMin
'''

# for islandNumber, hallOfFamers in enumerate(hallOfFamers):

# Wykres liniowy
fit_mins = hallOfFamers
islandNumber = 0
x = int(islandNumber / 2)
y = int(islandNumber % 2)

line1 = axs[x, y].plot([_ for _ in range(0, len(fit_mins))],
                       fit_mins, "b-", label="Minimum Fitness")
# line2 = axs[x, y].plot([_ for _ in range(0, len(fit_mins))],
#                       fit_avgs, "r-", label="Average Fitness")
axs[x, y].set_xlabel("Generation")
axs[x, y].set_yscale('log')
axs[x, y].set_ylabel("Fitness", color="b")
axs[x, y].set_title("ISLAND " + str(islandNumber))
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
