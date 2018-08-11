import abc
from .CooperativeConstructor import CooperativeConstructor

class Update(abc.ABC):
    def updatePheromones(self):
        if self.isLeader():
            self.pheromoneDecay()

        if self.canUpdatePheromone():
            for component in self.getSolutionComponents():
                self.setPheromoneValue(component, self.getPheromoneValue(component) + self.getDeltaTau(component))

    @abc.abstractmethod
    def setPheromoneValue(self, component, value):
        pass

    @abc.abstractmethod
    def getPheromoneValue(self):
        pass

    @abc.abstractmethod
    def getSolutionValue(self):
        pass

    @abc.abstractmethod
    def getSolutionComponents(self):
        pass

    @abc.abstractmethod
    def getQ(self):
        pass

    @abc.abstractmethod
    def getDeltaTau(self, component):
        pass

    @abc.abstractmethod
    def isLeader(self):
        pass

    @abc.abstractmethod
    def pheromoneDecay(self):
        pass

    @abc.abstractmethod
    def canUpdatePheromone(self):
        pass

class AllUpdate(Update, CooperativeConstructor):
    def canUpdatePheromone(self):
        return True

    def getDeltaTau(self, component):
        return self.getQ()/self.getSolutionValue()

class IterBestUpdate(Update, CooperativeConstructor):
    def canUpdatePheromone(self):
        return self == self.getIterBest()

    def getDeltaTau(self, component):
        return self.getQ()/self.getIterBest().getSolutionValue()

    @abc.abstractmethod
    def getIterBest(self):
        pass

class GlobalBestUpdate(Update, CooperativeConstructor):
    def canUpdatePheromone(self):
        return self == self.getGlobalBest()

    @abc.abstractmethod
    def getGlobalBest(self):
        pass

    def getDeltaTau(self, component):
        return self.getQ()/self.getGlobalBest().getSolutionValue()

class MMASIterBestUpdate(IterBestUpdate):
    def getDeltaTau(self, component):
        return self.getRho()*self.getQ()/self.getIterBest().getSolutionValue()

    @abc.abstractmethod
    def getRho(self):
        pass

    def updatePheromones(self):
        super().updatePheromones()

        if self.canUpdatePheromone():
            for component in self.getSolutionComponents():
                p = self.getPheromoneValue(component)
                p = max(p, self.getMinPheromone())
                p = min(p, self.getMaxPheromone())
                self.setPheromoneValue(component, p)

    @abc.abstractmethod
    def getMinPheromone(self):
        pass

    @abc.abstractmethod
    def getMaxPheromone(self):
        pass

