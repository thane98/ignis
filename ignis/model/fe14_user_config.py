import dataclasses
from typing import List

from ignis.model.fe14_route import FE14Route
from ignis.model.stat_randomization_algorithm import StatRandomizationAlgorithm


@dataclasses.dataclass
class FE14UserConfig:
    routes: List[FE14Route]
    stat_randomization_algorithm: StatRandomizationAlgorithm
    randomize_personal_skills: bool
    randomize_equip_skills: bool
    include_all_skills_in_skill_pool: bool
    randomize_classes: bool
    randomize_chest_items: bool
    unlock_hero_battles: bool
    add_anna_to_castle_join: bool
    include_anna_in_character_pool: bool
    include_amiibo_units_in_character_pool: bool
    randomize_children: bool
    randomize_join_order: bool
    randomize_player: bool
    same_sex_swaps_only: bool
    songstress_sprite_fix: bool
    elise_animation_fix: bool
    feral_dragon_head_fix: bool
    separate_pool_for_corrinsexuals: bool
    seed: int
    passes: int
