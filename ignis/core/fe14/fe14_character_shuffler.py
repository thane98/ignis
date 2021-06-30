from random import Random

from ignis.model.fe14_user_config import FE14UserConfig

from ignis.core.character_shuffler import CharacterShuffler


class FE14CharacterShuffler(CharacterShuffler):
    def __init__(self, user_config: FE14UserConfig, rand: Random):
        super().__init__(rand)
        self._predicates = [lambda c: c.generation == 2]
        if user_config.same_sex_swaps_only:
            self._predicates.append(lambda c: c.gender == "female")

    def predicates(self):
        return self._predicates
