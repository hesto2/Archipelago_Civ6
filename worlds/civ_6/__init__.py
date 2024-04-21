import os
from typing import Dict

import Utils
from worlds.civ_6.Container import CivVIContainer, generate_modinfo, generate_new_technologies
from .Items import generate_item_table, CivVIItem
from .Locations import CivVILocationData, EraType, generate_location_table
from .Options import CivVIOptions
from .Regions import create_regions
from BaseClasses import Item, MultiWorld, Tutorial
from ..AutoWorld import World, WebWorld


class CivVIWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Civlization VI for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["hesto2"]
    )]


class CivVIWorld(World):
    """
    Civilization VI is a turn-based strategy video game in which one or more players compete alongside computer-controlled AI opponents to grow their individual civilization from a small tribe to control the entire planet across several periods of development.
    """

    game: str = "Civilization VI"
    topology_present = False

    web = CivVIWeb()

    item_name_to_id = {}
    location_name_to_id = {}

    data_version = 9
    required_client_version = (0, 4, 5)

    area_connections: Dict[int, int]

    options_dataclass = CivVIOptions
    location_by_era: Dict[EraType, Dict[str, CivVILocationData]]

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.location_by_era = generate_location_table()
        self.item_by_era = generate_item_table()
        self.item_name_groups = {}

        for era in EraType:
            self.item_name_groups[era.value] = [item.name for item in self.item_by_era[era.value].values()]


        self.location_table = {}
        self.item_table = {}

        for era, locations in self.location_by_era.items():
            for tech_name, location in locations.items():
                self.location_name_to_id[location.name] = location.code
                self.location_table[location.name] = location

        for era, items in self.item_by_era.items():
            for item_name, item in items.items():
                self.item_name_to_id[item.name] = item.code
                self.item_table[item.name] = item

    def create_regions(self):
        create_regions(self, self.options, self.player)

    def create_item(self, name: str) -> Item:
        item = self.item_table[name]
        return CivVIItem(name, item.classification, item.civ_vi_id, self.player)

    def create_items(self):
        for item in self.item_table:
            self.multiworld.itempool += [self.create_item(
                item)]

    def fill_slot_data(self):
        # TODO: Pass in selected options here
        return {
        }

    def generate_output(self, output_directory: str):
      # fmt: off
        mod_name = f"AP-{self.multiworld.get_file_safe_player_name(self.player)}"
      # fmt: on
        mod_dir = os.path.join(
            output_directory, mod_name + "_" + Utils.__version__)
        mod_files = {
            f"{mod_name}/Changes.modinfo": generate_modinfo(self.multiworld),
            f"{mod_name}/NewTechnologies.xml": generate_new_technologies(self),
        }


        # Add static mod files
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        static_mod_files_folder = os.path.join(
            current_directory, 'static_mod_files')
        static_mod_files = os.listdir(static_mod_files_folder)

        for file_name in static_mod_files:
          file_path = os.path.join(static_mod_files_folder, file_name)
          with open(file_path, 'r') as file:
            mod_files[f"{mod_name}/{file_name}"] = file.read()

        mod = CivVIContainer(mod_files, mod_dir, output_directory, self.player,
                             self.multiworld.get_file_safe_player_name(self.player))
        mod.write()