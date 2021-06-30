import dataclasses

from ignis.model.game import Game
from ignis.model.language import Language


@dataclasses.dataclass
class GameLoadInputs:
    rom_path: str
    output_path: str
    game: Game
    language: Language
