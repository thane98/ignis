from typing import Literal, List

from ignis.model.fe14_route import FE14Route
from pydantic import BaseModel


class FE14CharacterInfo(BaseModel):
    pid: str
    voice_set: str
    gender: Literal["male", "female"]
    class_level: Literal["base", "advanced"]
    generation: Literal[1, 2]
    flags: List[str] = []
    routes: List[FE14Route] = []
    corrinsexual: bool = False
