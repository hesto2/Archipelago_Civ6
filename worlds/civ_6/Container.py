from dataclasses import dataclass
import os
from typing import List
import zipfile
from BaseClasses import MultiWorld
from worlds.Files import APContainer
import uuid

from worlds.civ_6.Enum import CivVICheckType
from worlds.civ_6.Locations import CivVILocation


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
    <CompatibleVersions>2.0</CompatibleVersions>
  </Properties>

  <Files>
    <File>NewItems.xml</File>
    <File>NewPrereqs.xml</File>
    <File>ResearchChooser.lua</File>
    <File>ResearchChooser.xml</File>
    <File>CivicsChooser.lua</File>
    <File>CivicsChooser.xml</File>
    <File>TechTree.lua</File>
    <File>TechTree.xml</File>
    <File>CivicsTree.lua</File>
    <File>CivicsTree.xml</File>
    <File>TechTreeNode.xml</File>
    <File>ArchipelagoRunner.lua</File>
    <File>ArchipelagoIcons.xml</File>
    <File>AllowBuildObsolete.sql</File>
    <File>GovernmentScreen.lua</File>
    <File>ActionPanel.lua</File>
  </Files>
  <InGameActions>
    <UpdateDatabase id="ArchipelagoItems">
      <File>NewItems.xml</File>
      <Properties>
        <LoadOrder>212</LoadOrder>
      </Properties>

      <File>NewPrereqs.xml</File>
    </UpdateDatabase>
    <UpdateDatabase id="ArchipelagoObsoleteUnits">
      <File>AllowBuildObsolete.sql</File>

    </UpdateDatabase>
    <ImportFiles id="ArchipelagoReplacers">
      <Properties>
        <LoadOrder>150000</LoadOrder>
      </Properties>
      <File>ResearchChooser.lua</File>
      <File>ResearchChooser.xml</File>
      <File>CivicsChooser.lua</File>
      <File>CivicsChooser.xml</File>

      <File>TechTree.lua</File>
      <File>TechTree.xml</File>
      <File>CivicsTree.lua</File>
      <File>CivicsTree.xml</File>
      <File>TechTreeNode.xml</File>

      <File>GovernmentScreen.lua</File>
      <File>ActionPanel.lua</File>

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
    <ReplaceUIScript id="Archipelago_ResearchChooser">
      <Properties>
        <LoadOrder>150002</LoadOrder>
        <LuaContext>CivicsChooser</LuaContext>
        <LuaReplace>CivicsChooser.lua</LuaReplace>
      </Properties>
    </ReplaceUIScript>
    <ReplaceUIScript id="Archipelago_CivicsTree">
      <Properties>
        <LoadOrder>150003</LoadOrder>
        <LuaContext>CivicsTree</LuaContext>
        <LuaReplace>CivicsTree.lua</LuaReplace>
      </Properties>
    </ReplaceUIScript>
    <ReplaceUIScript id="Archipelago_GovernmentScreen">
      <Properties>
        <LoadOrder>150004</LoadOrder>
        <LuaContext>GovernmentScreen</LuaContext>
        <LuaReplace>GovernmentScreen.lua</LuaReplace>
      </Properties>
    </ReplaceUIScript>
    <ReplaceUIScript id="Archipelago_ActionPanel">
      <Properties>
        <LoadOrder>150005</LoadOrder>
        <LuaContext>ActionPanel</LuaContext>
        <LuaReplace>ActionPanel.lua</LuaReplace>
      </Properties>
    </ReplaceUIScript>

    <AddGameplayScripts id="ArchipelagoScripts">
      <File>ArchipelagoRunner.lua</File>
    </AddGameplayScripts>
    <UpdateIcons id="icons">
      <File>ArchipelagoIcons.xml</File>
    </UpdateIcons>
  </InGameActions>
</Mod>
        """


def generate_new_items(world) -> str:
    """
    Generates the XML for the new techs/civics as well as the blockers used to prevent players from researching their own items
    """
    locations: List[CivVILocation] = world.multiworld.get_filled_locations(
        world.player)
    techs = [location for location in locations if location.location_type ==
             CivVICheckType.TECH]
    civics = [location for location in locations if location.location_type ==
              CivVICheckType.CIVIC]
# fmt: off
    return f"""<?xml version="1.0" encoding="utf-8"?>
<GameInfo>
  <Types>
    <Row Type="TECH_BLOCKER" Kind="KIND_TECH" />
    <Row Type="CIVIC_BLOCKER" Kind="KIND_CIVIC" />
  {"".join([f'{tab}<Row Type="{tech.name}" Kind="KIND_TECH" />{nl}' for
           tech in techs])}
  {"".join([f'{tab}<Row Type="{civic.name}" Kind="KIND_CIVIC" />{nl}' for
           civic in civics])}
  </Types>
  <Technologies>
      <Row TechnologyType="TECH_BLOCKER" Name="TECH_BLOCKER" EraType="ERA_ANCIENT" UITreeRow="0" Cost="9999" AdvisorType="ADVISOR_GENERIC" Description="Archipelago Tech created to prevent players from researching their own tech"/>
{"".join([f'{tab}<Row TechnologyType="{location.name}" '
               f'Name="{world.multiworld.player_name[location.item.player]}{apo}s '
               f'{location.item.name}" '
               f'EraType="{world.location_table[location.name].era_type}" '
               f'UITreeRow="{world.location_table[location.name].uiTreeRow}" '
               f'Cost="{world.location_table[location.name].cost}" '
               f'Description="{location.name}" '
               f'AdvisorType="ADVISOR_GENERIC" />{nl}'
               for location in techs])}
  </Technologies>
  <Civics>
      <Row CivicType="CIVIC_BLOCKER" Name="CIVIC_BLOCKER" EraType="ERA_ANCIENT" UITreeRow="0" Cost="9999" AdvisorType="ADVISOR_GENERIC" Description="Archipelago Civic created to prevent players from researching their own civics"/>
{"".join([f'{tab}<Row CivicType="{location.name}" '
               f'Name="{world.multiworld.player_name[location.item.player]}{apo}s '
               f'{location.item.name}" '
               f'EraType="{world.location_table[location.name].era_type}" '
               f'UITreeRow="{world.location_table[location.name].uiTreeRow}" '
               f'Cost="{world.location_table[location.name].cost}" '
               f'Description="{location.name}" '
               f'AdvisorType="ADVISOR_GENERIC" />{nl}'
               for location in civics])}
  </Civics>
</GameInfo>
    """
# fmt: on