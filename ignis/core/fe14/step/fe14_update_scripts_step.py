import os

from ignis.core.fe14 import fe14_utils

from ignis.core.randomization_step import RandomizationStep

from ignis import ignis as ignis_core


class FE14UpdateScriptsStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return user_config.randomize_join_order

    def name(self) -> str:
        return "Update Scripts (FE14)"

    def run(self, gd, user_config, dependencies):
        rom_path = dependencies.rom_path
        output_path = dependencies.output_path
        chapters = dependencies.chapters
        characters = dependencies.characters

        files = fe14_utils.get_all_files(gd, "Scripts", ".cmb", chapters)
        files.extend(self._get_bev_files(gd, chapters))

        sources = []
        destinations = []
        for f in files:
            path_in_rom = os.path.normpath(os.path.join(rom_path, f))
            path_in_output = os.path.normpath(os.path.join(output_path, f))
            if os.path.exists(path_in_output):
                sources.append(path_in_output)
            else:
                sources.append(path_in_rom)
            destinations.append(path_in_output)
        files = list(zip(sources, destinations))

        replacements = characters.get_script_replacements()
        ignis_core.randomize_scripts(files, replacements)

    @staticmethod
    def _get_bev_files(gd, chapters):
        files = set()
        all_cid_parts = set(map(lambda c: c[1][4:], chapters.enabled_chapters()))
        for bev_file in gd.list_files("Scripts/bev", "*.cmb"):
            basename = os.path.basename(bev_file)
            if len(basename) >= 4 and basename[:4] in all_cid_parts:
                files.add(bev_file)
        return files
