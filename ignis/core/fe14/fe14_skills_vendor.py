from random import Random

from ignis.model.fe14_user_config import FE14UserConfig

from ignis.model.fe14_game_config import FE14GameConfig


class FE14SkillsVendor:
    def __init__(
        self, gd, game_config: FE14GameConfig, user_config: FE14UserConfig, rand: Random
    ):
        self.gd = gd
        self.user_config = user_config
        self.personal_skills = game_config.personal_skills
        self.equip_skills = game_config.equip_skills
        self.rand = rand

        rid, field_id = gd.table("skills")
        self.default_skill_rid = gd.list_get(rid, field_id, 0)
        self.all_skills = gd.items(rid, field_id)[1:]  # Get rid of the null skill.
        self.seid_to_rid = gd.key_to_rid_mapping(rid, field_id)

    def default_skill(self):
        return self.default_skill_rid

    def random_personal_skill(self):
        if self.user_config.include_all_skills_in_skill_pool:
            return self.rand.choice(self.all_skills)
        else:
            return self.seid_to_rid[self.rand.choice(self.personal_skills)]

    def random_equip_skill(self):
        if self.user_config.include_all_skills_in_skill_pool:
            return self.rand.choice(self.all_skills)
        else:
            return self.seid_to_rid[self.rand.choice(self.equip_skills)]
