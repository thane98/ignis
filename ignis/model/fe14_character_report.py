from dataclasses import dataclass
from typing import List, Optional


@dataclass
class FE14CharacterReport:
    name: str
    replacing: str
    primary_class: str
    secondary_class: Optional[str]
    reclasses: List[Optional[str]]
    personal_skill: str

    def format(self):
        return "\n".join(
            [
                "Name: " + self.name,
                "Replacing: " + self.replacing,
                f"Primary Class: {self.primary_class}",
                f"Secondary Class: {self.secondary_class}",
                f"Reclasses: {self.reclasses[0]},{self.reclasses[1]}",
                "Personal Skill: " + self.personal_skill,
            ]
        )
