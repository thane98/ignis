from ignis.model.weapon_exp import WeaponExp
from ignis.model.weapon_rank import WeaponRank


class FE14ItemVendor:
    def __init__(self, gd, game_config, user_config, rand, characters, classes):
        self.gd = gd
        self.game_config = game_config
        self.user_config = user_config
        self.rand = rand
        self.characters = characters
        self.classes = classes

        self.items = game_config.items
        self.treasures = game_config.treasures

        table_rid, table_field_id = self.gd.table("items")
        self.iid_to_rid = self.gd.key_to_rid_mapping(table_rid, table_field_id)

    def get_treasures(self):
        return self.treasures

    def default_item(self):
        table_rid, table_field_id = self.gd.table("items")
        return self.gd.list_get(table_rid, table_field_id, 0)

    def random_weapon_for_character(self, rid):
        # Get usable weapons for the class + character experience
        character_class = self.gd.rid(rid, "class_1")
        class_weapons = self.classes.get_usable_weapons(character_class)
        character_ranks = WeaponExp.from_fates_character(self.gd, rid)

        # Reconcile exp differences between character and class.
        reconciled_weapons = []
        for i, info in enumerate(class_weapons):
            if info:
                category, class_rank = info
                character_rank = character_ranks[i].get_rank()
                if class_rank and character_rank:
                    reconciled_rank = self._reconcile_character_and_class_exp(
                        character_rank, class_rank
                    )
                    reconciled_weapons.append((category, reconciled_rank))

        # Select a random category, then get a random weapon for the rank.
        # If no weapons for the rank, try the previous rank.
        category, rank = self.rand.choice(reconciled_weapons)
        weapon = None
        while not weapon:
            bucket = self.items.get(category)
            if not bucket:
                # No weapons for the category
                return None
            bucket = bucket.get(rank)
            if not bucket:
                # No weapons for the rank. Try previous rank.
                rank = rank.previous()
                if not rank:
                    # Out of options, no weapons to give.
                    return None
            else:
                weapon = self.rand.choice(bucket)
        return self.iid_to_rid[weapon]

    @staticmethod
    def _reconcile_character_and_class_exp(
        character_rank: WeaponRank, class_rank: WeaponRank
    ):
        if class_rank.sort_value() < character_rank.sort_value():
            return class_rank
        else:
            return character_rank
