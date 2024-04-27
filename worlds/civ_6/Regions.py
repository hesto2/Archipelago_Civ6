import typing
from BaseClasses import CollectionState, Region
from worlds.AutoWorld import World
from worlds.civ_6.Enum import EraType
from worlds.civ_6.Locations import CivVILocation
from .Options import CivVIOptions
import json
import os


def get_cumulative_prereqs_for_era(end_era: EraType):
    """Gets the specific techs/civics that are required for the specified era as well as all previous eras"""
    cumulative_prereqs = []
    era_required_items = {}
    file_path = os.path.join(os.path.dirname(
        __file__), 'data/era_required_items.json')
    with open(file_path) as file:
        era_required_items = json.load(file)

    for era in EraType:
        cumulative_prereqs += era_required_items[era.value]
        if era == end_era:
            break
    return cumulative_prereqs


def has_required_items(state: CollectionState, era: EraType, player: int, has_progressive_items: bool):
    # If has progressive items, it will count how many progressive techs it should have, otherwise return the default array
    if has_progressive_items:
        file_path = os.path.join(os.path.dirname(
            __file__), 'data/progressive_districts.json')
        with open(file_path) as file:
            progressive_districts = json.load(file)
            required_counts: typing.Dict[str, int] = {}
            all_previous_items = get_cumulative_prereqs_for_era(era)
            for key, value in progressive_districts.items():
                required_counts[key] = 0
                for item in all_previous_items:
                    if item in value:
                        required_counts[key] += 1

            for key, value in required_counts.items():
                has_amount = state.has(key, player, required_counts[key])
                if not has_amount:
                    return False
            return True
    else:
        file_path = os.path.join(os.path.dirname(
            __file__), 'data/era_required_items.json')
        with open(file_path) as file:
            era_required_items = json.load(file)
            return state.has_all(era_required_items[era.value], player)


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
        # additional testing required
        # pct_previous_era_required = world.options.percent_of_era_items_required_for_next_era * .01
        pct_previous_era_required = .3
        total = len(world.item_name_groups[era.value])
        return int(total *
                   pct_previous_era_required)

    menu.connect(world.get_region(EraType.ERA_ANCIENT.value))

    world.get_region(EraType.ERA_ANCIENT.value).connect(
        world.get_region(EraType.ERA_CLASSICAL.value), None,
        lambda state:
        state.has_group(EraType.ERA_ANCIENT.value, player,
                        get_count_required(EraType.ERA_ANCIENT))
        and has_required_items(state, EraType.ERA_ANCIENT, player, options.progressive_districts.value)
    )

    world.get_region(EraType.ERA_CLASSICAL.value).connect(
        world.get_region(EraType.ERA_MEDIEVAL.value), None, lambda state: state.has_group(
            EraType.ERA_CLASSICAL.value, player, get_count_required(EraType.ERA_CLASSICAL))
        and has_required_items(state, EraType.ERA_CLASSICAL, player, options.progressive_districts.value)
    )

    world.get_region(EraType.ERA_MEDIEVAL.value).connect(
        world.get_region(EraType.ERA_RENAISSANCE.value), None, lambda state: state.has_group(
            EraType.ERA_MEDIEVAL.value, player, get_count_required(EraType.ERA_MEDIEVAL))
        and has_required_items(state, EraType.ERA_MEDIEVAL, player, options.progressive_districts.value)
    )

    world.get_region(EraType.ERA_RENAISSANCE.value).connect(
        world.get_region(EraType.ERA_INDUSTRIAL.value), None, lambda state: state.has_group(
            EraType.ERA_RENAISSANCE.value, player, get_count_required(EraType.ERA_RENAISSANCE))
        and has_required_items(state, EraType.ERA_RENAISSANCE, player, options.progressive_districts.value)
    )

    world.get_region(EraType.ERA_INDUSTRIAL.value).connect(
        world.get_region(EraType.ERA_MODERN.value), None, lambda state: state.has_group(
            EraType.ERA_INDUSTRIAL.value, player, get_count_required(EraType.ERA_INDUSTRIAL))
        and has_required_items(state, EraType.ERA_INDUSTRIAL, player, options.progressive_districts.value)
    )

    world.get_region(EraType.ERA_MODERN.value).connect(
        world.get_region(EraType.ERA_ATOMIC.value), None, lambda state: state.has_group(
            EraType.ERA_MODERN.value, player, get_count_required(EraType.ERA_MODERN))
        and has_required_items(state, EraType.ERA_MODERN, player, options.progressive_districts.value)
    )

    world.get_region(EraType.ERA_ATOMIC.value).connect(
        world.get_region(EraType.ERA_INFORMATION.value), None, lambda state: state.has_group(
            EraType.ERA_ATOMIC.value, player, get_count_required(EraType.ERA_ATOMIC))
        and has_required_items(state, EraType.ERA_ATOMIC, player, options.progressive_districts.value)
    )

    world.get_region(EraType.ERA_INFORMATION.value).connect(
        world.get_region(EraType.ERA_FUTURE.value), None, lambda state: state.has_group(
            EraType.ERA_INFORMATION.value, player, get_count_required(EraType.ERA_INFORMATION))
        and has_required_items(state, EraType.ERA_INFORMATION, player, options.progressive_districts.value))
