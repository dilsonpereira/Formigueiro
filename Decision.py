import abc
from . import DefaultParameters as dp

class Decision(abc.ABC):
    @abc.abstractmethod
    def makeDecision(self, components):
        pass

    @abc.abstractmethod 
    def getAlpha(self):
        pass

    @abc.abstractmethod
    def getBeta(self):
        pass
    
    @abc.abstractmethod
    def getPheromoneValue(self, component):
        pass

    @abc.abstractmethod
    def getHeuristicValue(self, component):
        pass

    @abc.abstractmethod
    def getComponentCost(self, component):
        pass

    def getNumerator(self, component):
        return self.getPheromoneValue(component)**self.getAlpha() * self.getHeuristicValue(component)**self.getBeta()

class DecisionComponentRecording(Decision):
    def __init__(self, **kwargs):
        self.components = set()
        self.solutionValue = 0

        super().__init__(**kwargs)

    def addSolutionComponent(self, component):
        self.components.add(component)
        self.solutionValue += self.getComponentCost(component)

    def getSolutionComponents(self):
        return (c for c in self.components)

    def probabilisticDecision(self, components):
        total = sum(self.getNumerator() for c in components)

        import random
        r = random.random()*total

        import bisect
        return bisect.bisect((self.getNumerator() for c in components), r)

        def getSolutionValue(self):
            return self.solutionValue

        def getHeuristicValue(self, component):
            return 1/self.getComponentCost(component)

class AS_Decision(DecisionComponentRecording):
    def makeDecision(self, components):
        component = self.probabilisticDecision()
        self.addSolutionComponent(component)
        return component

MMAS_Decision = AS_Decision

class ACS_Decision(DecisionComponentRecording):
    def __init__(self, phi = dp.phi, **kwargs):
        self.phi = phi

        super().__init__(**kwargs)

    def getPhi(self):
        return self.phi

    def deterministicFactor(self, component):
        return self.getPheromoneValue(component)*self.getHeuristicValue(component)**self.getBeta()

    def deterministicDecision(self, components):
        return max((c for c in range(components)), key = lambda c: self.deterministicFactor(c))

    def makeDecision(self, components):
        import random
        r = random.random()
        if r <= self.getq0():
            component = self.deterministicDecision()
        else:
            component = self.probabilisticDecision()
            self.addSolutionComponent(component)

        tau = self.getPheromoneValue(component)
        tau0 = self.getTau0()
        phi = self.getPhi()
        self.setPheromoneValue(component, (1-phi)*tau + phi*tau0)

        return component

    @abc.abstractmethod
    def setPheromoneValue(self, component):
        pass

    @abc.abstractmethod
    def getq0(self):
        pass

