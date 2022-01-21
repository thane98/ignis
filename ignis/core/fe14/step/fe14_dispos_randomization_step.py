from ignis.model.item_category import ItemCategory

from ignis.core.fe14 import fe14_utils
from ignis.core.randomization_step import RandomizationStep

_DIVINE_WEAPONS = {
    "IID_雷神刀",
    "IID_風神弓",
    "IID_風神弓（青銅）",
    "IID_ブリュンヒルデ",
    "IID_ジークフリート",
    "IID_スカディ",
}

_ITEM_FIELDS = ["item_1", "item_2", "item_3", "item_4", "item_5"]

_ITEM_BITFLAGS = [
    "item_flags_1",
    "item_flags_2",
    "item_flags_3",
    "item_flags_4",
    "item_flags_5",
]

_BANNED_PIDS = {"PID_A001_ボス", "PID_A005_リョウマ"}


class FE14DisposRandomizationStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return user_config.randomize_classes

    def name(self) -> str:
        return "Spawn/Dispos Randomization (FE14)"

    def run(self, gd, user_config, dependencies):
        chapters = dependencies.chapters
        classes = dependencies.classes
        characters = dependencies.characters
        items = dependencies.items

        # Get the target files
        files = fe14_utils.get_all_files(gd, "GameData/Dispos", ".bin.lz", chapters)

        # Randomize
        for f in files:
            dirty = False
            rid = gd.multi_open("dispos", f)
            factions = gd.items(rid, "factions")
            for faction in factions:
                spawn_table = gd.rid(faction, "table")
                if not spawn_table:
                    continue
                spawns = gd.items(spawn_table, "spawns")
                for spawn in spawns:
                    has_changes = self.randomize_spawn(
                        gd, characters, classes, items, spawn
                    )
                    dirty = dirty or has_changes
            if dirty:
                gd.multi_set_dirty("dispos", f, True)

    @staticmethod
    def randomize_spawn(gd, characters, classes, items, spawn):
        dirty = False

        pid = gd.string(spawn, "pid")
        if pid in _BANNED_PIDS:
            return dirty

        if replacement_pid := characters.get_replacement(pid):
            gd.set_string(spawn, "pid", replacement_pid)
            pid = replacement_pid

        if char := characters.get_global_character(pid):
            i = 0
            added_at_least_one_weapon = False

            character_class = gd.rid(char, "class_1")
            class_weapons = list(
                filter(
                    lambda p: p is not None, classes.get_usable_weapons(character_class)
                )
            )
            assign_extra_non_staff_weapon = len(class_weapons) > 1 and any(
                filter(lambda p: p[0] == ItemCategory.STAFF, class_weapons)
            )

            while i < len(_ITEM_FIELDS) and gd.rid(spawn, _ITEM_FIELDS[i]):
                item_rid = gd.rid(spawn, _ITEM_FIELDS[i])
                iid = gd.key(item_rid)

                if (
                    iid not in _DIVINE_WEAPONS
                    and gd.int(item_rid, "weapon_category") < 20
                ):
                    weapon = items.random_weapon_for_character(char)
                    gd.set_rid(spawn, _ITEM_FIELDS[i], weapon)
                    added_at_least_one_weapon = True
                    dirty = True
                    if weapon and assign_extra_non_staff_weapon:
                        assign_extra_non_staff_weapon = gd.int(weapon, "weapon_category") in {12, 13}
                i += 1
            if not added_at_least_one_weapon and i < len(_ITEM_FIELDS):
                weapon = items.random_weapon_for_character(char)
                gd.set_rid(spawn, _ITEM_FIELDS[i], weapon)
                dirty = True
                i += 1
                if weapon and assign_extra_non_staff_weapon:
                    assign_extra_non_staff_weapon = gd.int(weapon, "weapon_category") in {12, 13}
            if assign_extra_non_staff_weapon and i < len(_ITEM_FIELDS):
                weapon = items.random_weapon_for_character(char, staff_ban=True)
                gd.set_rid(spawn, _ITEM_FIELDS[i], weapon)
                dirty = True
        return dirty
