from dataclasses import dataclass
from Options import DeathLink, PerGameCommonOptions


@dataclass
class CivVIOptions(PerGameCommonOptions):
    death_link: DeathLink