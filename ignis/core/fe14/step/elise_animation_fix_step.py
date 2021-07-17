import os
import pathlib

from ignis.core.randomization_step import RandomizationStep

from ignis import ignis as ignis_core


_ASET_PATH = "bs/aset.lz"
_ELISE_PID = "PID_エリーゼ"
_ANIMATION_SET = "uEAnim_Eliserep_non"


class EliseAnimationFixStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return user_config.randomize_join_order and user_config.elise_animation_fix

    def name(self) -> str:
        return "Elise Animation Fix"

    def run(self, gd, user_config, dependencies):
        output_path = dependencies.output_path
        characters = dependencies.characters

        replacement_pid = characters.get_replacement(_ELISE_PID)
        replacement_rid = (
            characters.to_rid(replacement_pid) if replacement_pid else None
        )
        replacement_aid = gd.string(replacement_rid, "aid") if replacement_rid else None

        if not replacement_aid:
            return

        rom3 = gd.node("rom3")
        spec = gd.list_key_to_rid(rom3.rid, "specs", replacement_aid)

        if spec and not gd.string(spec, "attack_animation2"):
            gd.set_string(spec, "attack_animation2", _ANIMATION_SET)
            aset = gd.read_file(_ASET_PATH)
            aset_output_path = os.path.join(output_path, _ASET_PATH)
            os.makedirs(os.path.join(output_path, "bs"), exist_ok=True)
            ignis_core.apply_elise_animation_fix(aset, aset_output_path)
