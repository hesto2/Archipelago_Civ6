import typing
from enum import Enum

from BaseClasses import MultiWorld, Region, Entrance
from worlds.civ_6.Locations import CivVILocation
from .Options import CivVIOptions

def create_regions(world, options: CivVIOptions, player: int):
  menu = Region("Menu", player, world.multiworld, "Menu")
  world.multiworld.regions.append(menu)

  main_region = Region("Main", player, world.multiworld )
  main_region.add_locations(world.location_table, CivVILocation)

  world.multiworld.regions.append(main_region)

  menu.connect(main_region)