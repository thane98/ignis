import os

from ignis import ignis as ignis_core
from ignis.core.fe14 import fe14_utils
from ignis.core.randomization_step import RandomizationStep


class FE14RandomizeChestItemsStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return user_config.randomize_chest_items

    def name(self) -> str:
        return "Randomize Chest Items (FE14)"

    def run(self, gd, user_config, dependencies):
        rom_path = dependencies.rom_path
        output_path = dependencies.output_path
        chapters = dependencies.chapters
        items = dependencies.items

        files = fe14_utils.get_all_files(gd, "Scripts", "_Terrain.cmb", chapters)
        sources_and_destinations = self._resolve_paths(files, output_path, rom_path)
        treasures = items.get_treasures()

        ignis_core.randomize_terrain_scripts(
            sources_and_destinations, treasures, user_config.seed
        )

    @staticmethod
    def _resolve_paths(files, output_path, rom_path):
        resolved = []
        for f in files:
            path_in_rom = os.path.join(rom_path, f)
            path_in_output = os.path.join(output_path, f)
            if os.path.exists(path_in_output):
                resolved.append((path_in_output, path_in_output))
            else:
                resolved.append((path_in_rom, path_in_output))
        return resolved
