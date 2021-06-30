from abc import ABC, abstractmethod


class CharacterShuffler(ABC):
    def __init__(self, rand):
        self.rand = rand

    @abstractmethod
    def predicates(self):
        pass

    def shuffle(self, characters):
        # Group by predicates.
        groups = {}
        predicates = self.predicates()
        for char in characters:
            key = tuple([predicate(char) for predicate in predicates])
            if bucket := groups.get(key):
                bucket.append(char)
            else:
                groups[key] = [char]

        # Shuffle each group and merge.
        shuffled = []
        for group in groups.values():
            shuffled.extend(self._shuffle_group(group))
        return shuffled

    def _shuffle_group(self, group):
        shuffled = list(group)
        self.rand.shuffle(shuffled)
        return list(zip(group, shuffled))
