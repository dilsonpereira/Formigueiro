# Formigueiro - A python Framework for Simple Ant Colony Optimization Algorithms

Formigueiro is a framework that transforms user provided constructive heuristics into Ant Colony Optimization (ACO) algorithms.

## A Quick Introduction to Ant Colony Optimization

### Combinatorial Optimization
In Combinatorial Optimization problems, possible (or feasible) solutions are made up of *components*. Combinations of components that satisfy the problem constraints (that "make sense" as solutions) are called feasible solutions.
Finding optimal solutions (feasible combinations of components that minimize an objective function) is often hard.

### Constructive Heuristics
Constructive heuristics build solutions by iteratively adding components to an initially empty set. At each step, they employ some criterion to select one from a set of components whose selection can potentially lead to a feasible solution.

### Ant Colony Optimization
In nature, ants cooperate in finding resources by depositing pheromone along their traveled paths. Ant Colony Optimization is a metaheuristic inspired by this behavior.

Ants are responsible for applying a constructive algorithm to build solutions. After the solution is built, they might deposit pheromone on the components they employed. The amount of pheromone depends on the quality of the solution they found.

During the construction phase, the next component to be added to the solution is selected probabilistically. The probability p<sub>c</sub> for the selection of a component c takes into account the amount of pheromone &tau;<sub>c</sub> deposited on that component by all the ants as well as a measure &eta;<sub>c</sub> of the cost of employing that component on a solution. 

Let C be the set of components available to be selected at the current iteration. Let A be the set of ants.
In Ant System (one of the most basic ACO variations) the following formula for the probability of selecting component c is used:

p<sub>c</sub> = &tau;<sub>c</sub><sup>&alpha;</sup>&eta;<sub>c</sub><sup>&beta;</sup>/&Sigma;<sub>c'&isin;C</sub>&tau;<sub>c'</sub><sup>&alpha;</sup>&eta;<sub>c'</sub><sup>&beta;</sup>

After the construction and an optional local search phase, pheromones are then updated:

&tau;<sub>c</sub> &larr; (1-&rho;)&tau;<sub>c</sub> + &Sigma;<sub>a&isin;A</sub>&Delta;&tau;<sub>c</sub><sup>a</sup>, 

where &Delta;&tau;<sub>c</sub><sup>a</sup> = Q/f(a) if c is used by ant a, 0 otherwise; and f(a) is the objective value of the solution built by ant a.

&alpha;, &beta;, &rho;, and Q are algorithm parameters.

#### Main Variations

##### Ant System
Explained above.

##### Max-Min Ant System
* Pheromone values are updated only by global or iteration best ants.
* There are upper and lower limits on the amount of pheromone of each component.

##### Ant Colony System
* Pheromone values are updated only by global or iteration best ants.
* Local pheromone updates: Ants update component pheromones as soon as they are selected:
&tau;<sub>c</sub> &larr; (1-&phi;)&tau;<sub>c</sub> + &phi;&tau;<sub>0</sub>. The initial amount of pheromone on each component is &tau;<sub>0</sub> and &phi; is an algorithm parameter.
* Pseudorandom proportional rule: In order to select the next component, an ant draws a random number q &isin; [0, 1]. If q &le; q<sub>0</sub>, where q<sub>0</sub> is an algorithm parameter, the next component will be the one that maximizes &tau;<sub>c</sub>&eta;<sub>c</sub><sup>&beta;</sup>. Else, the classic rule is applied.

## How to Use the Framework

In short, we implement a constructive heuristic that calls a special method every time a component has to be chosen, possible choices are passed as arguments.

As an example, lets consider the Traveling Salesman Problem (TSP).

The following class implements a randomly generated TSP instance:
```python
class TSPInstance():
    def __init__(self, n):
        self.n = n

        self.xcoord = [random.random()*100 for v in range(n)]
        self.ycoord = [random.random()*100 for v in range(n)]

    def getNumVertices(self):
        return self.n

    def getWeight(self, u, v):
        return ((self.xcoord[u]-self.xcoord[v])**2 + (self.ycoord[u]-self.ycoord[v])**2)**(1/2)
```
In the above implementation, vertices are randomly chosen points in a 100x100 plane. Edge weights are the Euclidean distances between the vertices.

