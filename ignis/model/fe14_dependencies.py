from dataclasses import dataclass
from random import Random

from ignis.core.fe14.fe14_chapter_vendor import FE14ChapterVendor
from ignis.core.fe14.fe14_character_vendor import FE14CharactersVendor
from ignis.core.fe14.fe14_classes_vendor import FE14ClassesVendor
from ignis.core.fe14.fe14_item_vendor import FE14ItemVendor
from ignis.core.fe14.fe14_skills_vendor import FE14SkillsVendor


@dataclass
class FE14Dependencies:
    rom_path: str
    output_path: str
    rand: Random
    skills: FE14SkillsVendor
    classes: FE14ClassesVendor
    characters: FE14CharactersVendor
    chapters: FE14ChapterVendor
    items: FE14ItemVendor
