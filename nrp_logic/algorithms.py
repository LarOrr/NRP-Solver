from typing import List
from platypus import Problem, Binary, Real, RandomGenerator, Solution, NSGAII, nondominated_truncate, nondominated_sort, \
    default_variator, TournamentSelector
from nrp_logic.entities import Requirement


class Repairer:
    def __init__(self, requirements: List[Requirement]):
        self.requirements = requirements

    def repair_all(self, sols: List[Solution]):
        for s in sols:
            self.repair(s)

    # TODO positive repair
    def repair(self, sol: Solution):
        include_req = sol.variables[0]
        for i, is_met in enumerate(include_req):
            # ! Works for transitive closed requirements!
            if is_met:
                req = self.requirements[i]
                for prereq in req.prerequisites:
                    if not include_req[prereq.req_id - 1]:
                        # Deleting this requirement from list if at lest one prerequisite is not met
                        include_req[i] = False
                        break


class NSGAII_Repair(NSGAII):

    def __init__(self, problem: Problem, repairer: Repairer,
                 population_size=100,
                 generator=RandomGenerator(),
                 selector=TournamentSelector(2),
                 variator=None,
                 archive=None,
                 **kwargs):
        super(NSGAII_Repair, self).__init__(problem, population_size, generator, selector, variator, archive, **kwargs)
        self.repairer = repairer

    def initialize(self):
        self.population = [self.generator.generate(self.problem) for _ in range(self.population_size)]
        # Modification:
        self.repairer.repair_all(self.population)
        self.evaluate_all(self.population)
        if self.archive is not None:
            self.archive += self.population
        if self.variator is None:
            self.variator = default_variator(self.problem)

    # Overloading of iterate
    def iterate(self):
        offspring = []

        while len(offspring) < self.population_size:
            parents = self.selector.select(self.variator.arity, self.population)
            offspring.extend(self.variator.evolve(parents))
        # Modification:
        self.repairer.repair_all(offspring)
        self.evaluate_all(offspring)

        offspring.extend(self.population)
        nondominated_sort(offspring)
        self.population = nondominated_truncate(offspring, self.population_size)

        if self.archive is not None:
            self.archive.extend(self.population)
