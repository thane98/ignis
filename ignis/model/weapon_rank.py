from enum import Enum
from typing import Optional, List


_FE14_JOB_FIELDS = [
    "max_sword_exp",
    "max_lance_exp",
    "max_axe_exp",
    "max_dagger_exp",
    "max_bow_exp",
    "max_tome_exp",
    "max_staff_exp",
    "max_stone_exp",
]


_SORT_VALUES = {
    "E": 0,
    "D": 1,
    "C": 2,
    "B": 3,
    "A": 4,
    "S": 5,
}


class WeaponRank(str, Enum):
    E = "E"
    D = "D"
    C = "C"
    B = "B"
    A = "A"
    S = "S"

    @staticmethod
    def from_fates_exp(exp: int) -> Optional["WeaponRank"]:
        if exp >= 251:
            return WeaponRank.S
        elif exp >= 161:
            return WeaponRank.A
        elif exp >= 96:
            return WeaponRank.B
        elif exp >= 51:
            return WeaponRank.C
        elif exp >= 21:
            return WeaponRank.D
        elif exp >= 1:
            return WeaponRank.E
        else:
            return None

    @staticmethod
    def ranks_from_fates_job(gd, rid: int):
        return WeaponRank._ranks_from_fates_fields(gd, rid, _FE14_JOB_FIELDS)

    @staticmethod
    def _ranks_from_fates_fields(
        gd, rid: int, fields: List[str]
    ) -> List[Optional["WeaponRank"]]:
        result = []
        for i in range(0, len(fields)):
            exp = gd.int(rid, fields[i])
            result.append(WeaponRank.from_fates_exp(exp))
        return result

    def sort_value(self):
        return _SORT_VALUES[self.value]

    def previous(self):
        if self == WeaponRank.S:
            return WeaponRank.A
        elif self == WeaponRank.A:
            return WeaponRank.B
        elif self == WeaponRank.B:
            return WeaponRank.C
        elif self == WeaponRank.C:
            return WeaponRank.D
        elif self == WeaponRank.D:
            return WeaponRank.E
        return None
