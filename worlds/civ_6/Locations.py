import os
from typing import Dict, List, Optional
from BaseClasses import Location, Region
import json
from enum import Enum

CIV_VI_AP_LOCATION_ID_BASE = 5041000


class EraType(Enum):
    ERA_ANCIENT = "ERA_ANCIENT"
    ERA_CLASSICAL = "ERA_CLASSICAL"
    ERA_MEDIEVAL = "ERA_MEDIEVAL"
    ERA_RENAISSANCE = "ERA_RENAISSANCE"
    ERA_INDUSTRIAL = "ERA_INDUSTRIAL"
    ERA_MODERN = "ERA_MODERN"
    ERA_ATOMIC = "ERA_ATOMIC"
    ERA_INFORMATION = "ERA_INFORMATION"
    ERA_FUTURE = "ERA_FUTURE"


class CivVILocationData():
    game: str = "Civilization VI"
    cost: int
    uiTreeRow: int
    civ_id: int
    code: int
    era_type: EraType

    def __init__(self, name: str, cost: int, uiTreeRow: int, id: int, era_type: EraType):
        self.name = name
        self.cost = cost
        self.uiTreeRow = uiTreeRow
        self.civ_id = id
        self.code = id + CIV_VI_AP_LOCATION_ID_BASE
        self.era_type = era_type


class CivVILocation(Location):
    game: str = "Civilization VI"


def generate_location_table():
    """
    Uses the data from existing_tech.json to generate a location table in the following format:
    {
      "ERA_ANCIENT": {
        "TECH_AP0": CivVILocationData,
        "TECH_AP1": CivVILocationData,
      },
      ...
    }
    """
    # Generate Techs
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    existing_tech_path = os.path.join(
        current_directory, 'data', 'existing_tech.json')

    with open(existing_tech_path) as f:
        existing_data = json.load(f)
    era_techs = {}

    i = 0
    for data in existing_data:
        era_type = data['EraType']
        if era_type not in era_techs:
            era_techs[era_type] = {}
        ap_name = f'TECH_AP{i}'
        era_techs[era_type][ap_name] = CivVILocationData(
            ap_name, data['Cost'], data['UITreeRow'], i, era_type)
        i += 1

    location_table = era_techs

    return location_table
