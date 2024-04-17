import json
import os
from typing import Dict
from BaseClasses import Item, ItemClassification
CIV_VI_AP_ITEM_ID_BASE = 5041000


class CivVIItem(Item):
    game: str = "Civilization VI"
    civ_vi_id: int

    def __init__(self, name: str, classification: ItemClassification, civ_vi_id: int | None, player: int):
        super().__init__(name, classification, civ_vi_id + CIV_VI_AP_ITEM_ID_BASE, player)


class ItemData:
    civ_vi_id: int
    classification: ItemClassification
    name: str
    code: int

    def __init__(self, name, civ_vi_id: int, classification: ItemClassification = ItemClassification.useful):
        self.classification = classification
        self.civ_vi_id = civ_vi_id
        self.name = name
        self.code = civ_vi_id + CIV_VI_AP_ITEM_ID_BASE

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
        existing_data = json.load(f)
    era_techs = {}

    i = 0
    for data in existing_data:
        era_type = data['EraType']
        if era_type not in era_techs:
            era_techs[era_type] = {}
        era_techs[era_type][data["Type"]] = ItemData(data["Type"], i)
        i += 1

    item_table = era_techs

    return item_table
