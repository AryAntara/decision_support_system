from abc import ABC, abstractmethod
from models import criteria, alternative
from tabulate import tabulate
import copy


class DecisionMethod:

    @property
    @abstractmethod
    def criteria() -> criteria.CriteriaModel:
        pass

    @property
    @abstractmethod
    def alternatives() -> alternative.AlternativeModel:
        pass

    @abstractmethod
    def evaluate(self) -> dict:
        pass

    ROUNDED_SIZE: int = 3
    options: dict[any] = {"silent": True}

    def print(self, content):
        if self.options.get("silent") == True:
            return

        if isinstance(content, dict):
            table = copy.deepcopy(content)

            for name in table.keys():
                item = table[name]
                if isinstance(item, list):
                    for i, v in enumerate(item):
                        if isinstance(v, float):
                            table[name][i] = round(v, self.ROUNDED_SIZE)

            
            # reversing table
            table_rev = {}
            for i, name in enumerate(table):

                item = table[name]
                if i == 0:
                    table_rev[name] = list(table.keys())[1:]
                    for j, v in enumerate(item):
                        table_rev[v] = []
                    continue

                for k, reversed_name in enumerate(table_rev.keys()):

                    if k == 0:
                        continue
                    table_rev[reversed_name].append(table[name][k - 1])

            content = tabulate(table_rev, headers="keys", tablefmt="pretty")

        elif isinstance(content, list):
            table = copy.deepcopy(content)
            for i, v in content:
                if isinstance(v, float):
                    table[i] = round(v)

            content = tabulate(table, headers="keys", tablefmt="pretty")

        print(content)

    def set_opts(self, options: dict):
        for name in options.keys():
            opt = options.get(name)

            if opt == None:
                continue
            self.options[name] = opt
            
    def rank(self, scores: list[int]) -> list:
        sorted_scores = sorted(enumerate(scores), key=lambda x: -x[1])
        ranks = [0] * len(scores)
        rank = 1

        for i, (idx, score) in enumerate(sorted_scores):
            if i > 0 and score != sorted_scores[i - 1][1]:
                rank = i + 1
            ranks[idx] = rank
            
        return ranks
        