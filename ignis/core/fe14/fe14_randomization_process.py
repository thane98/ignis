from random import Random
from typing import List

from ignis.core.fe14.step.fe14_randomize_chest_items_step import (
    FE14RandomizeChestItemsStep,
)

from ignis.core.fe14.fe14_chapter_vendor import FE14ChapterVendor
from ignis.core.fe14.fe14_character_vendor import FE14CharactersVendor
from ignis.core.fe14.fe14_classes_vendor import FE14ClassesVendor
from ignis.core.fe14.fe14_item_vendor import FE14ItemVendor
from ignis.core.fe14.fe14_skills_vendor import FE14SkillsVendor
from ignis.core.fe14.step.fe14_dispos_randomization_step import (
    FE14DisposRandomizationStep,
)
from ignis.core.fe14.step.fe14_global_character_randomization_step import (
    FE14GlobalCharacterRandomizationStep,
)
from ignis.core.fe14.step.fe14_person_randomization_step import (
    FE14PersonRandomizationStep,
)
from ignis.core.fe14.step.fe14_update_dialogue_step import FE14UpdateDialogueStep
from ignis.core.fe14.step.fe14_update_paralogue_unlocks_step import (
    FE14UpdateParalogueUnlocksStep,
)
from ignis.core.fe14.step.fe14_update_scripts_step import FE14UpdateScriptsStep
from ignis.core.fe14.step.handover_randomization_step import HandoverRandomizationStep
from ignis.core.fe14.step.leo_a001_model_replacement_step import (
    LeoA001ModelReplacementStep,
)
from ignis.core.fe14.step.unlock_hero_battles_step import UnlockHeroBattlesStep
from ignis.core.fe14.step.update_castle_join_step import UpdateCastleJoinStep
from ignis.core.step.generate_report_step import GenerateReportStep
from ignis.core.step.save_game_data_step import SaveGameDataStep
from ignis.model.fe14_dependencies import FE14Dependencies
from ignis.model.fe14_route_exception import FE14RouteException

from ignis.model.fe14_route import FE14Route

from ignis.core.randomization_process import RandomizationProcess
from ignis.core.randomization_step import RandomizationStep


class FE14RandomizationProcess(RandomizationProcess):
    def sanity_check(self):
        if FE14Route.BIRTHRIGHT in self.user_config.routes and not self.gd.file_exists(
            "GameData/Dispos/A/A008.bin.lz", False
        ):
            raise FE14RouteException(FE14Route.BIRTHRIGHT)
        if FE14Route.CONQUEST in self.user_config.routes and not self.gd.file_exists(
            "GameData/Dispos/B/B008.bin.lz", False
        ):
            raise FE14RouteException(FE14Route.CONQUEST)
        if FE14Route.REVELATION in self.user_config.routes and not self.gd.file_exists(
            "GameData/Dispos/C/C008.bin.lz", False
        ):
            raise FE14RouteException(FE14Route.REVELATION)

    def init_dependencies(self):
        rand = Random(self.user_config.seed)
        skills = FE14SkillsVendor(self.gd, self.game_config, rand)
        classes = FE14ClassesVendor(self.gd, self.game_config, rand)
        characters = FE14CharactersVendor(
            self.gd, self.game_config, self.user_config, skills, classes, rand
        )
        chapters = FE14ChapterVendor(self.gd, self.game_config, self.user_config)
        items = FE14ItemVendor(
            self.gd, self.game_config, self.user_config, rand, characters, classes
        )
        return FE14Dependencies(
            self.rom_path,
            self.output_path,
            rand,
            skills,
            classes,
            characters,
            chapters,
            items,
        )

    def steps(self) -> List[RandomizationStep]:
        return [
            FE14GlobalCharacterRandomizationStep(),
            FE14PersonRandomizationStep(),
            FE14DisposRandomizationStep(),
            FE14UpdateDialogueStep(),
            FE14UpdateScriptsStep(),
            FE14RandomizeChestItemsStep(),
            FE14UpdateParalogueUnlocksStep(),
            HandoverRandomizationStep(),
            UnlockHeroBattlesStep(),
            UpdateCastleJoinStep(),
            LeoA001ModelReplacementStep(),
            SaveGameDataStep(),
            GenerateReportStep(),
        ]
