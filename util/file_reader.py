from abc import ABC, abstractmethod
from nrp_logic.entities import Requirement, Stakeholder, NRPInstance
# from nrp_logic.nrp import
# from nrp_logic.Stakeholder import Stakeholder

class AbstractFileReader(ABC):
    @abstractmethod
    def read_nrp_instance(self, filename):
        pass


class FileReader(AbstractFileReader):
    # @abstractmethod
    def read_nrp_instance(self, filename):
        # TODO where to eval score?
        stakeholders = []
        requirements = []

        file = open(filename, 'r')
        lines = file.readlines()
        # line_index = 0
        # 1.1 get requirements
        temp = lines[0].split()
        budget = None
        ratio = None
        if temp[0] == 'B':
            # nrp.budget = float(temp[1])
            budget = float(temp[1].strip())
        elif temp[0] == 'R':
            # TODO fix readline
            # nrp.budget = nrp.get_max_budget(float(temp[1]))
            ratio = float(temp[1].strip())

        number_of_req = int(lines[1])
        line_ind = 2
        prereqs = []
        for i in range(number_of_req):
            req_info = lines[line_ind + i].strip().split(';')
            # Fix strip
            new_req = Requirement(req_id=i + 1, name=req_info[0].strip(), cost=int(req_info[1].strip()))
            requirements.append(new_req)
            prereqs.append([])
            for j in range(2, len(req_info)):
                try:
                    dependency_type, req_id = req_info[j].split()
                except ValueError:
                    continue
                req_id = int(req_id)
                if dependency_type == 'PRE':
                    # prereqs.append(req_id)
                    prereqs[i].append(req_id)
                    # new_req.add_prerequisi
                    # te(requirements[req_id - 1])
                else:
                    raise NotImplementedError()

        # TODO through setter
        for i, req in enumerate(requirements):
            for p in prereqs[i]:
                requirements[i].add_prerequisite(requirements[p - 1])
            # TODO add dep!!!
            # for id, req_cost_str in enumerate(req_costs):
            #     requirements.append(Requirement(req_id=id + 1, cost=float(req_cost_str)))
        line_ind += number_of_req
        # 2.1 Get stakeholders info
        number_of_stake = int(lines[line_ind])
        line_ind += 1
        for i in range(number_of_stake):
            raw_stake = lines[i + line_ind].strip().split(';')
            name = raw_stake[0]
            weight = float(raw_stake[1])
            values = {}
            for j in range(2, len(raw_stake)):
                t = raw_stake[j].strip().split()
                req = int(t[0].strip())
                val = float(t[1].strip())
                values[req] = val
            stakeholders.append(Stakeholder(name=name, weight=weight, values=values))

        nrp = NRPInstance(requirements, stakeholders, budget= budget, budget_ratio=ratio)
        return nrp

class ClassicFileReader(AbstractFileReader):
    def read_nrp_instance(self, filename):
        requirements = []

        file = open(filename, 'r')
        lines = file.readlines()

        budget = None
        ratio = None
        line_index = 1
        # try:
        temp = lines[0].split()
        if temp[0] == 'B':
            # nrp.budget = float(temp[1])
            budget = float(temp[1].strip())
        elif temp[0] == 'R':
            ratio = float(temp[1].strip())
        else:
            # If there is no budget or ratio in first line
            line_index = 0
        if ratio is None:
            # Default ratio
            ratio = 0.3

        # 1.1 get requirements
        number_of_levels = int(lines[line_index])
        last_id = 0
        for i in range(number_of_levels):
            line = lines[line_index + (i + 1) * 2]
            req_costs = line.strip().split()
            for id, req_cost_str in enumerate(req_costs):
                requirements.append(Requirement(req_id=last_id + id + 1, cost=float(req_cost_str)))
            last_id += len(req_costs)
        # 1.2 transform requirement cost to

        reqs_deps_index = line_index + (number_of_levels * 2) + 1
        # TODO deps
        reqs_deps_number = int(lines[reqs_deps_index])
        for i in range(reqs_deps_index + 1, reqs_deps_index + reqs_deps_number):
            id1, id2 = map(int, lines[i].strip().split())
            requirements[id1 - 1].add_prerequisite(requirements[id2 - 1])
        number_of_stake_index = reqs_deps_index + reqs_deps_number + 1
        number_of_stakes = int(lines[number_of_stake_index])
        # 2.1 Get stakeholders info
        raw_stakes = []
        for i in range(number_of_stake_index + 1, len(lines)):
            line = lines[i]
            bits = line.rstrip().split()
            # get unporcessed stake value
            stake_value_raw = int(bits.pop(0))
            # remove number of requirements
            bits.pop(0)
            # the leftover is just requirements
            reqs = []
            # convert to ints
            for j in range(len(bits)):
                reqs.append(int(bits[j]))
            # stakes is an array [raw_score, [...reqs]]
            raw_stakes.append([stake_value_raw, reqs])
        # 2.2 get sum of all stake value
        raw_stake_value_sum = raw_stakes[0][0]
        for i in range(len(raw_stakes)):
            raw_stake_value_sum += raw_stakes[i][0]
        # transform raw stakes values to floats 0.0-1.0
        # assign values to each stake requirement as well
        stakeholders = []
        for raw_stake in raw_stakes:
            raw_stake_value = raw_stake[0]
            raw_stake_requirements = raw_stake[1]

            stakeholder_value = raw_stake_value / raw_stake_value_sum

            number_of_stakeholder_requirements = len(raw_stake_requirements)
            stakeholder_requirements = {}
            stakeholder_requirement_value = 1 / 0.9
            for i in range(number_of_stakeholder_requirements):
                # stakeholder_requirement_value = ((number_of_stakeholder_requirements - i) / number_of_stakeholder_requirements) * 100
                stakeholder_requirement_value *= 0.9
                stakeholder_requirement = int(raw_stake_requirements[i])
                # stakeholder_requirements.append((stakeholder_requirement_value, stakeholder_requirement))
                stakeholder_requirements[stakeholder_requirement] = stakeholder_requirement_value
            stakeholders.append(Stakeholder(weight=stakeholder_value, values=stakeholder_requirements))
        return NRPInstance(requirements, stakeholders, budget=budget, budget_ratio=ratio)
