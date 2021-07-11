from random import Random
from typing import Union, Tuple, List
import ctypes

from ignis.model.stat_randomization_algorithm import StatRandomizationAlgorithm


def _redistribute(
    rand: Random,
    stats: List[int],
    limits: Tuple[int, int],
    step_size,
    k: int,
    weights=None,
) -> bytes:
    indices = [i for i in range(0, len(stats))]
    choices = rand.choices(population=indices, weights=weights, k=k * 2)
    for i in range(0, len(choices), 2):
        source = choices[i]
        dest = choices[i + 1]
        if (
            stats[source] - step_size >= limits[0]
            and stats[dest] + step_size <= limits[1]
        ):
            stats[source] -= step_size
            stats[dest] += step_size
    return bytes(map(lambda b: ctypes.c_uint8(b).value, stats))


class WeightedRedistributeStatsStrategy:
    @staticmethod
    def randomize_stats(
        rand: Random,
        stats: Union[bytes, bytearray],
        limits: Tuple[int, int],
        step_size=1,
        passes=20,
        weights=None,
        **kwargs,
    ) -> bytes:
        tmp = list(map(lambda b: ctypes.c_int8(b).value, stats))
        if not weights:
            denominator = sum(map(abs, tmp))
            weights = list(map(lambda b: abs(b) / denominator if b != 0 else 0, tmp))
            min_weight = min(weights)
            weights = [min_weight if w == 0 else w for w in weights]
        return _redistribute(
            rand,
            tmp,
            limits,
            step_size,
            passes,
            weights,
        )


class RedistributeStatsStrategy:
    @staticmethod
    def randomize_stats(
        rand: Random,
        stats: Union[bytes, bytearray],
        limits: Tuple[int, int],
        step_size=1,
        passes=20,
        **kwargs,
    ) -> bytes:
        tmp = list(map(lambda b: ctypes.c_int8(b).value, stats))
        return _redistribute(
            rand,
            tmp,
            limits,
            step_size,
            passes,
        )


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
    elif algorithm == StatRandomizationAlgorithm.WEIGHTED_REDISTRIBUTE:
        return WeightedRedistributeStatsStrategy
    elif algorithm == StatRandomizationAlgorithm.SHUFFLE:
        return ShuffleStatsStrategy
    else:
        return RedistributeStatsStrategy
