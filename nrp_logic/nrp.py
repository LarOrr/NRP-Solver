from abc import abstractmethod, ABCMeta
from typing import List
from platypus import Problem, Binary, Real, RandomGenerator, Solution
from nrp_logic.entities import Requirement, Stakeholder, NRPInstance, NRPSolution


def make_solutions(nrp: NRPInstance, solutions: List[Solution]) -> List[NRPSolution]:
    res = []
    for sol in solutions:
        res.append(make_solution(nrp, sol))
    return res

def make_solution(nrp: NRPInstance, solution: Solution) -> NRPSolution:
    reqs = []
    for i, is_met in enumerate(solution.variables[0]):
        if is_met:
            reqs.append(nrp.requirements[i])
    return NRPSolution(total_score=solution.objectives[0], total_cost=solution.constraints[0], requirements=reqs)


class NRP_Problem_SO(Problem):
    def __init__(self, NRPInstance: NRPInstance):
        # 1 decision variable, 1 objective, 1 constraint
        super(NRP_Problem_SO, self).__init__(1, 1, 1)
        self.NRPInstance = NRPInstance
        self.types[:] = Binary(len(NRPInstance.requirements))
        # Maximize score
        self.directions[:] = Problem.MAXIMIZE
        self.constraints[0] = "<={}".format(NRPInstance.budget)

    def evaluate(self, solution: Solution):
        score, cost = self.NRPInstance.get_score_cost(solution.variables[0])
        solution.objectives[:] = [score]
        solution.constraints[:] = [cost]

class NRP_Problem_MO(Problem):
    def __init__(self, NRPInstance: NRPInstance):
        # 1 decision variable, 2 objectives, 1 constraint
        super(NRP_Problem_MO, self).__init__(1, 2, 1)
        self.NRPInstance = NRPInstance
        self.types[:] = Binary(len(NRPInstance.requirements))
        # Maximize score
        self.directions[0] = Problem.MAXIMIZE
        # Changed
        self.directions[1] = Problem.MINIMIZE
        self.constraints[0] = "<={}".format(NRPInstance.budget)

    def evaluate(self, solution: Solution):
        score, cost = self.NRPInstance.get_score_cost(solution.variables[0])
        # Changed
        solution.objectives[:] = [score, cost]
        solution.constraints[:] = [cost]

