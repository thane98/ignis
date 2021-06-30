from enum import Enum


class Game(str, Enum):
    FE14 = "FE14"

    def to_rust_variant(self):
        return self.value
