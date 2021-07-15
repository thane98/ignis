import re

from ignis.core.fe14 import fe14_utils
from ignis.core.randomization_step import RandomizationStep


_KANA_MPID = "MPID_カンナ"
_MALE_KANA = "PID_カンナ男"
_FEMALE_KANA = "PID_カンナ女"
_MALE_KANA_PLACEHOLDER = "IGNIS_MALE_KANA_PLACEHOLDER"
_FEMALE_KANA_PLACEHOLDER = "IGNIS_FEMALE_KANA_PLACEHOLDER"


class FE14UpdateDialogueStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return user_config.randomize_join_order

    def name(self) -> str:
        return "Update Dialogue (FE14)"

    def run(self, gd, user_config, dependencies):
        chapters = dependencies.chapters
        characters = dependencies.characters

        # Get these now since we need them later.
        kana_name = gd.message("m/GameData.bin.lz", True, _KANA_MPID)
        male_kana_replacement = characters.get_replacement(_MALE_KANA)
        female_kana_replacement = characters.get_replacement(_FEMALE_KANA)
        male_kana_replacement_rid = characters.to_rid(male_kana_replacement) if male_kana_replacement else None
        female_kana_replacement_rid = characters.to_rid(female_kana_replacement) if female_kana_replacement else None
        male_kana_replacement_name = gd.display(male_kana_replacement_rid) if male_kana_replacement_rid else None
        female_kana_replacement_name = gd.display(female_kana_replacement_rid) if female_kana_replacement_rid else None

        # Get dialogue replacements.
        replacements = characters.get_dialogue_replacements()
        if kana_name in replacements:
            del replacements[kana_name]
        if male_kana_replacement_name and female_kana_replacement_name:
            replacements[_MALE_KANA_PLACEHOLDER] = male_kana_replacement_name
            replacements[_FEMALE_KANA_PLACEHOLDER] = female_kana_replacement_name

        # Build a regex for matching everything we need to replace.
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
                if key.endswith("_PCM1") and f.endswith("X002.bin.lz"):
                    message = message.replace(kana_name, _FEMALE_KANA_PLACEHOLDER)
                if key.endswith("_PCF1") and f.endswith("X002.bin.lz"):
                    message = message.replace(kana_name, _MALE_KANA_PLACEHOLDER)
                new_message = exp.sub(
                    lambda match: replacements[match.group(0)], message
                )
                gd.set_message(f, True, key, new_message)
