from random import Random

from ignis.model.fe14_game_config import FE14GameConfig
from ignis.model.item_category import ItemCategory
from ignis.model.weapon_rank import WeaponRank


_WEAPONS = [
    ItemCategory.SWORD,
    ItemCategory.LANCE,
    ItemCategory.AXE,
    ItemCategory.HIDDEN_WEAPON,
    ItemCategory.BOW,
    ItemCategory.TOME,
    ItemCategory.STAFF,
]


class FE14ClassesVendor:
    def __init__(self, gd, game_config: FE14GameConfig, rand: Random):
        self.gd = gd
        self.game_config = game_config
        self.rand = rand

        rid, field_id = gd.table("jobs")
        self.jid_to_rid_mapping = gd.key_to_rid_mapping(rid, field_id)

        self.jid_to_info_mapping = {}
        self.buckets = {}
        for cls in game_config.classes:
            self.jid_to_info_mapping[cls.jid] = cls
            key = (cls.gender, cls.level)
            if key in self.buckets:
                self.buckets[key].append(cls)
            else:
                self.buckets[key] = [cls]

    def get_class_level(self, rid):
        return self.jid_to_info_mapping[self.gd.key(rid)].level

    def get_usable_weapons(self, rid):
        ranks = WeaponRank.ranks_from_fates_job(self.gd, rid)
        weapons = []
        for i, rank in enumerate(ranks):
            if rank and i == len(ranks) - 1:
                if self.gd.int(rid, "special_flags_1") & 0b10000000:
                    weapons.append((ItemCategory.BEASTSTONE, rank))
                else:
                    weapons.append((ItemCategory.DRAGONSTONE, rank))
            elif rank:
                weapons.append((_WEAPONS[i], rank))
            else:
                weapons.append(None)
        return weapons

    def random_class_set(self, gender, level, staff_only_ban=False):
        done = False
        while not done:
            class_1 = self.rand.choice(self.buckets[(gender, level)])
            class_1_rid = self.jid_to_rid_mapping[class_1.jid]
            if not staff_only_ban:
                done = True
            else:
                usable_weapons = self.get_usable_weapons(class_1_rid)
                non_null = list(filter(lambda i: bool(i), usable_weapons))
                done = len(non_null) > 1 or non_null[0][0] != ItemCategory.STAFF
        if (
            class_1.paired_classes[0] == self._default_class()
            and not class_1.paired_classes[1] == self._default_class()
        ):
            class_2 = class_1.paired_classes[1]
        elif (
            not class_1.paired_classes[0] == self._default_class()
            and class_1.paired_classes[1] == self._default_class()
        ):
            class_2 = class_1.paired_classes[0]
        else:
            class_2 = self.rand.choice(class_1.paired_classes)
        class_2_rid = self.jid_to_rid_mapping[class_2]
        reclass_1 = self._get_reclass(
            self.buckets[(gender, "base")], [class_1, class_2]
        )
        reclass_1_rid = self.jid_to_rid_mapping[reclass_1.jid]
        reclass_2 = self._get_reclass(
            self.buckets[(gender, "base")], [class_1, class_2, reclass_1]
        )
        reclass_2_rid = self.jid_to_rid_mapping[reclass_2.jid]
        return class_1_rid, class_2_rid, reclass_1_rid, reclass_2_rid

    def _get_reclass(self, bucket, used):
        valid_classes = list(filter(lambda c: c not in used, bucket))
        if not valid_classes:
            return self._default_class()
        return self.rand.choice(valid_classes)

    def _default_class(self):
        rid, field_id = self.gd.table("jobs")
        return self.gd.key(self.gd.list_get(rid, field_id, 0))
