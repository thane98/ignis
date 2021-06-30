from enum import Enum


class ItemCategory(str, Enum):
    SWORD = "Sword"
    LANCE = "Lance"
    AXE = "Axe"
    HIDDEN_WEAPON = "HiddenWeapon"
    BOW = "Bow"
    TOME = "Tome"
    STAFF = "Staff"
    DRAGONSTONE = "Dragonstone"
    BEASTSTONE = "Beaststone"
