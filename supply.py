"""
To store constants, hashmaps and classes relating to supplies (weights, costs and attributed names)
Classes involving list of Supplies including supply count, and SupplyOrder structure to store net weight and cost.
"""

# Two separate hashmaps which stores supply cost and weight.
SUPPLY_WEIGHT: dict[str, float] = {
    "Scalpel": 0.1,
    "Nitrous Oxide Canister": 1.8,
    "Stitches":	0.2,
    "Syringe": 0.05,
    "Vaccination Kit": 0.5,
    "Masks": 0.01,
    "Soap":	0.1,
    "Sanitiser": 0.95,
    "Bandages": 0.25,
    "Sticker": 0.001,
    "Stethoscope": 0.18,
    "Dialysis Machine": 150.0
}
SUPPLY_COST: dict[str, float] = {
    "Scalpel": 24.0,
    "Nitrous Oxide Canister": 80.0,
    "Stitches":	15.0,
    "Syringe": 0.2,
    "Vaccination Kit": 40.0,
    "Masks": 0.15,
    "Soap":	2.5,
    "Sanitiser": 15.0,
    "Bandages": 8.50,
    "Sticker": 0.03,
    "Stethoscope": 170.50,
    "Dialysis Machine": 1_604.00
}
SUPPLY_NAMES: list[str] = {"".join(supply.lower().split()): supply for supply in SUPPLY_WEIGHT.keys()}

class Supplies:
    def __init__(self, **kwargs):
        self.net_weight = 0
        self.net_value = 0
        self._supplies: dict[str, int] = {}
        for supply, count in kwargs.items():
            if supply not in SUPPLY_NAMES:
                continue
            setattr(self, supply, count)
            supply = SUPPLY_NAMES[supply]
            self.net_weight += SUPPLY_WEIGHT[supply] * count
            self.net_value += SUPPLY_COST[supply] * count
            self._supplies[supply] = count
    
    def __str__(self) -> str:
        s = ""
        for supply in self._supplies:
            count = self._supplies[supply]
            s += f"{count}x {supply}, "
        return s[:-2]
    
    def dict(self) -> dict:
        return self._supplies
    
    def add(self, supply: str, count: int):
        supply = "".join(supply.lower().split())
        if supply not in SUPPLY_NAMES:
            return
        setattr(self, supply, count)
        supply = SUPPLY_NAMES[supply]
        self.net_weight += SUPPLY_WEIGHT[supply] * count
        self.net_value += SUPPLY_COST[supply] * count
        if supply in self._supplies:
            self._supplies[supply] += count
            return
        self._supplies[supply] = count

    def remove(self, supply: str, count: int):
        supply = "".join(supply.lower().split())
        if supply not in SUPPLY_NAMES:
            return
        if SUPPLY_NAMES[supply] not in self._supplies:
            return
        setattr(self, supply, count)
        supply = SUPPLY_NAMES[supply]
        self._supplies[supply] -= count
        self.net_weight -= SUPPLY_WEIGHT[supply] * count
        self.net_value -= SUPPLY_COST[supply] * count

    def copy(self) -> "Supplies":
        return Supplies(**self._supplies)

class SupplyOrder:
    def __init__(self, **kwargs):
        self.supplies = Supplies()
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def is_empty(self) -> bool:
        d = self.supplies.dict()
        for supply in d:
            if d[supply] != 0:
                return False
        return True

    @property
    def net_weight(self) -> float:
        return self.supplies.net_weight

    @property
    def net_value(self) -> float:
        return self.supplies.net_value

    def dict(self) -> dict:
        return self.supplies._supplies
    
    def contains(self, supply: str) -> bool:
        return supply in self.supplies._supplies

    def copy(self) -> "SupplyOrder":
        return SupplyOrder(town=self.town, supplies=self.supplies)
