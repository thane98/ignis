from typing import List, Dict

from ignis.model.fe14_route import FE14Route
from pydantic.main import BaseModel

from ignis.model.fe14_character_info import FE14CharacterInfo
from ignis.model.fe14_class_info import FE14ClassInfo
from ignis.model.item_category import ItemCategory
from ignis.model.weapon_rank import WeaponRank


class FE14GameConfig(BaseModel):
    characters: List[FE14CharacterInfo]
    classes: List[FE14ClassInfo]
    equip_skills: List[str]
    personal_skills: List[str]
    items: Dict[ItemCategory, Dict[WeaponRank, List[str]]]
    treasures: List[str]
    global_chapters: List[str]
    route_chapters: Dict[FE14Route, List[str]]
