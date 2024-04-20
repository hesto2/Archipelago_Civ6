"""
Usage: python Tools.py <function_name> <args>
generate_new_techs: Generates AP techs based on the index of the existing techs in the game. Defaults to putting them in ./data/new_tech.json
  args: file_path (optional), output_file (optional)
generate_new_prereqs: Copies the existing prereqs but changes out the names for the associated AP techs
  args: file_path (optional), output_file (optional)
"""
import json
import sys
from typing import List
import os


def generate_new_techs(file_path, output_file):
    """Generates AP techs based on the index of the existing techs in the game. Defaults to putting them in ./data/new_tech.json"""
    with open(file_path, 'r') as file:
        data = json.load(file)

    with open(output_file, 'w') as output:
        i = 0
        output.write("[\n")
        for item in data:
            # write the item contents to the output file as a json but change the name to be "TECH_AP{index}"
            output.write(json.dumps({"Type": f"TECH_AP{i}", "Cost": item["Cost"],
                         "UITreeRow": item["UITreeRow"], "EraType": item["EraType"]}))
            if i != len(data) - 1:
                output.write(",\n")
            else:
                output.write("\n")
            i += 1
        output.write("]")


def generate_new_prereqs(file_path, output_file):
    """Copies the existing prereqs but changes out the names for the associated AP techs"""
    with open(file_path, 'r') as file:
        prereq_data = json.load(file)

    with open("./data/new_tech.json", 'r') as file:
        new_tech = json.load(file)

    with open("./data/existing_tech.json", 'r') as file:
        existing_tech = json.load(file)

    with open(output_file, 'w') as output:
        i = 0
        output.write("[\n")
        for item in prereq_data:
            output.write(json.dumps({"Technology": find_new_tech_based_on_existing_name(
                item["Technology"], existing_tech, new_tech), "PrereqTech": find_new_tech_based_on_existing_name(item["PrereqTech"], existing_tech, new_tech)}))

            if i != len(prereq_data) - 1:
                output.write(",\n")
            else:
                output.write("\n")
            i += 1
        output.write("]")


def find_new_tech_based_on_existing_name(existing_name: str, existing_tech: List[dict], new_tech: List[dict]) -> str:
    for i in range(len(existing_tech)):
        if existing_tech[i]["Type"] == existing_name:
            return new_tech[i]["Type"]
    return ""


# Allow this function to be run from the command line
if __name__ == "__main__":

    function_name = sys.argv[1]

    if function_name == "generate_new_techs":
        file_path = "./data/existing_tech.json"
        output_file = "./data/new_tech.json"

        if len(sys.argv) > 2:
            file_path = sys.argv[2]
            output_file = sys.argv[3]
        generate_new_techs(file_path, output_file)

    elif function_name == "generate_new_prereqs":
        file_path = "./data/existing_prereqs.json"
        output_file = "./data/new_prereqs.json"

        if len(sys.argv) > 2:
            file_path = sys.argv[2]
            output_file = sys.argv[3]
        generate_new_prereqs(file_path, output_file)
