import re

from ignis.core.fe14 import fe14_utils
from ignis.core.randomization_step import RandomizationStep


class FE14UpdateDialogueStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return user_config.randomize_join_order

    def name(self) -> str:
        return "Update Dialogue (FE14)"

    def run(self, gd, user_config, dependencies):
        chapters = dependencies.chapters
        characters = dependencies.characters

        # Build a regex for matching everything we need to replace.
        replacements = characters.get_dialogue_replacements()
        keys = sorted(replacements.keys(), key=len, reverse=True)
        exp = re.compile("|".join(keys))

        # Get the target files
        files = fe14_utils.get_all_files(gd, "m", ".bin.lz", chapters, localized=True)
        files.extend(["m/Join.bin.lz", "m/GMap.bin.lz"])

        # Perform replacements!
        for f in files:
            gd.open_text_data(f, True)
            for key in gd.enumerate_messages(f, True):
                message = gd.message(f, True, key)
                new_message = exp.sub(
                    lambda match: replacements[match.group(0)], message
                )
                gd.set_message(f, True, key, new_message)
