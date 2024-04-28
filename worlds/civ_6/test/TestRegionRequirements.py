import json
import os
from worlds.civ_6.Enum import EraType
from . import CivVITestBase


class TestRegionRequirements(CivVITestBase):
    options = {
        "progressive_districts": False
    }

    def collect_items_for_era(self, era: EraType) -> None:
        file_path = os.path.join(os.path.dirname(
            __file__), '../data/era_required_items.json')
        with open(file_path) as file:
            era_required_items = json.load(file)
            self.collect_by_name(era_required_items[era.value])

    def test_eras_are_accessible_without_progressive_districts(self) -> None:
        state = self.multiworld.state
        for era in EraType:
            if era == EraType.ERA_ANCIENT:
                self.assertTrue(state.can_reach(
                    era.value, "Region", self.player))
            else:
                self.assertFalse(state.can_reach(
                    era.value, "Region", self.player))

        self.collect_items_for_era(EraType.ERA_ANCIENT)
        self.assertTrue(state.can_reach(
            EraType.ERA_CLASSICAL.value, "Region", self.player))

        self.collect_items_for_era(EraType.ERA_CLASSICAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_MEDIEVAL.value, "Region", self.player))

        self.collect_items_for_era(EraType.ERA_MEDIEVAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_RENAISSANCE.value, "Region", self.player))

        self.collect_items_for_era(EraType.ERA_RENAISSANCE)
        self.assertTrue(state.can_reach(
            EraType.ERA_INDUSTRIAL.value, "Region", self.player))

        self.collect_items_for_era(EraType.ERA_INDUSTRIAL)
        self.assertTrue(state.can_reach(
            EraType.ERA_MODERN.value, "Region", self.player))

        self.collect_items_for_era(EraType.ERA_MODERN)
        self.assertTrue(state.can_reach(
            EraType.ERA_ATOMIC.value, "Region", self.player))

        self.collect_items_for_era(EraType.ERA_ATOMIC)
        self.assertTrue(state.can_reach(
            EraType.ERA_INFORMATION.value, "Region", self.player))

        self.collect_items_for_era(EraType.ERA_INFORMATION)
        self.assertTrue(state.can_reach(
            EraType.ERA_FUTURE.value, "Region", self.player))

    def test_eras_are_accessible_with_progressive_districts(self) -> None:
        pass
