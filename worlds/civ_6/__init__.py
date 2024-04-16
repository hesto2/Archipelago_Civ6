import typing
from .Items import item_table, CivVIItem
from .Locations import location_table
from .Options import CivVIOptions
from .Rules import set_rules
from .Regions import create_regions
from BaseClasses import Item, Tutorial
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

    item_name_to_id = {value.name: value.code for _name, value in item_table.items()}
    location_name_to_id = location_table

    data_version = 9
    required_client_version = (0, 4, 5)

    area_connections: typing.Dict[int, int]

    options_dataclass = CivVIOptions

    def create_regions(self):
        create_regions(self.multiworld, self.options, self.player)

    def set_rules(self):
      set_rules(self.multiworld, self.player, location_table.keys())

    def create_item(self, name: str) -> Item:
        item = item_table[name]
        return CivVIItem(name, item.classification, item.civ_vi_id, self.player)

    def create_items(self):
        for item in item_table:
            self.multiworld.itempool += [self.create_item(
                item)]

    def fill_slot_data(self):
        # TODO: Pass in selected options here
        return {
        }

    def generate_output(self, output_directory: str):
        data = {
            "slot_data": self.fill_slot_data(),
            "location_to_item": {self.location_name_to_id[i.name]: item_table[i.item.name] for i in self.multiworld.get_locations()},
            "data_package": {
                "data": {
                    "games": {
                        self.game: {
                            "item_name_to_id": self.item_name_to_id,
                            "location_name_to_id": self.location_name_to_id
                        }
                    }
                }
            }
        }
        # filename = f"{self.multiworld.get_out_file_name_base(
        #     self.player)}.apciv6"
        # with open(os.path.join(output_directory, filename), 'w') as f:
        #     json.dump(data, f)
