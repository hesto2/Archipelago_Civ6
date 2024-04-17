from typing import Callable, Union, Dict, Set

from BaseClasses import MultiWorld
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import add_rule


def set_rules(multiworld: MultiWorld, player, locations):
    access_rules = {
        "TECH_1": lambda _state: True,
        "TECH_2": lambda _state: True,
        "TECH_3": lambda _state: True,
        "TECH_4": lambda _state: True,
        "TECH_5": lambda _state: True,
        "TECH_6": lambda _state: True,
        "TECH_7": lambda _state: True,
        "TECH_8": lambda _state: True,
        "TECH_9": lambda _state: True,
        "TECH_10": lambda _state: True,
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
