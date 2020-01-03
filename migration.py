from __future__ import division


def sortByFitness(wholePopulation):
    wholePopulation.sort(key=lambda x: x.fitness, reverse=False)

def getMinFitness(wholePopulation):

    minFit = wholePopulation[0].fitness

    for individual in wholePopulation[1:]:
        if individual.fitness < minFit:
            minFit = individual.fitness

    return minFit

def getMaxFitness(wholePopulation):

    maxFit = wholePopulation[0].fitness

    for individual in wholePopulation[1:]:
        if individual.fitness > maxFit:
            maxFit = individual.fitness

    return maxFit

def migSel(populations, numOfIslands):
    wholePopulation = []

    print("before:")
    for population in populations:
        print(getMaxFitness(population))
        wholePopulation += population

    islandSize = int(len(wholePopulation) / numOfIslands)

    newIslands = []

    sortByFitness(wholePopulation)

    
    for i in range(0, len(wholePopulation), islandSize):
        newIslands.append(wholePopulation[i:i + islandSize])
        lastIndex = i + islandSize

    newIslands[-1] += wholePopulation[lastIndex:]

    for i, newIs in enumerate(newIslands):
        if(i >= len(populations)):
            populations.append(newIs)
        else:
            populations[i] = newIs

    if(len(populations) > len(newIslands)):
        del populations[len(newIslands):]

    #populations = newIslands[:]


    print("after:")
    for population in populations:
        print(getMaxFitness(population))


def migRing(populations, k, selection, replacement=None, migarray=None):
    """Perform a ring migration between the *populations*. The migration first
    select *k* emigrants from each population using the specified *selection*
    operator and then replace *k* individuals from the associated population
    in the *migarray* by the emigrants. If no *replacement* operator is
    specified, the immigrants will replace the emigrants of the population,
    otherwise, the immigrants will replace the individuals selected by the
    *replacement* operator. The migration array, if provided, shall contain
    each population's index once and only once. If no migration array is
    provided, it defaults to a serial ring migration (1 -- 2 -- ... -- n --
    1). Selection and replacement function are called using the signature
    ``selection(populations[i], k)`` and ``replacement(populations[i], k)``.
    It is important to note that the replacement strategy must select *k*
    **different** individuals. For example, using a traditional tournament for
    replacement strategy will thus give undesirable effects, two individuals
    will most likely try to enter the same slot.
    :param populations: A list of (sub-)populations on which to operate
                        migration.
    :param k: The number of individuals to migrate.
    :param selection: The function to use for selection.
    :param replacement: The function to use to select which individuals will
                        be replaced. If :obj:`None` (default) the individuals
                        that leave the population are directly replaced.
    :param migarray: A list of indices indicating where the individuals from
                     a particular position in the list goes. This defaults
                     to a ring migration.
    """
    nbr_demes = len(populations)
    if migarray is None:
        migarray = range(1, nbr_demes) + [0]

    immigrants = [[] for i in range(nbr_demes)]
    emigrants = [[] for i in range(nbr_demes)]

    for from_deme in range(nbr_demes):
        emigrants[from_deme].extend(selection(populations[from_deme], k))
        if replacement is None:
            # If no replacement strategy is selected, replace those who migrate
            immigrants[from_deme] = emigrants[from_deme]
        else:
            # Else select those who will be replaced
            immigrants[from_deme].extend(replacement(populations[from_deme], k))

    for from_deme, to_deme in enumerate(migarray):
        for i, immigrant in enumerate(immigrants[to_deme]):
            indx = populations[to_deme].index(immigrant)
            populations[to_deme][indx] = emigrants[from_deme][i]

__all__ = ['migRing', 'migSel']