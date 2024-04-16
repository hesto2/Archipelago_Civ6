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


ancient_era_item_table: Dict[str, ItemData] = {
  "Pottery": ItemData("Pottery", 0),
  "Animal Husbandry": ItemData("Animal Husbandry", 1),
  "Mining": ItemData("Mining", 2),
  "Sailing": ItemData("Sailing", 3, ItemClassification.progression),
  "Astrology": ItemData("Astrology", 4, ItemClassification.progression),
  "Irrigation": ItemData("Irrigation", 5),
  "Archery": ItemData("Archery", 6),
  "Writing": ItemData("Writing", 7, ItemClassification.progression),
  "Masonry": ItemData("Masonry", 8),
  "Bronze Working": ItemData("Bronze Working", 9, ItemClassification.progression),
  "Wheel": ItemData("Wheel", 10),
}

item_table: Dict[str, ItemData] = {**ancient_era_item_table}
