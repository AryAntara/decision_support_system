from methods import method
from models import criteria as ctr, alternative as altr
import math


class Electre(method.DecisionMethod):
    criteria: ctr.CriteriaModel = []
    alternatives: altr.AlternativeModel = []

    def __init__(self, alternative: altr.AlternativeModel, options):
        self.criteria = alternative.criteria
        self.alternatives = alternative
        self.set_opts(options)

    def evaluate(self):
        self.print("============================")
        self.print("Calculating ELECTRE")

        # add divider
        table_with_divider = self._add_devider()

        self.print("\nTable With Divider")
        self.print(table_with_divider)

        # normalize
        normalized_table = self._normalize_table(table_with_divider)
        self.print("\nNormalized Table")
        self.print(normalized_table)

        # get cordences
        self.print("\nCalulate Cordenses And Thresolds")
        cordences = self._generate_cordences(normalized_table)

        self.print("\nTabel Concordence")
        self.print(cordences.get("concordence_table"))

        self.print("\nTabel Discordence")
        self.print(cordences.get("discordence_table"))

        self.print(f"\nTreshold Concordence {cordences.get('treshold_c')}")
        self.print(f"Treshold Discordence {cordences.get('treshold_d')}")

        # generate matrix F,G,E
        matrixs = self._generate_matrixs(cordences)

        self.print("\nMatrix F")
        self.print(matrixs.get("matrix_F"))
        self.print("\nMatrix G")
        self.print(matrixs.get("matrix_G"))
        self.print("\nMatrix E")
        self.print(matrixs.get("matrix_E"))

        return

    def _generate_matrixs(self, table: dict) -> dict:
        codes = self.alternatives.get_codes()
        codes_len = len(codes)
        matrix_E = {"Cat": codes + ["Sums", "Rank"]}
        matrix_F = table.get("concordence_table")
        matrix_G = table.get("discordence_table")
        treshold_c = table.get("treshold_c")
        treshold_d = table.get("treshold_d")

        for i in range(codes_len):
            idx = f"A{i+1}"
            data_c = matrix_F[idx]
            data_d = matrix_G[idx]
            data_e = []

            for j in range(codes_len):

                v_c = data_c[j]
                v_d = data_d[j]

                if v_c >= treshold_c:
                    matrix_F[idx][j] = 1
                else:
                    matrix_F[idx][j] = 0

                if i == j:
                    matrix_G[idx][j] = 0
                elif v_d < treshold_d:
                    matrix_G[idx][j] = 1
                else:
                    matrix_G[idx][j] = 0

                data_e.append(matrix_F[idx][j] * matrix_G[idx][j])

            matrix_E[idx] = data_e

        scores = []
        for name in codes:
            i = 0
            items = matrix_E[name]
            for v in items:
                i += v

            matrix_E[name].append(i)
            scores.append(i)

        ranks = self.rank(scores)
        for i, name in enumerate(codes):
            matrix_E[name].append(ranks[i])

        return {
            "matrix_F": matrix_F,
            "matrix_G": matrix_G,
            "matrix_E": matrix_E,
        }

    def _generate_cordences(self, table: dict) -> dict:

        codes = self.alternatives.get_codes()
        codes_len = len(codes)
        weights = self.criteria.get_weights()
        concordence_table = {"Cat": codes}
        discordence_table = {"Cat": codes}
        concordence_total = 0
        discordence_total = 0

        for i, code in enumerate(codes):
            alternatives = table.get(code)
            table_cij = []
            table_dij = []

            for j, compared_code in enumerate(codes):

                compared_alternatives = table.get(compared_code)
                total_c = 0
                table_d = []
                table_divider_d = []
                if i == j:
                    table_cij.append(0)
                    table_dij.append(0)
                    continue

                for k in range(len(alternatives)):
                    weight = weights[k]
                    v = alternatives[k]
                    compared_v = compared_alternatives[k]

                    if v >= compared_v:
                        total_c += weight
                    else:
                        table_d.append(abs(v - compared_v))

                    table_divider_d.append(abs(v - compared_v))

                if total_c == 0:
                    table_cij.append(0)
                else:
                    table_cij.append(total_c)

                if table_d == 0:
                    table_dij.append(0)
                else:
                    if len(table_d) == 0:
                        table_dij.append(0)
                    else:
                        table_dij.append(max(table_d) / max(table_divider_d))

            concordence_table[f"A{i+1}"] = table_cij
            discordence_table[f"A{i+1}"] = table_dij
            concordence_total += sum(table_cij)
            discordence_total += sum(table_dij)

        treshold_c = concordence_total / (codes_len * (codes_len - 1))
        treshold_d = discordence_total / (codes_len * (codes_len - 1))

        return {
            "concordence_table": concordence_table,
            "discordence_table": discordence_table,
            "treshold_c": treshold_c,
            "treshold_d": treshold_d,
        }

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
