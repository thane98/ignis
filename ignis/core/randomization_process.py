import logging
from abc import ABC, abstractmethod
from typing import List

from ignis.core.randomization_step import RandomizationStep


class RandomizationProcess(ABC):
    def __init__(self, gd, user_config, game_config, rom_path, output_path):
        self.gd = gd
        self.user_config = user_config
        self.game_config = game_config
        self.rom_path = rom_path
        self.output_path = output_path

        # Verify that the user's options make sense.
        # Ex. If a user selects Conquest, does their ROM actually have the files?
        self.sanity_check()

        self.dependencies = self.init_dependencies()

    @abstractmethod
    def sanity_check(self):
        pass

    @abstractmethod
    def init_dependencies(self):
        pass

    @abstractmethod
    def steps(self) -> List[RandomizationStep]:
        pass

    def randomize(self):
        try:
            for step in self.steps():
                if step.should_run(self.user_config):
                    logging.info(f"Performing randomization step '{step.name()}'")
                    step.run(self.gd, self.user_config, self.dependencies)
                else:
                    logging.info(f"Skipping step '{step.name()}'")
        except:
            logging.exception("Failed randomization step.")
            raise
        try:
            self.gd.write()
        except:
            logging.exception("Failed to save randomization results.")
            raise
