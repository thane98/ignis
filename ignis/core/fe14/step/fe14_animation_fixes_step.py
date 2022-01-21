import os
import pathlib

from ignis.core.randomization_step import RandomizationStep

from ignis import ignis as ignis_core


_ASET_PATH = "bs/aset.lz"
_ELISE_PID = "PID_エリーゼ"
_HINOKA_PID = "PID_ヒノカ"
_KAZE_PID = "PID_スズカゼ"
_ELISE_ANIMATION_SET = "uEAnim_Eliserep_non"
_HINOKA_ANIMATION_SET = "uEAnim_Hinokarep_non"
_KAZE_ANIMATION_SET = "uEAnim_Kazerep_non"


class FE14AnimationFixesStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return user_config.randomize_join_order and user_config.apply_animation_fixes

    def name(self) -> str:
        return "Animation Fixes (FE14)"

    def run(self, gd, user_config, dependencies):
        output_path = dependencies.output_path
        characters = dependencies.characters
        rom3 = gd.node("rom3")

        dirty = False

        elice_replacement_aid = self._get_replacement_aid(gd, characters, _ELISE_PID)
        hinoka_replacement_aid = self._get_replacement_aid(gd, characters, _HINOKA_PID)
        kaze_replacement_aid = self._get_replacement_aid(gd, characters, _KAZE_PID)

        if elice_replacement_aid:
            dirty = self._apply_fix(gd, rom3, elice_replacement_aid, _ELISE_ANIMATION_SET)
        if hinoka_replacement_aid:
            dirty = self._apply_fix(gd, rom3, hinoka_replacement_aid, _HINOKA_ANIMATION_SET)
        if kaze_replacement_aid:
            dirty = self._apply_fix(gd, rom3, kaze_replacement_aid, _KAZE_ANIMATION_SET)

        if dirty:
            aset = gd.read_file(_ASET_PATH)
            aset_output_path = os.path.join(output_path, _ASET_PATH)
            os.makedirs(os.path.join(output_path, "bs"), exist_ok=True)
            ignis_core.apply_fe14_animation_fixes(aset, aset_output_path)

    @staticmethod
    def _get_replacement_aid(gd, characters, pid):
        replacement_pid = characters.get_replacement(pid)
        replacement_rid = (
            characters.to_rid(replacement_pid) if replacement_pid else None
        )
        return gd.string(replacement_rid, "aid") if replacement_rid else None

    @staticmethod
    def _apply_fix(gd, rom3, aid, anim):
        spec = gd.list_key_to_rid(rom3.rid, "specs", aid)
        if spec and not gd.string(spec, "attack_animation2"):
            gd.set_string(spec, "attack_animation2", anim)
            return True
        return False
