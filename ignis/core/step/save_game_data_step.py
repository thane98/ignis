from ignis.core.randomization_step import RandomizationStep


class SaveGameDataStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return True

    def name(self) -> str:
        return "Save Game Data"

    def run(self, gd, user_config, dependencies):
        gd.write()
