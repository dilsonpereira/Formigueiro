import abc
from .CooperativeConstructor import CooperativeConstructor

class Update(abc.ABC):
    @abc.abstractmethod
    def updatePheromones(self):
        pass

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

class TypicalUpdate(Update):
    def updatePheromones(self):
        if self.isLeader():
            self.pheromoneDecay()
            
        if self.canUpdatePheromone():
            for component in self.getSolutionComponents():
                self.setPheromoneValue(component, self.getPheromoneValue(component) + self.getQ()*self.getDeltaTau(component))

    def getDeltaTau(self, component):
        return 1/self.getSolutionValue()

class AllUpdate(TypicalUpdate, CooperativeConstructor):
    def canUpdatePheromone(self):
        return True

class IterBestUpdate(TypicalUpdate, CooperativeConstructor):
    def canUpdatePheromone(self):
        return self == self.getIterBest()

    @abc.abstractmethod
    def getIterBest(self):
        pass

class GlobalBestUpdate(TypicalUpdate, CooperativeConstructor):
    def canUpdatePheromone(self):
        return self == self.getGlobalBest()

    @abc.abstractmethod
    def getGlobalBest(self):
        pass

class ACSUpdate(TypicalUpdate):
    def updatePheromones(self):
        if self.canUpdatePheromone():
            for component in self.getSolutionComponents():
                rho = self.getRho()
                tau = self.getPheromoneValue(component)
                delta = self.getDeltaTau(component)
                Q = self.getQ()
                self.setPheromoneValue(component, (1-rho)*tau + rho*Q*delta)

    @abc.abstractmethod
    def getRho(self):
        pass

class ACSIterBestUpdate(ACSUpdate, IterBestUpdate):
    pass

class MMASUpdate(TypicalUpdate):
    def updatePheromones(self):
        super().updatePheromones()

        if self.isLeader():
            for component in self.getComponents():
                p = self.getPheromoneValue(component)
                p = min(max(p, self.getMinPheromone()), self.getMaxPheromone())
                self.setPheromoneValue(component, p)

    @abc.abstractmethod
    def getMinPheromone(self):
        pass

    @abc.abstractmethod
    def getMaxPheromone(self):
        pass

class MMASIterBestUpdate(MMASUpdate, IterBestUpdate):
    pass

