import typing
from enum import Enum
from Utils import visualize_regions

from BaseClasses import MultiWorld, Region, Entrance
from worlds.AutoWorld import World
from worlds.civ_6.Enum import EraType
from worlds.civ_6.Locations import CivVILocation
from .Options import CivVIOptions


def create_regions(world: World, options: CivVIOptions, player: int):
    menu = Region("Menu", player, world.multiworld)
    world.multiworld.regions.append(menu)

    regions: typing.List[Region] = []
    for era in EraType:
        era_region = Region(era.value, player, world.multiworld)
        era_locations = {location.name: location.code for key,
                         location in world.location_by_era[era.value].items()}
        era_region.add_locations(era_locations, CivVILocation)

        regions.append(era_region)
        world.multiworld.regions.append(era_region)

    def get_count_required(era: EraType):
        # TODO: Add player option for checking how many items from previous era are expected to be found rather than 75%
        pct_previous_era_required = 1
        total = len(world.item_name_groups[era.value])
        return int(total *
                   pct_previous_era_required)

    menu.connect(world.get_region(EraType.ERA_ANCIENT.value))
    world.get_region(EraType.ERA_ANCIENT.value).connect(
        world.get_region(EraType.ERA_CLASSICAL.value), None, lambda state: state.has_group(EraType.ERA_ANCIENT.value, player, get_count_required(EraType.ERA_ANCIENT)))

    world.get_region(EraType.ERA_CLASSICAL.value).connect(
        world.get_region(EraType.ERA_MEDIEVAL.value), None, lambda state: state.has_group(EraType.ERA_CLASSICAL.value, player, get_count_required(EraType.ERA_CLASSICAL)))

    world.get_region(EraType.ERA_MEDIEVAL.value).connect(
        world.get_region(EraType.ERA_RENAISSANCE.value), None, lambda state: state.has_group(EraType.ERA_MEDIEVAL.value, player, get_count_required(EraType.ERA_MEDIEVAL)))

    world.get_region(EraType.ERA_RENAISSANCE.value).connect(
        world.get_region(EraType.ERA_INDUSTRIAL.value), None, lambda state: state.has_group(EraType.ERA_RENAISSANCE.value, player, get_count_required(EraType.ERA_RENAISSANCE)))

    world.get_region(EraType.ERA_INDUSTRIAL.value).connect(
        world.get_region(EraType.ERA_MODERN.value), None, lambda state: state.has_group(EraType.ERA_INDUSTRIAL.value, player, get_count_required(EraType.ERA_INDUSTRIAL)))

    world.get_region(EraType.ERA_MODERN.value).connect(
        world.get_region(EraType.ERA_ATOMIC.value), None, lambda state: state.has_group(EraType.ERA_MODERN.value, player, get_count_required(EraType.ERA_MODERN)))

    world.get_region(EraType.ERA_ATOMIC.value).connect(
        world.get_region(EraType.ERA_INFORMATION.value), None, lambda state: state.has_group(EraType.ERA_ATOMIC.value, player, get_count_required(EraType.ERA_ATOMIC)))

    world.get_region(EraType.ERA_INFORMATION.value).connect(
        world.get_region(EraType.ERA_FUTURE.value), None, lambda state: state.has_group(EraType.ERA_INFORMATION.value, player, get_count_required(EraType.ERA_INFORMATION)))
