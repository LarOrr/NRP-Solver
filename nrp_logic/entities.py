from typing import List, Set


# from __future__ import annotations


class Requirement:
    def __init__(self, cost=0, name=None, req_id=0):
        if name is None:
            name = "Req_" + str(req_id)
        self.req_id: int = req_id
        self.cost: int = cost
        self.name: str = name
        self.score = None
        # if prerequisites is None:
        #     # TODO ?
        #     prerequisites = set()
        self.prerequisites: Set[Requirement] = set()

    def add_prerequisite(self, prerequisite):
        self.prerequisites.add(prerequisite)

    def __str__(self):
        return "{}".format(self.req_id)


class Stakeholder:
    def __init__(self, name="", weight=0, values=None):
        if values is None:
            values = {}
        self.name = name
        self.weight = weight
        # TODO dict
        self.req_values = values


class NRPInstance:
    # __metaclass__ = ABCMeta

    def __init__(self, requirements: List[Requirement] = None, stakeholders: List[Stakeholder] = None, budget=None,
                 budget_ratio=None):
        self.requirements = requirements
        self.stakeholders = stakeholders
        if budget is None:
            budget = self.__get_max_budget(budget_ratio)
        self.budget = budget
        # TODO when? Create controller&
        self.calculate_scores()
        self.trans_closure_all()

    def calculate_scores(self):
        for r in self.requirements:
            r.score = 0
            for s in self.stakeholders:
                r.score += s.weight * s.req_values.get(r.req_id, 0)

    def __get_max_budget(self, budget_ratio):
        sum = 0
        for req in self.requirements:
            sum += req.cost
        if budget_ratio is None:
            return sum
        return sum * budget_ratio

    def get_score_cost(self, candidate: List[bool]):
        # score is a sum of all customer weighted scores
        score = 0
        cost = 0
        for i, req_met in enumerate(candidate):
            if req_met:
                score += self.requirements[i].score
                cost += self.requirements[i].cost
        return score, cost

    def trans_closure_all(self):
        for r in self.requirements:
            self.trans_closure(r)

    def trans_closure(self, req: Requirement):
        # new_preq = req.prerequisites.copy()
        # TODO check loops!
        stack = list(req.prerequisites)
        while stack:
            prereq = stack.pop()
            # TODO list?
            req.add_prerequisite(prereq)
            for p in prereq.prerequisites:
                stack.append(p)


class NRPSolution():
    def __init__(self, total_score: float, total_cost: float, requirements: List[Requirement]):
        self.total_cost = total_cost
        self.total_score = total_score
        self.requirements = requirements
