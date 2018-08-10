from . import DefaultParameters as dp

def Solve(antCls, numIterations = dp.numIterations, numAnts = dp.numAnts, **kwargs):
    ants = [antCls(**kwargs) for _ in range(numAnts)]

    for ant in ants[1:]:
        ants[0].sharePheromoneStructure(ant)

    globalBest = None
    for k in range(numIterations):
        for ant in ants:
            ant.constructSolution()
            ant.localSearch()

    iterBest = min(ants, key = lambda a: a.getSolutionValue())
    globalBest = iterBest if not globalBest or ib.getSolutionValue() < globalBest.getSolutionValue() else globalBest

    for ant in set(ants + [iterBest, globalBest]):
        ant.setIterBest(iterBest)
        ant.setGlobalBest(globalBest)
        ant.UpdatePheromones()
