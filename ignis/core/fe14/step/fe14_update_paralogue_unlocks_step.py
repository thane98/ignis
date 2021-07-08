from ignis.core.randomization_step import RandomizationStep


_ALL_ROUTES = 7


class FE14UpdateParalogueUnlocksStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return user_config.randomize_join_order and user_config.randomize_children

    def name(self) -> str:
        return "Update Paralogue Unlocks (FE14)"

    def run(self, gd, user_config, dependencies):
        characters = dependencies.characters
        chapters = dependencies.chapters

        for _, cid in chapters.enabled_chapters():
            rid = chapters.to_rid(cid)
            if character_rid := gd.rid(rid, "married_character"):
                if replacement := characters.get_replacement(gd.key(character_rid)):
                    replacement_rid = characters.to_rid(replacement)
                    gd.set_rid(rid, "married_character", replacement_rid)
                    gd.set_int(rid, "route", _ALL_ROUTES)

        gd.set_store_dirty("gamedata", True)
