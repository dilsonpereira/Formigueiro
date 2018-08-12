import abc
import collections

class Pheromone(abc.ABC):
    @abc.abstractmethod
    def getPheromoneValue(self, component):
        pass

    @abc.abstractmethod
    def setPheromoneValue(self, component, value):
        pass

    @abc.abstractmethod
    def sharePheromoneStructure(self, other):
        pass

    @abc.abstractmethod
    def pheromoneDecay(self):
        pass

    @abc.abstractmethod
    def getRho(self):
        pass
    
    @abc.abstractmethod
    def getTau0(self):
        pass

    @abc.abstractmethod
    def getComponents(self):
        pass

class PheromoneDict(Pheromone):
    def __init__(self, **kwargs):
        self.P = collections.defaultdict(self.getCurrentTau)
        self.P['currentTau'] = self.getTau0()

        super().__init__(**kwargs)

    def getPheromoneValue(self, component):
        return self.P[component]

    def setPheromoneValue(self, component, value):
        self.P[component] = value

    def sharePheromoneStructure(self, other):
        other.P = self.P

    def getCurrentTau(self):
        return self.P['currentTau']

    def pheromoneDecay(self):
        for component in self.P:
            self.P[component] *= (1-self.getRho())

    def getComponents(self):
        return (c for c in self.P)
