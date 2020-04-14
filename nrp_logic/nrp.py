from abc import abstractmethod, ABCMeta
from typing import List
from platypus import Problem, Binary, Real, RandomGenerator, Solution
from nrp_logic.entities import Requirement, Stakeholder, NRPInstance
# from nrp_logic.Stakeholder import Stakeholder

class NRPSolution():
    # TODO implement
    pass

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

# class NRPInstance:
#     # __metaclass__ = ABCMeta
#
#     def __init__(self, requirements: List[Requirement] = None, stakeholders: List[Stakeholder] = None, budget=None, budget_ratio=None):
#         self.requirements = requirements
#         self.stakeholders = stakeholders
#         if budget is None:
#             budget = self.__get_max_budget(budget_ratio)
#         self.budget = budget
#         # TODO when? Create controller&
#         self.calculate_scores()
#         self.trans_closure_all()
#
#     def calculate_scores(self):
#         for r in self.requirements:
#             r.score = 0
#             for s in self.stakeholders:
#                 r.score += s.weight * s.req_values.get(r.req_id, 0)
#
#     def __get_max_budget(self, budget_ratio):
#         sum = 0
#         for req in self.requirements:
#             sum += req.cost
#         if budget_ratio is None:
#             return sum
#         return sum / budget_ratio
#
#     def get_score_cost(self, candidate: List[bool]):
#         # score is a sum of all customer weighted scores
#         score = 0
#         cost = 0
#         for i, req_met in enumerate(candidate):
#             if req_met:
#                 score += self.requirements[i].score
#                 cost += self.requirements[i].cost
#         return score, cost
#
#     def trans_closure_all(self):
#         for r in self.requirements:
#             self.trans_closure(r)
#
#     def trans_closure(self, req: Requirement):
#         # new_preq = req.prerequisites.copy()
#         # TODO check loops!
#         stack = list(req.prerequisites)
#         while stack:
#             prereq = stack.pop()
#             # TODO list?
#             req.add_prerequisite(prereq)
#             for p in prereq.prerequisites:
#                 stack.append(p)

    # @abstractmethod
    # def get_problem_function(self):
    #     raise NotImplementedError('Method not implemented')
    #
    # @abstractmethod
    # def generate_problem(self):
    #     raise NotImplementedError('Method not implemented')

# class NRP_Problem(NRPInstance):
#     def __init__(self, requirements, clients, budget, budget_ratio, score_weight, cost_weight):
#         super(NRP_Singleobj, self).__init__(requirements, clients, budget, budget_ratio)
#         self.score_weight = score_weight
#         self.cost_weight = cost_weight
#
#     def get_problem_function(self, x):
#         score = self.get_score(x[0])
#         cost = self.get_cost(x[0])
#         weighted_score = self.score_weight * score
#         weighted_cost = self.cost_weight * cost
#         fitness = weighted_score + weighted_cost
#         number_of_requirements_met = len(self.get_requirements_met(x[0]))
#         max_budget_constraint = cost - self.max_budget
#        Функция, потом констреиты
#         return [fitness], [number_of_requirements_met, max_budget_constraint]
#
#     def generate_problem(self):
#         # 1 decision variables, 1 objectives, 2 constraints
#         problem = Problem(1, 1, 2)
#         problem.types[:] = Binary(len(self.requirements))
#         problem.directions[:] = Problem.MAXIMIZE
#         problem.constraints[0] = "!=0"
#         problem.constraints[1] = "<=0"
#         problem.function = self.get_problem_function
#         return problem

# class NRP_Problem(Problem):
#     def __init__(self, NRPInstance: NRPInstance, ndecision_vars: int, nobjectives: int, nconstraints: int):
#         super(NRP_Problem, self).__init__(ndecision_vars, nobjectives, nconstraints)
#         self.NRPInstance = NRPInstance
#         self.types[:] = Binary(len(NRPInstance.requirements))

