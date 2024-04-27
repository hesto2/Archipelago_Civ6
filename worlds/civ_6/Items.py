from enum import Enum
import json
import os
from typing import Dict, List
from BaseClasses import Item, ItemClassification
from worlds.civ_6.Enum import CivVICheckType
CIV_VI_AP_ITEM_ID_BASE = 5041000


class CivVIItem(Item):
    game: str = "Civilization VI"
    civ_vi_id: int
    item_type: CivVICheckType

    def __init__(self, name: str, classification: ItemClassification, civ_vi_id: int | None, player: int):
        super().__init__(name, classification, civ_vi_id + CIV_VI_AP_ITEM_ID_BASE, player)
        if name.split("_")[0] == "TECH":
            self.item_type = CivVICheckType.TECH
        elif name.split("_")[0] == "CIVIC":
            self.item_type = CivVICheckType.CIVIC


class CivVIItemData:
    civ_vi_id: int
    classification: ItemClassification
    name: str
    code: int
    cost: int
    item_type: CivVICheckType

    def __init__(self, name, civ_vi_id: int, cost: int,  item_type: CivVICheckType, id_offset: int = 0, classification: ItemClassification = ItemClassification.useful,):
        self.classification = classification
        self.civ_vi_id = civ_vi_id
        self.name = name
        self.code = civ_vi_id + CIV_VI_AP_ITEM_ID_BASE + id_offset
        self.cost = cost
        self.item_type = item_type


def generate_flat_item_table():
    """
    Generates a flat item table using the data from existing_tech.json and existing_civics.json.
    The table is a dictionary with item names as keys and CivVIItemData objects as values.
    """

    era_items = generate_item_by_era_table()
    flat_items = {}
    for era_type, era_items in era_items.items():
        for item_id, item_data in era_items.items():
            flat_items[item_id] = item_data
    return flat_items


def generate_item_by_era_table():
    """
    Uses the data from existing_tech.json to generate a location table in the following format:
    {
      "ERA_ANCIENT": {
        "TECH_POTTERY": ItemData,
        "TECH_ANIMAL_HUSBANDRY": ItemData,
        "CIVIC_CODE_OF_LAWS": ItemData,
        "CIVIC_CRAFTSMANSHIP": ItemData
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

    file_path = os.path.join(os.path.dirname(
        __file__), 'data/era_required_items.json')
    required_items: List[str] = []
    with open(file_path) as file:
        era_required_items = json.load(file)
        for key, value in era_required_items.items():
            required_items += value

    era_items = {}

    id_base = 0
    for tech in existing_techs:
        era_type = tech['EraType']
        if era_type not in era_items:
            era_items[era_type] = {}

        classification = ItemClassification.progression if tech[
            "Type"] in required_items else ItemClassification.useful
        era_items[era_type][tech["Type"]] = CivVIItemData(
            tech["Type"], id_base, tech["Cost"], CivVICheckType.TECH, 0, classification)

        id_base += 1

    # Generate Civics
    existing_civics_path = os.path.join(
        current_directory, 'data', 'existing_civics.json')
    civic_id_base = 0
    with open(existing_civics_path) as f:
        existing_civics = json.load(f)
    for civic in existing_civics:
        era_type = civic['EraType']
        if era_type not in era_items:
            era_items[era_type] = {}

        classification = ItemClassification.progression if civic[
            "Type"] in required_items else ItemClassification.useful
        era_items[era_type][civic["Type"]] = CivVIItemData(
            civic["Type"], civic_id_base, civic["Cost"], CivVICheckType.CIVIC, id_base, classification)

        civic_id_base += 1

    return era_items
