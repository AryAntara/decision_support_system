from methods import method
from models import criteria as ctr
import copy


class AHP(method.DecisionMethod):   
    criteria = ctr.CriteriaModel
    priorities = dict
    RI_VALUES = [
        0.00,
        0.00,
        0.58,
        0.90,
        1.12,
        1.24,
        1.32,
        1.41,
        1.45,
        11.49,
        11.51,
        11.54,
        11.56,
        11.57,
    ]

    def __init__(
        self, criteria: ctr.CriteriaModel, priorities: dict, options: dict = {}
    ):
        self.criteria = criteria
        self.priorities = priorities
        (message, status) = self._validate_priority()
        if not status:
            raise Exception(message)

        self.set_opts(options)

    def evaluate(self) -> dict:
        self.print("Calculating AHP")

        # create a pairwase tables
        pairwise_table = self._create_pairwise()
        self.print("\n# Pairwise Table")
        self.print(pairwise_table)

        # normalize the tables
        normalized_table = self._normalize(copy.deepcopy(pairwise_table))
        self.print("\n# Normalized Table")
        self.print(normalized_table)

        # calculate eigen vector and value
        eigen = self._calculate_eigen(normalized_table, pairwise_table)
        self.print("\n# Eigen Vector")
        self.print(eigen)

        # calculate CI
        CI = self._calculate_CI(eigen)
        self.print("CI   : {}".format(round(CI, self.ROUNDED_SIZE)))

        # calculate RI
        RI = self._get_RI()
        self.print("RI   : {}".format(round(RI, self.ROUNDED_SIZE)))

        # calculate CR
        CR = self._calculate_CR(CI, RI)
        self.print("CR   : {}".format(round(CR, self.ROUNDED_SIZE)))

        # return all calculated items
        return {
            "pairwise_table": pairwise_table,
            "normalized_table": normalized_table,
            "eigen": eigen,  # Corrected spelling
            "CI": CI,
            "RI": RI,
            "CR": CR,
        }

    def _validate_priority(self) -> tuple[str, bool]:

        ctr = self.criteria
        priorities = self.priorities
        names = ctr.get_names()

        for i, name in enumerate(names[:-1]):
            priority = priorities.get(name)
            if not priority:
                return ("The {} is need in priority list".format(priority), False)

            for comp_name in names[i + 1 :]:
                if not priority.get(comp_name):
                    return (
                        "The {} is need to be added in priority with {}".format(
                            comp_name, name
                        ),
                        False,
                    )

        return ("Validation success", True)

    def _create_pairwise(self) -> dict:
        names = self.criteria.get_names()
        priorities = self.priorities
        table = {
            "Cat": names + ["Total"],
        }

        for i, name in enumerate(names):
            table[name] = []
            priority_criteria = priorities.get(name)  # C1, C3

            for comp_name in names:
                if comp_name == name:
                    table[name].append(1)
                    continue

                compared_v = 0
                if priority_criteria:
                    compared_priority = priority_criteria.get(comp_name)  # C2 - C8

                    if compared_priority != None:
                        is_more_important = compared_priority.get("is_more_important")
                        compared_v = compared_priority.get("value")
                        if not is_more_important:
                            compared_v = 1 / compared_v

                        table[name].append(compared_v)
                        continue

                compared_priority_criteria = priorities.get(comp_name)
                compared_priority = compared_priority_criteria.get(name)
                is_more_important = compared_priority.get("is_more_important")
                compared_v = compared_priority.get("value")
                if is_more_important:
                    compared_v = 1 / compared_v
                else:
                    compared_v = 1 / (1 / compared_v)

                table[name].append(compared_v)

            table[name].append(sum(table[name]))

        return table

    def _normalize(self, table: dict) -> dict:
        names = self.criteria.get_names()
        for name in names:
            table_item = table[name]
            total = table_item[-1]
            for i in range(len(table_item) - 1):
                weight = table_item[i]
                table_item[i] = weight / total
            del table[name][-1]
        del table["Cat"][-1]

        table["Total"] = []
        for i in range(len(names)):
            total = table["Total"]
            for name in names:
                value = table[name][i]
                if len(total) < i + 1:
                    table["Total"].append(value)
                else:
                    table["Total"][i] += value
            table["Total"][i] = table["Total"][i]

        return table

    def _calculate_eigen(self, table: dict, pairwise_table: dict) -> dict:
        totals = table.get("Total")
        names = self.criteria.get_names()
        eigen_vecs = {"Crit": names, "Total": totals, "Eigen_vector": [], "Eigen_value": []}

        names = self.criteria.get_names()
        for i, name in enumerate(names):
            pw_total = pairwise_table[name][-1]
            normalized_total = totals[i]
            eigen_vec = normalized_total / len(names)
            eigen_vecs["Eigen_vector"].append(eigen_vec)
            eigen_vecs["Eigen_value"].append(eigen_vec * pw_total)

        return eigen_vecs

    def _get_RI(self):
        rvl = len(self.RI_VALUES)
        cl = self.criteria.length()
        idx = -1
        if rvl >= cl:
            idx = cl - 1

        return self.RI_VALUES[idx]

    def _calculate_CI(self, table: dict) -> int:
        ev = table.get("Eigen_value")
        n = len(ev)
        CI = (sum(ev) - n) / (n - 1)
        return CI

    def _calculate_CR(self, CI: int, RI: int) -> int:
        return CI / RI

    def to_criteria(self) -> ctr.CriteriaModel:
        ev = self.evaluate()

        cr = self.criteria
        cr.data["weight"] = ev.get("eigen")["Eigen_vector"]
        return cr

# assign priority for a Criteria between other
def priority(value: int, is_more_important: bool = True):
    return {"value": value, "is_more_important": is_more_important}
