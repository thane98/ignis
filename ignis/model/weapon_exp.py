from dataclasses import dataclass

from ignis.model.weapon_rank import WeaponRank

_FE14_CHARACTER_FIELDS = [
    "sword_exp",
    "lance_exp",
    "axe_exp",
    "dagger_exp",
    "bow_exp",
    "tome_exp",
    "staff_exp",
    "stone_exp",
]


@dataclass
class WeaponExp:
    exp: int

    @staticmethod
    def from_fates_character(gd, rid):
        result = []
        for field in _FE14_CHARACTER_FIELDS:
            exp = WeaponExp(gd.int(rid, field))
            result.append(exp)
        return result

    @staticmethod
    def save_fates_weapon_exp(gd, rid, exp):
        assert len(exp) == 8
        for i in range(0, len(_FE14_CHARACTER_FIELDS)):
            field = _FE14_CHARACTER_FIELDS[i]
            gd.set_int(rid, field, exp[i])

    def get_rank(self):
        return WeaponRank.from_fates_exp(self.exp)

    def sort_value(self):
        rank = self.get_rank()
        return rank.sort_value() if rank else -1
