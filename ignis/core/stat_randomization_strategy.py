from random import Random
from typing import Union, Tuple
import ctypes

from ignis.model.stat_randomization_algorithm import StatRandomizationAlgorithm


class RedistributeStatsStrategy:
    PASSES = 20

    @staticmethod
    def randomize_stats(
        rand: Random,
        stats: Union[bytes, bytearray],
        limits: Tuple[int, int],
        step_size=1,
    ) -> bytes:
        tmp = list(map(lambda b: ctypes.c_int8(b).value, stats))
        for _ in range(0, RedistributeStatsStrategy.PASSES):
            index1 = rand.randint(0, len(tmp) - 1)
            index2 = rand.randint(0, len(tmp) - 1)
            if (
                tmp[index1] - step_size >= limits[0]
                and tmp[index2] + step_size <= limits[1]
            ):
                tmp[index1] -= step_size
                tmp[index2] += step_size
        return bytes(map(lambda b: ctypes.c_uint8(b).value, tmp))


class ShuffleStatsStrategy:
    @staticmethod
    def randomize_stats(
        rand: Random, stats: Union[bytes, bytearray], **kwargs
    ) -> bytes:
        tmp = list(stats)
        rand.shuffle(tmp)
        return bytes(tmp)


class NoOpStatsStrategy:
    @staticmethod
    def randomize_stats(
        _rand: Random, stats: Union[bytes, bytearray], **kwargs
    ) -> bytes:
        return stats


def from_algorithm(algorithm: StatRandomizationAlgorithm):
    if algorithm == StatRandomizationAlgorithm.NONE:
        return NoOpStatsStrategy
    elif algorithm == StatRandomizationAlgorithm.SHUFFLE:
        return ShuffleStatsStrategy
    else:
        return RedistributeStatsStrategy
