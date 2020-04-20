from typing import List, Set
import matplotlib.pyplot as plt


class Requirement:
    def __init__(self, cost=0, name=None, req_id=0):
        if name is None:
            name = "Req_" + str(req_id)
        self.req_id: int = req_id
        self.cost: float = cost
        self.name: str = name
        self.score: float = None
        self.prerequisites: Set[Requirement] = set()

    def add_prerequisite(self, prerequisite) -> None:
        self.prerequisites.add(prerequisite)

    def __str__(self) -> str:
        return 'Id_{}: "{}"'.format(self.req_id, self.name)


class Stakeholder:
    def __init__(self, name="", weight=0, values=None):
        if values is None:
            values = {}
        self.name = name
        self.weight = weight
        self.req_values = values


class NRPInstance:
    def __init__(self, requirements: List[Requirement] = None, stakeholders: List[Stakeholder] = None,
                 budget: float = None,
                 budget_ratio: float = None):
        self.requirements: List[Requirement] = requirements
        self.stakeholders: List[Stakeholder] = stakeholders
        self.total_cost: float = None
        self.total_score: float = None
        max_budg = self.__get_max_budget(budget_ratio)
        if budget is None:
            budget = max_budg
            if budget_ratio is not None:
                budget *= budget_ratio
        self.budget: float = budget
        # TODO find better place to put it:
        self.calculate_scores()
        self.trans_closure_all()

    def calculate_scores(self) -> float:
        """
        Calculates scores for requirements and total score
        :return: total score
        """
        self.total_score = 0
        for r in self.requirements:
            r.score = 0
            for s in self.stakeholders:
                r.score += s.weight * s.req_values.get(r.req_id, 0)
            self.total_score += r.score
        return self.total_score

    def __get_max_budget(self, budget_ratio: float) -> float:
        self.total_cost = 0
        sum = 0
        for req in self.requirements:
            sum += req.cost
        self.total_cost = sum
        return sum

    def get_score_cost(self, candidate: List[bool]) -> (float, float):
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

    # Old version
    # def trans_closure(self, req: Requirement):
    #     # new_preq = req.prerequisites.copy()
    #     stack = list(req.prerequisites)
    #     while stack:
    #         prereq = stack.pop()
    #         if prereq == req:
    #             raise RuntimeError("Cycle in the requirements dependencies!")
    #         req.add_prerequisite(prereq)
    #         for p in prereq.prerequisites:
    #             stack.append(p)

    def trans_closure(self, req: Requirement) -> None:
        """
        Transitive closure for requirement with check for cycles
        :except: RuntimeErrpor
        """
        def cycle_error():
            raise RuntimeError("Cycle in the requirements dependencies!")

        # To detect a cycle in requirements tree
        visited = [False] * len(self.requirements)
        on_stack = [False] * len(self.requirements)
        stack = list(req.prerequisites)
        while stack:
            prereq = stack.pop()
            ind = prereq.req_id - 1
            if not visited[ind]:
                visited[ind] = True
                on_stack[ind] = True
                # Putting back
                stack.append(prereq)
            else:
                on_stack[ind] = False
            if prereq != req:
                # Adding prereq
                req.add_prerequisite(prereq)
            else:
                cycle_error()
            for p in prereq.prerequisites:
                if not visited[p.req_id - 1]:
                    stack.append(p)
                elif on_stack[p.req_id - 1]:
                    cycle_error()


class NRPSolution:
    def __init__(self, total_score: float, total_cost: float, requirements: List[Requirement]):
        self.total_cost = total_cost
        self.total_score = total_score
        self.requirements = requirements

    def reqs_to_string(self, separator: str) -> str:
        return separator.join([str(r) for r in self.requirements])


def plot_solutions(solutions: List[NRPSolution], budget, title, file_name='last_result.png'):
    """
    Plots solutions and saves the picture
    """
    plt.clf()
    xs = [s.total_score for s in solutions]
    ys = [s.total_cost for s in solutions]
    # plt.scatter(xs, ys, c='red', label='Infeasible')
    # feasible_xs = [s.objectives[0] for s in solutions]
    # feasible_ys = [s.constraints[0] for s in solutions]
    plt.scatter(xs, ys, c='blue', label='Solutions')
    # nondominated_xs = [s.objectives[0] for s in nondominated_solutions]
    # nondominated_ys = [s.constraints[0] for s in nondominated_solutions]
    # plt.scatter(nondominated_xs, nondominated_ys,
    #             c='green', label='Nondominated')
    xmin = min(xs)
    xmax = max(xs)
    dx = xmax - xmin
    margin = 0.1
    xmin -= dx * margin
    xmax += dx * margin
    ymin = min(ys)
    ymax = max(ys)
    dy = ymax - ymin
    ymin -= dy * margin
    ymax += dy * margin
    plt.hlines(budget, xmin, xmax, label='Budget')
    plt.title(title)
    plt.legend()
    plt.xlabel("Score")
    plt.ylabel("Cost")
    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])
    plt.savefig(file_name)
    return file_name
