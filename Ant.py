import abc
from .Pheromone import *
from .Decision import *
from .Update import *
from . import DefaultParameters as dp

class Ant(abc.ABC):
    #@abc.abstractmethod
    #def getPheromoneValue(self, component):
    #    pass
    
    #@abc.abstractmethod
    #def setPheromoneValue(self, component, value):
    #    pass

    #@abc.abstractmethod
    #def getHeuristicValue(self, component):
    #    pass

    #@abc.abstractmethod
    #def getComponentCost(self, component):
    #    pass

    #@abc.abstractmethod
    #def getAlpha(self):
    #    pass

    #@abc.abstractmethod
    #def getBeta(self):
    #    pass

    #@abc.abstractmethod
    #def getRho(self):
    #    pass

    #@abc.abstractmethod
    #def getQ(self):
    #    pass

    #@abc.abstractmethod
    #def getTau0(self):
    #    pass

    #@abc.abstractmethod
    #def makeDecision(self, components):
    #    pass
    
    @abc.abstractmethod
    def constructSolution(self):
        pass

    #@abc.abstractmethod
    #def updatePheromones(self):
    #    pass

    #@abc.abstractmethod
    #def canUpdatePheromones(self):
    #    pass

    #@abc.abstractmethod
    def localSearch(self):
        pass

    @abc.abstractmethod
    def setGlobalBest(self, globalBest):
        pass

    @abc.abstractmethod
    def setIterBest(self, iterBest):
        pass

    @abc.abstractmethod
    def getGlobalBest(self):
        pass

    @abc.abstractmethod
    def getIterBest(self):
        pass

    @abc.abstractmethod
    def getSolutionValue(self):
        pass

    #@abc.abstractmethod
    #def getSolutionComponents(self):
    #    pass

    #@abc.abstractmethod
    #def sharePheromoneStructure(self, other):
    #    pass

    #@abc.abstractmethod
    #def getDeltaTau(self, component):
    #    pass

    @abc.abstractmethod
    def makeLeader(self):
        pass

    #@abc.abstractmethod
    #def isLeader(self):
    #    pass

    #@abc.abstractmethod
    #def pheromoneDecay(self):
    #    pass

class ConcreteAnt(Ant, PheromoneDict):
    def __init__(self, alpha = dp.alpha, beta = dp.beta, rho = dp.rho, Q = dp.Q, tau0 = dp.tau0, **kwargs):
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.tau0 = tau0
        self.iterBest = None
        self.globalBest = None
        self.leader = False

        super().__init__(**kwargs)

    def getAlpha(self):
        return self.alpha

    def getBeta(self):
        return self.beta

    def getRho(self):
        return self.rho

    def getQ(self):
        return self.Q

    def getTau0(self):
        return self.tau0

    def setIterBest(self, iterBest):
        self.iterBest = iterBest

    def setGlobalBest(self, globalBest):
        self.globalBest = globalBest

    def getIterBest(self):
        return self.iterBest

    def getGlobalBest(self):
        return self.globalBest

    def isLeader(self):
        return self.leader

    def makeLeader(self):
        self.leader = True

    #@abc.abstractmethod
    #def getCurrentTau(self):
    #    pass

    def getSolutionValue(self):
        return sum(self.getComponentCost(c) for c in self.getSolutionComponents())

class AS_Ant(ConcreteAnt, AS_Decision, AllUpdate):
    pass

class ACS_Ant(ConcreteAnt, ACS_Decision, ACSIterBestUpdate):
    def __init__(self, phi = dp.phi, q0 = dp.q0, **kwargs):
        self.q0 = q0
        self.phi = phi

        super().__init__(**kwargs)

    def getq0(self):
        return self.q0

    def getPhi(self):
        return self.phi

class MMAS_Ant(ConcreteAnt, MMAS_Decision, MMASIterBestUpdate):
    def __init__(self, minPheromone = dp.minPheromone, maxPheromone = dp.maxPheromone, **kwargs):
        self.minPheromone = minPheromone
        self.maxPheromone = maxPheromone

        super().__init__(**kwargs)

    def getMinPheromone(self):
        return self.minPheromone

    def getMaxPheromone(self):
        return self.maxPheromone

