from random import Random

from ignis.model.fe14_game_config import FE14GameConfig


class FE14SkillsVendor:
    def __init__(self, gd, game_config: FE14GameConfig, rand: Random):
        self.gd = gd
        self.personal_skills = game_config.personal_skills
        self.rand = rand

        rid, field_id = gd.table("skills")
        self.seid_to_rid = gd.key_to_rid_mapping(rid, field_id)

    def random_personal_skill(self):
        return self.seid_to_rid[self.rand.choice(self.personal_skills)]
