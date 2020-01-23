import sys


class IslandResults():

    def __init__(self, min, islandNumber):
        self.min = min

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

    def setIslandData(self, min, islandNumber):

        self.benchmarkAverangeMin[islandNumber].append(min)

    def calcAvgs(self):
        self.islands = []

        for island in range(0, self.numOfIslands):

            avgMin = [sum(x)/len(x)
                      for x in zip(*self.benchmarkAverangeMin[island])]

            self.islands.append(IslandResults(
                avgMin, island))


for arg in sys.argv:
    print(arg)

values = (0, 0, 0, 0, 0, 0, 0)

i1 = [10, 20, 30, 40, 50, 100, 100]
i2 = [12, 24, 36, 48, 60]

b = Benchmark(1)

b.setIslandData(i1, 0)
b.setIslandData(i2, 0)

b.calcAvgs()

for island in b.islands:
    print(island.min)

print(all(v == 0 for v in values))

for i in range(0, 10, 2):
    print(i)
