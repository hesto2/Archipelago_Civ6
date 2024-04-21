import os
from typing import Dict, List, Optional
from BaseClasses import Location
import json

from worlds.civ_6.Enum import CivVICheckType, EraType

CIV_VI_AP_LOCATION_ID_BASE = 5041000


class CivVILocationData():
    game: str = "Civilization VI"
    name: str
    cost: int
    uiTreeRow: int
    civ_id: int
    code: int
    era_type: EraType
    location_type: CivVICheckType
    pre_reqs: List[str]

    def __init__(self, name: str, cost: int, uiTreeRow: int, id: int, era_type: EraType, location_type: CivVICheckType, pre_reqs: Optional[List[str]] = None):
        self.name = name
        self.cost = cost
        self.uiTreeRow = uiTreeRow
        self.civ_id = id
        self.code = id + CIV_VI_AP_LOCATION_ID_BASE
        self.era_type = era_type
        self.pre_reqs = pre_reqs
        self.location_type = location_type


class CivVILocation(Location):
    game: str = "Civilization VI"


def format_tech_name(id: int) -> str:
    return f'TECH_AP{id}'


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
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    new_tech_prereq_path = os.path.join(
        current_directory, 'data', 'new_tech_prereqs.json')
    with open(new_tech_prereq_path) as f:
        new_tech_prereqs = json.load(f)

    new_tech_path = os.path.join(
        current_directory, 'data', 'new_tech.json')

    with open(new_tech_path) as f:
        new_techs = json.load(f)

    era_techs = {}

    i = 0
    for data in new_techs:
        era_type = data['EraType']
        if era_type not in era_techs:
            era_techs[era_type] = {}

        prereq_data = [
            item for item in new_tech_prereqs if item['Technology'] == data['Type']]

        era_techs[era_type][data["Type"]] = CivVILocationData(
            data["Type"], data['Cost'], data['UITreeRow'], i, era_type, CivVICheckType.TECH, prereq_data)
        i += 1

    return era_techs