To use the framework, we have to define a user class subclassing an ant class corresponding to our desired ACO variation:

* `AS_Ant` for Ant System.
* `ACS_Ant` for Ant Colony System.
*  `MMAS_Ant` for Min-Max Ant System

**If we choose to define a constructor in our user class**, in addition to user parameters, we **must** receive a dictionary of keyword parameters of the form `**kwargs` and make a call to `super().__init__(**kwargs)`

```python
class TSPAnt(Formigueiro.ACS_Ant):
    def __init__(self, instance, **kwargs):
        self.instance = instance

        super().__init__(**kwargs)
```

In the example above, we subclass `ACS_Ant` and the constructor of our user class receives the problem instance.

The method `constructSolution` is where solutions should be built. In the example, components will be tuples of the form `(u, v)`, representing edges. In Formigueiro, **every component must be hashable**. Every time a component has to be selected, we must call `makeDecision`, passing an iterable with the possible choices. `makeDecision` will return the selected component.

```python
    def constructSolution(self):
        # set of all vertices
        V = set(range(self.instance.getNumVertices()))

        # initial vertex - last added vertex
        u = 0

        # vertices in the solution
        U = set([u])

        while U != V:
            # the available components at the current iteration
            # are (u, v) where u is the last added vertex
            # and v is a vertex that has not been added
            components = [(u, v) for v in V - U]

            # select a component and update u
            _, u = self.makeDecision(components)

            U.add(u)

        # add last edge
        self.makeDecision([(u, 0)])
```

We must also tell Formigueiro how to evaluate the cost of a component by implementing the method `getComponentCost`:

```python
    def getComponentCost(self, component):
        return self.instance.getWeight(*component)
```

This is the complete class:

```python
class TSPAnt(Formigueiro.ACS_Ant):
    def __init__(self, instance, **kwargs):
        self.instance = instance

        super().__init__(**kwargs)

    def getComponentCost(self, component):
        return self.instance.getWeight(*component)

    def constructSolution(self):
        # set of all vertices
        V = set(range(self.instance.getNumVertices()))

        # initial vertex - last added vertex
        u = 0

        # vertices in the solution
        U = set([u])

        while U != V:
            # the available components at the current iteration
            # are (u, v) where u is the last added vertex
            # and v is a vertex that has not been added
            components = [(u, v) for v in V - U]

            # select a component and update u
            _, u = self.makeDecision(components)

            U.add(u)

        # add last edge
        self.makeDecision([(u, 0)])
```

Finally, to solve the problem, we call `Solve`, passing the user class as an argument, together with arguments for Formigueiro and arguments for the user class itself. `Solve` will return the objective value and the components in the best solution found:

```python
instance = TSPInstance(50)
obj, components = Formigueiro.Solve(antCls = TSPAnt, instance = instance, numIterations = 1000, numAnts = 10, alpha = 1, beta = 1) 
```

The following are the parameters that can be passed to `Solve`:

Name | Meaning | Default
-----|---------|--------
alpha | &alpha; | 1
beta |&beta;| 1
rho |&rho;| 0.1
Q   |Q| 1
tau0 |&tau;<sub>0</sub>| 1
q0 |q<sub>0</sub>| 0.5
phi |&phi;| 0.9
minPheromone |min. amount of pheromone in MMAS| -&#x221e;
maxPheromone |max. amount of pheromone in MMAS| &#x221e;
numAnts |number of ants| 10
numIterations |number of iterations| 100


## Support for Local Search
Local Search is supported. The user must implement the `localSearch` method in the user class. If local search is implemented, the `getSolutionComponents` method must also be implemented. It should return an iterable with the components in the solution after local search.
