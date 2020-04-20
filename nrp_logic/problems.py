from typing import List

from platypus import Problem, Binary, Solution

from nrp_logic.entities import NRPInstance, NRPSolution


def make_solutions(nrp: NRPInstance, solutions: List[Solution]) -> List[NRPSolution]:
    res = []
    for sol in solutions:
        res.append(make_solution(nrp, sol))
    return res


def make_solution(nrp: NRPInstance, solution: Solution) -> NRPSolution:
    """
    Makes NRP_Solution out of Platypus Solution
    """
    reqs = []
    for i, is_met in enumerate(solution.variables[0]):
        if is_met:
            reqs.append(nrp.requirements[i])
    return NRPSolution(total_score=solution.objectives[0], total_cost=solution.constraints[0], requirements=reqs)


class NRP_Problem_SO(Problem):
    def __init__(self, nrp_instance: NRPInstance):
        # 1 decision variable, 1 objective, 2 constraint
        super(NRP_Problem_SO, self).__init__(1, 1, 2)
        self.nrp_instance = nrp_instance
        # Binary solution with size of number of requirements
        self.types[:] = Binary(len(nrp_instance.requirements))
        # Maximize score
        self.directions[:] = Problem.MAXIMIZE
        #  Cost <= budget and score > 0
        self.constraints[0] = "<={}".format(nrp_instance.budget)
        self.constraints[1] = ">0"

    def evaluate(self, solution: Solution):
        score, cost = self.nrp_instance.get_score_cost(solution.variables[0])
        solution.objectives[:] = [score]
        solution.constraints[:] = [cost, score]


class NRP_Problem_MO(Problem):
    def __init__(self, nrp_instance: NRPInstance):
        # 1 decision variable, 2 objectives, 2 constraint
        super(NRP_Problem_MO, self).__init__(1, 2, 2)
        self.nrp_instance = nrp_instance
        self.types[:] = Binary(len(nrp_instance.requirements))
        # Maximize score
        self.directions[0] = Problem.MAXIMIZE
        # Minimize cost
        self.directions[1] = Problem.MINIMIZE
        self.constraints[0] = "<={}".format(nrp_instance.budget)
        self.constraints[1] = ">0"

    def evaluate(self, solution: Solution):
        score, cost = self.nrp_instance.get_score_cost(solution.variables[0])
        # Changed
        solution.objectives[:] = [score, cost]
        solution.constraints[:] = [cost, score]
