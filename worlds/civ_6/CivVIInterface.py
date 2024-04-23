from logging import Logger
from typing import List

from worlds.civ_6.TunerClient import TunerClient, TunerConnectionException, TunerTimeoutException


class CivVIInterface:
    logger: Logger
    tuner: TunerClient

    def __init__(self, logger: Logger):
        self.logger = logger
        self.tuner = TunerClient(logger)

    def is_connected(self) -> bool:
        self.logger.info("Checking if connected")
        command = "_VERSION"
        try:
            self.tuner.send_command(command)
            return True
        except TunerConnectionException:
            return False

    def is_in_game(self) -> bool:
        self.logger.info("Checking if in game")
        command = "IsInGame()"
        try:
            result = self.tuner.send_game_command(command)
            return result == "true"
        except TunerTimeoutException:
            return False

    def give_item_to_player(self, item: str, sender: str = "") -> bool:
        command = "ReceiveItem(\"" + item + "\", \"" + sender + "\")"
        self.tuner.send_game_command(command)
        return True

    def get_checked_locations(self) -> List[str]:
        command = "GetCheckedLocations()"
        result = self.tuner.send_game_command(command)
        return result.split(",")
