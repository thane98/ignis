import os

from ignis.core import stat_randomization_strategy

from ignis import ignis as ignis_core
from ignis.ignis import PlayerRandomizationInfo

from ignis.core.fe14 import fe14_utils
from ignis.core.randomization_step import RandomizationStep
from ignis.model.weapon_rank import WeaponRank

_MALE_CORRIN = "PID_プレイヤー男"
_FEMALE_CORRIN = "PID_プレイヤー女"
_MALE_AID = "AID_プレイヤー男"
_FEMALE_AID = "AID_プレイヤー女"


class FE14RandomizePlayerStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return user_config.randomize_player

    def name(self) -> str:
        return "Randomize Player (FE14)"

    def run(self, gd, user_config, dependencies):
        rom_path = dependencies.rom_path
        output_path = dependencies.output_path
        rand = dependencies.rand
        characters = dependencies.characters
        skills = dependencies.skills
        items = dependencies.items

        male_rid = characters.to_rid(_MALE_CORRIN)
        female_rid = characters.to_rid(_FEMALE_CORRIN)

        if user_config.randomize_personal_skills:
            fe14_utils.apply_randomized_skills(
                gd, characters, user_config, skills, _MALE_AID, male_rid
            )
            fe14_utils.apply_randomized_skills(
                gd, characters, user_config, skills, _FEMALE_AID, female_rid
            )

        if user_config.randomize_classes:
            fe14_utils.apply_randomized_class_set(
                gd,
                characters,
                _MALE_AID,
                male_rid,
                male_rid,
                rand,
                gender="male",
                class_level="base",
                staff_only_ban=True,
            )
            fe14_utils.apply_randomized_class_set(
                gd,
                characters,
                _FEMALE_AID,
                female_rid,
                female_rid,
                rand,
                gender="female",
                class_level="base",
                staff_only_ban=True,
            )

            # Now for the difficult part: updating scripts.
            male_class = gd.key(gd.rid(male_rid, "class_1"))
            female_class = gd.key(gd.rid(female_rid, "class_1"))
            male_weapon_a000 = gd.key(
                items.random_weapon_for_character(
                    male_rid, desired_rank=WeaponRank.E, staff_ban=True
                )
            )
            female_weapon_a000 = gd.key(
                items.random_weapon_for_character(
                    female_rid, desired_rank=WeaponRank.E, staff_ban=True
                )
            )
            male_weapon_006 = gd.key(
                items.random_weapon_for_character(
                    male_rid, desired_rank=WeaponRank.E, staff_ban=True
                )
            )
            female_weapon_006 = gd.key(
                items.random_weapon_for_character(
                    female_rid, desired_rank=WeaponRank.E, staff_ban=True
                )
            )

            if not os.path.exists(os.path.join(output_path, "Scripts")):
                os.mkdir(os.path.join(output_path, "Scripts"))
            files = [
                "Scripts/A000.cmb",
                "Scripts/A002.cmb",
                "Scripts/A005.cmb",
                "Scripts/B006.cmb",
                "Scripts/C006.cmb",
            ]
            input_output_pairs = []
            for f in files:
                path_in_rom = os.path.normpath(os.path.join(rom_path, f))
                path_in_output = os.path.normpath(os.path.join(output_path, f))
                if os.path.exists(path_in_output):
                    input_output_pairs.append((path_in_output, path_in_output))
                elif os.path.exists(path_in_rom):
                    input_output_pairs.append((path_in_rom, path_in_output))
                else:
                    input_output_pairs.append(None)
            player_randomization_info = PlayerRandomizationInfo(
                male_class,
                female_class,
                male_weapon_a000,
                female_weapon_a000,
                male_weapon_006,
                female_weapon_006,
                input_output_pairs[0],
                input_output_pairs[1],
                input_output_pairs[2],
                input_output_pairs[3],
                input_output_pairs[4],
            )
            ignis_core.apply_mu_class_randomization(player_randomization_info)

        strategy = stat_randomization_strategy.from_algorithm(
            user_config.stat_randomization_algorithm
        )
        fe14_utils.apply_randomized_stats(
            gd,
            rand,
            male_rid,
            male_rid,
            strategy,
            user_config.passes,
            weights=[0.15, 0.175, 0.15, 0.1, 0.125, 0.1, 0.1, 0.1],
        )
        fe14_utils.apply_randomized_stats(
            gd,
            rand,
            female_rid,
            female_rid,
            strategy,
            user_config.passes,
            weights=[0.15, 0.175, 0.15, 0.1, 0.125, 0.1, 0.1, 0.1],
        )

        # Nerf a few troublesome characters so that you can reasonably
        # get through the first few chapters.
        a000_table_rid = gd.multi_open("person", "GameData/Person/A000.bin.lz")
        a001_table_rid = gd.multi_open("person", "GameData/Person/A001.bin.lz")
        fighter_rid = gd.list_key_to_rid(
            a000_table_rid, "people", "PID_A000_アクスファイター初期"
        )
        lancer_rid = gd.list_key_to_rid(a000_table_rid, "people", "PID_A000_ランサー増援")
        a001_boss_rid = gd.list_key_to_rid(a001_table_rid, "people", "PID_A001_ボス")
        fe14_utils.nerf_character(gd, fighter_rid)
        fe14_utils.nerf_character(gd, lancer_rid)
        fe14_utils.nerf_character(gd, a001_boss_rid)
        # gd.multi_set_dirty("person", "GameData/Person/A000.bin.lz", True)
        # gd.multi_set_dirty("person", "GameData/Person/A001.bin.lz", True)

        gd.set_store_dirty("gamedata", True)
