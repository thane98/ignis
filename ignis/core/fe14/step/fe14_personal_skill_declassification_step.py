from ignis.core.randomization_step import RandomizationStep


class FE14PersonalSkillDeclassificationStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return user_config.include_all_skills_in_skill_pool

    def name(self) -> str:
        return "Personal Skill Declassification (FE14)"

    def run(self, gd, user_config, dependencies):
        rid, field_id = gd.table("skills")
        skills = gd.items(rid, field_id)
        for skill_rid in skills:
            gd.set_int(skill_rid, "unknown_2", 0)
