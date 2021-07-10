from dataclasses import dataclass
from typing import List, Optional


@dataclass
class FE14CharacterReport:
    name: Optional[str]
    replacing: Optional[str]
    primary_class: str
    secondary_class: Optional[str]
    reclasses: List[Optional[str]]
    personal_skill: str
    equip_skills: List[str]
    bases: List[int]
    growths: List[int]
    modifiers: List[int]
    level: int
    internal_level: int

    def format(self):
        return "\n".join(
            [
                f"Name: {self.name}",
                f"Replacing: {self.replacing}",
                f"Primary Class: {self.primary_class}",
                f"Secondary Class: {self.secondary_class}",
                f"Reclasses: {self.reclasses[0]}, {self.reclasses[1]}",
                "Personal Skill: " + self.personal_skill,
                f"Equip Skills: {self.equip_skills}",
                f"Bases: {self.bases}",
                f"Growths: {self.growths}",
                f"Modifiers: {self.modifiers}",
                "Level: " + str(self.level),
                "Internal Level: " + str(self.internal_level),
            ]
        )
