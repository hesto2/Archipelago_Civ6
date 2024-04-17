import os
from typing import List
import zipfile
from BaseClasses import Location, MultiWorld
from worlds.Files import APContainer
import json
import uuid


# Python fstrings don't allow backslashes, so we use this workaround
nl = "\n"
tab = "\t"
apo = "\'"


class CivVIContainer(APContainer):
    game: str = "Civilization VI"

    def __init__(self, patch_data: dict, base_path: str, output_directory: str,
                 player=None, player_name: str = "", server: str = ""):
        self.patch_data = patch_data
        self.file_path = base_path
        container_path = os.path.join(output_directory, base_path + ".zip")
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        for filename, yml in self.patch_data.items():
            opened_zipfile.writestr(filename, yml)
        super().write_contents(opened_zipfile)


def generate_modinfo(multiworld: MultiWorld) -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<Mod id="{uuid.uuid4()}" version="1">
  <Properties>
    <Name>Archipelago</Name>
    <Teaser>Mod for Archipelago Multiworld</Teaser>
    <Description>This mod disables the ability for players to research their own tech tree and instead provides Archipelago-specific techs that can be researched.</Description>
    <Authors>Hesto2</Authors>
  </Properties>

  <Files>
    <File>NewTechnologies.xml</File>
    <File>NewTechPrereqs.xml</File>
    <File>UpdateTechs.sql</File>
    <File>Code.sql</File>
  </Files>
  <InGameActions>
    <UpdateDatabase id="ArchipelagoTech">
      <File>NewTechnologies.xml</File>

      <!-- Needs to Be over 200 to work with Real Tech Tree -->
      <Properties>
        <LoadOrder>212</LoadOrder>
      </Properties>

      <File>UpdateTechs.sql</File>
      <File>NewTechPrereqs.xml</File>
    </UpdateDatabase>
  </InGameActions>
</Mod>
        """

def generate_new_technologies(world) -> str:
    locations = world.multiworld.get_filled_locations(world.player)
# fmt: off
    return f"""<?xml version="1.0" encoding="utf-8"?>
<GameInfo>
  <Types>
  {"".join([f'{tab}<Row Type="{location.name}" Kind="KIND_TECH" />{nl}' for
           location in locations])}
  </Types>
  <Technologies>
{"".join([f'{tab}<Row TechnologyType="{location.name}" '
               f'Name="{world.multiworld.player_name[location.item.player]}{apo}s '
               f'{location.item.name}" '
               f'EraType="{world.location_table[location.name].era_type}" '
               f'UITreeRow="{world.location_table[location.name].uiTreeRow}" '
               f'Cost="{world.location_table[location.name].cost}" '
               f'AdvisorType="ADVISOR_GENERIC" />{nl}'
               for location in locations])}
  </Technologies>
</GameInfo>
    """
# fmt: on


def generate_tech_prereqs(world) -> str:
    locations = world.multiworld.get_filled_locations(world.player)
# fmt: off
    return f"""<?xml version="1.0" encoding="utf-8"?>
  <GameData>
    <TechnologyPrereqs>
      <!--ERA_ANCIENT-->
{"".join([f'{tab}<Row Technology="TECH_AP{world.location_table[location.name].civ_id}" '
          f'PrereqTech="TECH_AP'
          f'{world.location_table[location.name].civ_id - 1}" />{nl}'
          for location in locations
          if world.location_table[location.name].civ_id != 0 and world.location_table[location.name].civ_id != 5])}
    </TechnologyPrereqs>
  </GameData>
  """
# fmt: on

def generate_update_techs() -> str:
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    existing_tech_path = os.path.join(
        current_directory, 'data', 'existing_tech.json')
    with open(existing_tech_path) as f:
        data = json.load(f)

        sql_statements = ""

        # fmt: off
        for tech in data:
            # Generate the SQL update statements for UITreeRow and Cost
            sql_statements += f"UPDATE Technologies{nl}SET UITreeRow= {tech['UITreeRow']}{nl}WHERE TechnologyType ='{tech['Type']}';{nl}"
            sql_statements += f"UPDATE Technologies{nl}SET Cost = {tech['Cost']}{nl}WHERE TechnologyType ='{tech['Type']}';{nl}--{nl}"
        # fmt: on
    return sql_statements
