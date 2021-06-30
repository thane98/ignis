import dataclasses
import logging

import yaml

from ignis.model.fe14_game_config import FE14GameConfig

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


@dataclasses.dataclass
class Configs:
    fe14_config: FE14GameConfig

    @staticmethod
    def load(fe14_path="ignis-fe14.yml"):
        try:
            with open(fe14_path, "r", encoding="utf-8") as f:
                raw_yaml = yaml.load(f, Loader=Loader)
            fe14_config = FE14GameConfig(**raw_yaml)
            return Configs(fe14_config)
        except:
            logging.exception("Failed to load ignis configs.")
            raise
