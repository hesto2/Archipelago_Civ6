from typing import Callable, Union, Dict, Set

from BaseClasses import MultiWorld
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import add_rule


def set_rules(multiworld: MultiWorld, player, locations):
    access_rules = {
        "AP1": lambda _state: True,
        "AP2": lambda _state: True,
        "AP3": lambda _state: True,
        "AP4": lambda _state: True,
        "AP5": lambda _state: True,
        "AP6": lambda _state: True,
        "AP7": lambda _state: True,
        "AP8": lambda _state: True,
        "AP9": lambda _state: True,
        "AP10": lambda _state: True,
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
