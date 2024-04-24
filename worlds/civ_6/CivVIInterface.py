from logging import Logger
from typing import List

from worlds.civ_6.Enum import CivVICheckType
from worlds.civ_6.Items import CivVIItemData
from worlds.civ_6.TunerClient import TunerClient, TunerConnectionException, TunerTimeoutException


class CivVIInterface:
    logger: Logger
    tuner: TunerClient

    def __init__(self, logger: Logger):
        self.logger = logger
        self.tuner = TunerClient(logger)

    def is_in_game(self) -> bool:
        command = "IsInGame()"
        try:
            result = self.tuner.send_game_command(command)
            return result == "true"
        except TunerTimeoutException:
            self.logger.info("Connected to game,  waiting for game to start")
            return False
        except TunerConnectionException:
            self.logger.info(
                "Not connected to game, waiting for connection to be available")
            return False

    def give_item_to_player(self, item: CivVIItemData, sender: str = ""):
      # fmt: off
        command = f"HandleReceiveItem({item.civ_vi_id}, \"{item.name}\", \"{item.item_type.value}\", \"{sender}\")"
      # fmt: on
        self.tuner.send_game_command(command)

    def resync(self) -> None:
        command = "Resync()"
        self.tuner.send_game_command(command)

    def get_checked_locations(self) -> List[str]:
        command = "GetUnsentCheckedLocations()"
        result = self.tuner.send_game_command(command)
        return result.split(",")

    def get_last_received_index(self) -> int:
        command = "ClientGetLastReceivedIndex()"
        result = self.tuner.send_game_command(command)
        return int(result)

    def send_notification(self, item: CivVIItemData, sender="someone") -> None:
      # fmt: off
        command = f"GameCore.NotificationManager:SendNotification(GameCore.NotificationTypes.USER_DEFINED_2, \"{item.name} Received\", \"You have received {item.name} from \" .. \"{sender}\", 0, {item.civ_vi_id})"
      # fmt: on
        self.tuner.send_command(command)
