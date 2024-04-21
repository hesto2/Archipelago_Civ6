from dataclasses import dataclass
import os
import zipfile
from BaseClasses import MultiWorld
from worlds.Files import APContainer
import uuid


# Python fstrings don't allow backslashes, so we use this workaround
nl = "\n"
tab = "\t"
apo = "\'"


@dataclass
class CivTreeItem:
    name: str
    cost: int
    ui_tree_row: int


class CivVIContainer(APContainer):
    """
    Responsible for generating the mod files for the Civ VI multiworld
    """
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
    <Description>This mod disables the ability for players to research their own tech tree and
      instead provides Archipelago-specific techs that can be researched.</Description>
    <Authors>Hesto2</Authors>
  </Properties>

  <Files>
    <File>NewTechnologies.xml</File>
    <File>NewTechPrereqs.xml</File>
    <File>ResearchChooser.lua</File>
    <File>ResearchChooser.xml</File>
    <File>TechTree.lua</File>
    <File>TechTree.xml</File>
    <File>TechTreeNode.xml</File>
  </Files>
  <InGameActions>
    <UpdateDatabase id="ArchipelagoTech">
      <File>NewTechnologies.xml</File>
      <Properties>
        <LoadOrder>212</LoadOrder>
      </Properties>

      <File>NewTechPrereqs.xml</File>
    </UpdateDatabase>
    <ImportFiles id="ArchipelagoReplacers">
      <Properties>
        <LoadOrder>150000</LoadOrder>
      </Properties>
      <File>ResearchChooser.lua</File>
      <File>ResearchChooser.xml</File>

      <File>TechTree.lua</File>
      <File>TechTree.xml</File>

      <File>TechTreeNode.xml</File>
    </ImportFiles>
    <ReplaceUIScript id="Archipelago_ResearchChooser">
      <Properties>
        <LoadOrder>150000</LoadOrder>
        <LuaContext>ResearchChooser</LuaContext>
        <LuaReplace>ResearchChooser.lua</LuaReplace>
      </Properties>
    </ReplaceUIScript>
    <ReplaceUIScript id="Archipelago_TechTree">
      <Properties>
        <LoadOrder>150001</LoadOrder>
        <LuaContext>TechTree</LuaContext>
        <LuaReplace>TechTree.lua</LuaReplace>
      </Properties>
    </ReplaceUIScript>
  </InGameActions>
</Mod>
        """


def generate_new_technologies(world) -> str:
    """
    Generates the XML for the new techs as well as the tech blocker used to prevent humans from researching their own techs
    """
    locations = world.multiworld.get_filled_locations(world.player)
# fmt: off
    return f"""<?xml version="1.0" encoding="utf-8"?>
<GameInfo>
  <Types>
    <Row Type="TECH_BLOCKER" Kind="KIND_TECH" />
  {"".join([f'{tab}<Row Type="{location.name}" Kind="KIND_TECH" />{nl}' for
           location in locations])}
  </Types>
  <Technologies>
      <Row TechnologyType="TECH_BLOCKER" Name="TECH_BLOCKER" EraType="ERA_FUTURE" UITreeRow="0" Cost="9999" AdvisorType="ADVISOR_GENERIC" Description="Archipelago Tech created to prevent players from researching their own tech"/>
{"".join([f'{tab}<Row TechnologyType="{location.name}" '
               f'Name="{world.multiworld.player_name[location.item.player]}{apo}s '
               f'{location.item.name}" '
               f'EraType="{world.location_table[location.name].era_type}" '
               f'UITreeRow="{world.location_table[location.name].uiTreeRow}" '
               f'Cost="{world.location_table[location.name].cost}" '
               f'Description="{location.name}" '
               f'AdvisorType="ADVISOR_GENERIC" />{nl}'
               for location in locations])}
  </Technologies>
</GameInfo>
    """
# fmt: on