def sortByFitness(wholePopulation):
    wholePopulation.sort(key=lambda x: x.fitness, reverse=False)


class t:

    def __init__(self, f):
        self.fitness = f


tab = [
    t(10),
    t(20),
    t(1),
    t(13),
    t(26)
]


sortByFitness(tab)

for t in tab:
    print(t.fitness)
