from typing import Literal, List

from pydantic import BaseModel


class FE14ClassInfo(BaseModel):
    jid: str
    gender: Literal["male", "female"]
    level: Literal["base", "advanced"]
    paired_classes: List[str] = None
    capped_at_40: bool = False
