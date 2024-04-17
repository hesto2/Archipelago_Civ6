from typing import Optional
from BaseClasses import Location, Region

CIV_VI_AP_LOCATION_ID_BASE = 5041000


class CivVILocationData():
    game: str = "Civilization VI"
    cost: int
    uiTreeRow: int
    civ_id: int
    code: int
    era_type: str

    def __init__(self, name: str, cost: int, uiTreeRow: int, id: int, era_type: str = "ERA_ANCIENT"):
        self.name = name
        self.cost = cost
        self.uiTreeRow = uiTreeRow
        self.civ_id = id
        self.code = id + CIV_VI_AP_LOCATION_ID_BASE
        self.era_type = era_type

class CivVILocation(Location):
  game: str = "Civilization VI"


ancient_era = {
    "AP1": CivVILocationData("AP1", 25, 0, 1),
    "AP2": CivVILocationData("AP2", 25, 1, 2),
    "AP3": CivVILocationData("AP3", 25, 2, 3),
    "AP4": CivVILocationData("AP4", 50, 0, 4),
    "AP5": CivVILocationData("AP5", 50, 1, 5),
    "AP6": CivVILocationData("AP6", 50, 2, 6),
    "AP7": CivVILocationData("AP7", 50, 3, 7),
    "AP8": CivVILocationData("AP8", 50, 4, 8),
    "AP9": CivVILocationData("AP9", 80, 0, 9),
    "AP10": CivVILocationData("AP10", 80, 1, 10),
    "AP11": CivVILocationData("AP11", 80, 2, 11),
}

location_table = {**ancient_era}
