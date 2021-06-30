from enum import Enum


class StatRandomizationAlgorithm(str, Enum):
    NONE = "NONE"
    REDISTRIBUTE = "REDISTRIBUTE"
    SHUFFLE = "SHUFFLE"
