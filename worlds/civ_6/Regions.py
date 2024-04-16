import typing
from enum import Enum

from BaseClasses import MultiWorld, Region, Entrance
from worlds.civ_6.Locations import CivVILocation
from .Options import CivVIOptions
from .Locations import location_table

def create_regions(world: MultiWorld, options: CivVIOptions, player: int):
  menu = Region("Menu", player, world, "Menu")
  world.regions.append(menu)

  main_region = Region("Main", player, world )
  main_region.add_locations(location_table, CivVILocation)

  world.regions.append(main_region)

  menu.connect(main_region)