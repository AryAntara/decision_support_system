from methods import method
from models import alternative as altr, criteria as ctr
import math


class Moora(method.DecisionMethod):

    criteria: ctr.CriteriaModel = []
    alternatives: altr.AlternativeModel = []

    def __init__(
        self,        
        alternatives: altr.AlternativeModel,
        options: dict = {},
    ):
        self.criteria = alternatives.criteria
        self.alternatives = alternatives

        self.set_opts(options)

    def evaluate(self):
        self.print("============================")
        self.print("Calculating MOORA")
        
        # add divider        
        table_with_divider = self._add_devider()
        
        self.print("\nTable With Divider")
        self.print(table_with_divider)

        # normalize
        normalized_table = self._normalize_table(table_with_divider)
        
        self.print("\nNormalized Table")
        self.print(
            normalized_table,
        )

        # caluclate yi value
        yi_table = self._calculate_yi_value(normalized_table)
        self.print("\nYi Value")
        self.print(yi_table)

    def _calculate_yi_value(self, table: dict) -> dict:
        ctr = self.criteria
        ctr_types = ctr.get_types()
        codes = self.alternatives.get_codes()
        scores = []
        table["Crit"].append("BEN")
        table["Crit"].append("COST")
        table["Crit"].append("YI")
        table["Crit"].append("RANK")

        for code in codes:
            data = table[code]
            data_len = len(data)
            ben_idx = data_len
            cost_idx = data_len + 1
            yi_idx = data_len + 2

            for i in range(data_len):
                value = data[i]
                type = ctr_types[i]

                if type == "BENEFIT":
                    try:
                        table[code][ben_idx] += value
                        table[code][yi_idx] += value
                    except:
                        table[code].append(value)
                        table[code].append(0)
                        table[code].append(value)
                else:
                    try:
                        table[code][cost_idx] += value
                        table[code][yi_idx] -= value
                    except:
                        table[code].append(0)
                        table[code].append(value)
                        table[code].append(0 - value)
            
            scores.append(table[code][yi_idx])            
        del table["Div"]
        
        
        ranks = self.rank(scores)
        for i,code in enumerate(codes): 
            table[code].append(ranks[i])
            
        return table

    def _normalize_table(self, table: dict) -> dict:
        ctr = self.criteria
        ctr_len = ctr.length()
        ctr_weights = ctr.get_weights()

        codes = self.alternatives.get_codes()

        for i in range(ctr_len):
            divider = table.get("Div")
            for key in codes:

                value = table[key][i] / divider[i] * ctr_weights[i]
                table[key][i] = value
        
        return table

    def _add_devider(self) -> dict:
        table = self.alternatives.get_data()
        codes = self.alternatives.get_codes()
        ctr_len = self.criteria.length()

        table["Div"] = []
        for i in range(ctr_len):
            divider = table.get("Div")
            for key in codes:
                value = table[key][i]
                if len(divider) < i + 1:
                    table["Div"].append(value**2)
                else:
                    table["Div"][i] += value**2

        for i, v in enumerate(table["Div"]):
            table["Div"][i] = math.sqrt(v)

        return table
