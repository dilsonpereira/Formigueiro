from . import DefaultParameters as dp

def Solve(antCls, numIterations = dp.numIterations, numAnts = dp.numAnts, **kwargs):

    fa = antCls(**kwargs)
    globalBest = None
    for k in range(numIterations):
        ants = [antCls(**kwargs) for _ in range(numAnts)]
        ants[0].makeLeader()

        for ant in ants:
            fa.sharePheromoneStructure(ant)
            ant.constructSolution()
            ant.localSearch()

        iterBest = min(ants, key = lambda a: a.getSolutionValue())
        if globalBest==None or iterBest.getSolutionValue() < globalBest.getSolutionValue():
            globalBest = iterBest 
        print(iterBest.getSolutionValue(), globalBest.getSolutionValue(), max(a.getSolutionValue() for a in ants))

        for ant in set(ants + [iterBest, globalBest]):
            ant.setIterBest(iterBest)
            ant.setGlobalBest(globalBest)
            ant.updatePheromones()

    return globalBest.getSolutionValue(), list(globalBest.getSolutionComponents())

