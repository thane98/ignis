from ignis.core.randomization_step import RandomizationStep


class UnlockHeroBattlesStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return user_config.unlock_hero_battles

    def name(self) -> str:
        return "Unlock Hero Battles Step"

    def run(self, gd, user_config, dependencies):
        chapters = dependencies.chapters

        hero_battles = ["CID_M001", "CID_M002", "CID_M003", "CID_M004"]
        unlock_chapters = [
            ("birthright_requirement", "CID_A007"),
            ("conquest_requirement", "CID_B007"),
            ("revelation_requirement", "CID_C007"),
        ]

        for cid in hero_battles:
            if rid := chapters.to_rid(cid):
                for f, unlock_cid in unlock_chapters:
                    gd.set_rid(rid, f, chapters.to_rid(unlock_cid))

        gd.set_store_dirty("gamedata", True)
