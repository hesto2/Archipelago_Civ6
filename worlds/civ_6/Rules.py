from typing import Callable, Union, Dict, Set

from BaseClasses import MultiWorld
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import add_rule


def set_rules(multiworld: MultiWorld, player, locations):
    access_rules = {
        "AP_1": lambda _state: True,
        "AP_2": lambda _state: True,
        "AP_3": lambda _state: True,
        "AP_4": lambda _state: True,
        "AP_5": lambda _state: True,
        "AP_6": lambda _state: True,
        "AP_7": lambda _state: True,
        "AP_8": lambda _state: True,
        "AP_9": lambda _state: True,
        "AP_10": lambda _state: True,
    }
    for i in locations:
        location = multiworld.get_location(i, player)
        try:
            add_rule(location, access_rules[i])
        except KeyError:
            continue


class CivVILogic(LogicMixin):
    def has_tech(self, player: int, tech: str) -> bool:
        return self.has(tech, player)
