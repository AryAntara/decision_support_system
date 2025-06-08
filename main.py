from methods import moora, electre
from methods.ahp import AHP, priority
from methods.moora import Moora
from methods.electre import Electre
from models.criteria import CriteriaModel
from models.alternative import AlternativeModel


COST = "COST"
BENEFIT = "BENEFIT"

criteria = CriteriaModel(
    {
        "type": [
            COST,
            BENEFIT,
            BENEFIT,
            COST,
            COST,
            COST,
            COST,
            BENEFIT,
        ],
        "name": ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"],  # Must be ordered
        "label": [
            "C1 (Harga)",
            "C2 (Rating)",
            "C3 (Fasilitas)",
            "C4 (Larangan Hewan Peliharan)",
            "C5 (Deposit)",
            "C6 (Larangan Merokok)",
            "C7 (Larangan Alkohol)",
            "C8 (Bisa Di Refund)",
        ],
        "weight": [0, 0, 0, 0, 0, 0, 0, 0],
    }
)

ahp_method = AHP(
    criteria,
    {
        "C1": {
            "C2": priority(2),
            "C3": priority(1),
            "C4": priority(1),
            "C5": priority(1),
            "C6": priority(5),
            "C7": priority(3),
            "C8": priority(1),
        },
        "C2": {
            "C3": priority(3, False),
            "C4": priority(3, False),
            "C5": priority(1),
            "C6": priority(5),
            "C7": priority(1),
            "C8": priority(1),
        },
        "C3": {
            "C4": priority(1),
            "C5": priority(1),
            "C6": priority(3),
            "C7": priority(1),
            "C8": priority(3),
        },
        "C4": {
            "C5": priority(1),
            "C6": priority(3),
            "C7": priority(3),
            "C8": priority(1),
        },
        "C5": {"C6": priority(1), "C7": priority(1), "C8": priority(3)},
        "C6": {"C7": priority(3, False), "C8": priority(5, False)},
        "C7": {"C8": priority(1)},
    },
    {"silent": True},
)
criteria = ahp_method.to_criteria()
alternatives = AlternativeModel(
    data={
        "Infinity 8 Bali": [5, 1, 5, 2, 1, 2, 2, 2],
        "Episode Kuta Bali": [9, 1, 5, 2, 2, 2, 2, 2],
        "Fairfield by Marriott Bali Kuta Sunset Road": [10, 2, 5, 2, 1, 2, 2, 1],
        "Luminor Hotel Legian Seminyak Bali": [8, 2, 5, 2, 1, 1, 2, 2],
        "Grandmas Plus Hotel Legian": [3, 2, 5, 2, 1, 1, 1, 2],
        "Grandmas Plus Hotel Airport": [3, 1, 5, 2, 1, 1, 1, 2],
        "Choice Stay Hotel Denpasar": [5, 2, 3, 2, 1, 2, 3, 2],
        "Daun Bali Seminyak Hotel": [9, 1, 5, 2, 1, 1, 2, 2],
        "Quest San Denpasar by ASTON": [10, 1, 5, 2, 1, 1, 1, 2],
        "PassGo Digital Airport Hotel Bali": [4, 2, 1, 2, 1, 1, 1, 2],
        "Yans House Hotel Kuta": [4, 2, 5, 2, 2, 2, 2, 2],
        "Aralea CoLiving": [4, 3, 5, 2, 2, 1, 1, 2],
        "Paripadi Studio Canggu": [8, 3, 4, 2, 1, 2, 2, 2],
        "Kamaniiya Petitenget Seminyak": [7, 1, 5, 2, 1, 1, 2, 2],
        "Black Lava Camp Kintamani": [10, 1, 5, 2, 1, 1, 1, 2],
        "Sari Villa Ubud": [4, 2, 4, 2, 1, 1, 1, 2],
        "Cove Vin Stay Petanu": [3, 1, 3, 2, 1, 1, 1, 1],
        "The Alea Hotel Seminyak": [2, 1, 3, 2, 1, 1, 1, 1],
        "Kuta Paradiso Hotel": [4, 3, 3, 1, 1, 1, 1, 1],
        "Abian Srama Hotel and Spa": [4, 1, 2, 2, 1, 1, 1, 1],
    },
    criteria=criteria,
)

moora_method = Moora(alternatives, {"silent": False})
moora_method.evaluate()

electre_method = Electre(alternatives, {"silent": True})
electre_method.evaluate()


