import json
import os
from typing import List


def get_flat_progressive_items():
    progressive_districts = get_progressive_districts()
    flat_progressive_techs = {}
    for key, value in progressive_districts.items():
        for item in value:
            flat_progressive_techs[item] = key
    return flat_progressive_techs


def get_progressive_districts():
    file_path = os.path.join(os.path.dirname(
        __file__), 'data/progressive_districts.json')
    with open(file_path) as file:
        progressive_districts = json.load(file)
    return progressive_districts


def convert_items_to_have_progression(items: List[str]):
    flat_progressive_techs = get_flat_progressive_items()
    new_list = []
    for item in items:
        if item in flat_progressive_techs.keys():
            new_list.append(flat_progressive_techs[item])
        else:
            new_list.append(item)
    return new_list
