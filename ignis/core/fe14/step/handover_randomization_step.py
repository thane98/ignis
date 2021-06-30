from ignis.core.fe14 import fe14_utils

from ignis.core import stat_randomization_strategy

from ignis.model.fe14_route import FE14Route

from ignis.model.stat_randomization_algorithm import StatRandomizationAlgorithm

from ignis.core.randomization_step import RandomizationStep


class HandoverRandomizationStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return (
            user_config.randomize_join_order
            or user_config.randomize_classes
            or user_config.stat_randomization_algorithm
            != StatRandomizationAlgorithm.NONE
        )

    def name(self) -> str:
        return "Handover Randomization"

    def run(self, gd, user_config, dependencies):
        rand = dependencies.rand
        characters = dependencies.characters
        files = self._get_handover_files(user_config.routes)
        for f in files:
            if gd.file_exists(f, False):
                rid = gd.multi_open("person", f)
                people = gd.items(rid, "people")
                if self.randomize_people(gd, user_config, characters, rand, people):
                    gd.multi_set_dirty("person", f, True)

    @staticmethod
    def randomize_people(gd, user_config, characters, rand, people):
        dirty = False
        for rid in people:
            if orig := gd.rid(rid, "replacing"):
                if replacement := characters.get_replacement(gd.key(orig)):
                    HandoverRandomizationStep.randomize_person(
                        gd,
                        user_config,
                        rand,
                        characters,
                        rid,
                        characters.to_rid(replacement),
                    )
                    dirty = True
        return dirty

    @staticmethod
    def randomize_person(gd, user_config, rand, characters, rid, replacement):
        if user_config.randomize_join_order:
            gd.set_rid(rid, "replacing", replacement)
            fe14_utils.morph_character(gd, replacement, rid)
        if user_config.randomize_classes:
            fe14_utils.apply_randomized_class_set(
                gd, characters, gd.string(rid, "aid"), rid, replacement, rand
            )
        strategy = stat_randomization_strategy.from_algorithm(
            user_config.stat_randomization_algorithm
        )
        fe14_utils.apply_randomized_stats(gd, rand, rid, rid, strategy)

    @staticmethod
    def _get_handover_files(routes):
        files = set()
        for route in routes:
            if route == FE14Route.BIRTHRIGHT:
                files.add("GameData/Person/A_HANDOVER.bin.lz")
            elif route == FE14Route.CONQUEST:
                files.add("GameData/Person/B_HANDOVER.bin.lz")
            elif route == FE14Route.REVELATION:
                files.add("GameData/Person/C_HANDOVER.bin.lz")
        return files
