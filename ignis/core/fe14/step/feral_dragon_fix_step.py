from ignis.core.randomization_step import RandomizationStep


_MALE_KANA = "PID_カンナ男"
_MALE_COND = "!JID_竜男"
_FEMALE_KANA = "PID_カンナ女"
_FEMALE_COND = "!JID_竜女"


class FeralDragonFixStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return user_config.randomize_join_order and user_config.feral_dragon_head_fix

    def name(self) -> str:
        return "Feral Dragon Fix"

    def run(self, gd, user_config, dependencies):
        characters = dependencies.characters

        male_kana_replacement = characters.get_replacement(_MALE_KANA)
        female_kana_replacement = characters.get_replacement(_FEMALE_KANA)
        male_kana_replacement_rid = (
            characters.to_rid(male_kana_replacement) if male_kana_replacement else None
        )
        female_kana_replacement_rid = (
            characters.to_rid(female_kana_replacement)
            if female_kana_replacement
            else None
        )
        male_kana_replacement_aid = gd.string(male_kana_replacement_rid, "aid")
        female_kana_replacement_aid = gd.string(female_kana_replacement_rid, "aid")
        if male_kana_replacement_aid:
            self._apply_fix(gd, male_kana_replacement_aid, male=True)
        if female_kana_replacement_aid:
            self._apply_fix(gd, female_kana_replacement_aid)

    @staticmethod
    def _apply_fix(gd, aid, male=False):
        node = gd.node("rom3")
        spec = gd.list_key_to_rid(node.rid, "specs", aid)
        cond = _MALE_COND if male else _FEMALE_COND
        if spec:
            cond1 = gd.string(spec, "conditional1")
            cond2 = gd.string(spec, "conditional2")
            if cond1 == cond or cond2 == cond:
                return
            if not cond1:
                gd.set_string(spec, "conditional1", cond)
            elif not cond2:
                gd.set_string(spec, "conditional2", cond)
        gd.set_store_dirty("rom3", True)
