import os

from ignis.model.fe14_route import FE14Route

from ignis.core.randomization_step import RandomizationStep

from ignis import ignis as ignis_core


class ApplyB016ShuraFixStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return (
            user_config.randomize_classes and FE14Route.CONQUEST in user_config.routes
        )

    def name(self) -> str:
        return "Apply B016 Shura Fix"

    def run(self, gd, user_config, dependencies):
        output_path = dependencies.output_path
        rom_path = dependencies.rom_path
        characters = dependencies.characters
        items = dependencies.items

        # Get new weapons for Shura/Shura's replacement
        replacement = characters.get_replacement("PID_アシュラ")
        if not replacement:
            return
        rid = characters.to_rid(replacement)
        weapon1 = gd.key(items.random_weapon_for_character(rid))
        weapon2 = gd.key(items.random_weapon_for_character(rid))

        # Swap out weapons in the B016 script.
        path_in_rom = os.path.join(rom_path, "Scripts", "B", "B016.cmb")
        path_in_output = os.path.join(output_path, "Scripts", "B", "B016.cmb")
        if os.path.exists(path_in_output):
            input_path, output_path = path_in_output, path_in_output
        else:
            input_path, output_path = path_in_rom, path_in_output
        ignis_core.fix_b016_shura_weapons(input_path, output_path, weapon1, weapon2)
