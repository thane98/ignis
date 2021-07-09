import os
from distutils import dir_util

from ignis.core.randomization_step import RandomizationStep


class ApplySongstressSpriteFixStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return user_config.songstress_sprite_fix

    def name(self) -> str:
        return "Apply Songstress Sprite Fix"

    def run(self, gd, user_config, dependencies):
        output_path = dependencies.output_path
        source_path = os.path.join(".", "Data", "Misc", "GenericSongstress")
        sprite_path = os.path.join(output_path, "unit", "Body", "歌姫女")

        # Avoid accidentally overwriting another songstress sprite
        # if one exists.
        if not os.path.exists(sprite_path):
            os.makedirs(sprite_path, exist_ok=True)
            dir_util.copy_tree(source_path, sprite_path)
