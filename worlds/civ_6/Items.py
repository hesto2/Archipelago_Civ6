from enum import Enum
import json
import os
from typing import Dict
from BaseClasses import Item, ItemClassification
from worlds.civ_6.Enum import CivVICheckType
CIV_VI_AP_ITEM_ID_BASE = 5041000


class CivVIItem(Item):
    game: str = "Civilization VI"
    civ_vi_id: int

    def __init__(self, name: str, classification: ItemClassification, civ_vi_id: int | None, player: int):
        super().__init__(name, classification, civ_vi_id + CIV_VI_AP_ITEM_ID_BASE, player)


class CivVIItemData:
    civ_vi_id: int
    classification: ItemClassification
    name: str
    code: int
    cost: int
    item_type: CivVICheckType

    def __init__(self, name, civ_vi_id: int, cost: int,  item_type: CivVICheckType, classification: ItemClassification = ItemClassification.progression,):
        self.classification = classification
        self.civ_vi_id = civ_vi_id
        self.name = name
        self.code = civ_vi_id + CIV_VI_AP_ITEM_ID_BASE
        self.cost = cost
        self.item_type = item_type


def generate_item_table():
    """
    Uses the data from existing_tech.json to generate a location table in the following format:
    {
      "ERA_ANCIENT": {
        "TECH_POTTERY": ItemData,
        "TECH_ANIMAL_HUSBANDRY": ItemData
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
        existing_techs = json.load(f)
    era_techs = {}

    i = 0
    for tech in existing_techs:
        era_type = tech['EraType']
        if era_type not in era_techs:
            era_techs[era_type] = {}
        era_techs[era_type][tech["Type"]] = CivVIItemData(
            tech["Type"], i, tech["Cost"], CivVICheckType.TECH)
        i += 1

    item_table = era_techs

    return item_table
