from typing import Literal, List

from pydantic import BaseModel


class FE14CharacterInfo(BaseModel):
    pid: str
    voice_set: str
    gender: Literal["male", "female"]
    class_level: Literal["base", "advanced"]
    generation: Literal[1, 2]
    flags: List[str] = []
