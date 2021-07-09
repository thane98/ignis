from enum import Enum


class StatRandomizationAlgorithm(str, Enum):
    NONE = "NONE"
    WEIGHTED_REDISTRIBUTE = "WEIGHTED_REDISTRIBUTE"
    REDISTRIBUTE = "REDISTRIBUTE"
    SHUFFLE = "SHUFFLE"
