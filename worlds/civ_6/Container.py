import os
import zipfile
from worlds.Files import APContainer


class CivVIContainer(APContainer):
    game: str = "Civilization VI"

    def __init__(self, base_path: str, output_directory: str,
                 player=None, player_name: str = "", server: str = ""):
        self.file_path = base_path
        container_path = os.path.join(output_directory, base_path + ".zip")
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr("civ_vi.txt", "Hello, World!")
        super().write_contents(opened_zipfile)
