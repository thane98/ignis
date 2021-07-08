import random
from typing import List

from PySide6.QtCore import Signal

from ignis.model.fe14_route import FE14Route
from ignis.model.fe14_user_config import FE14UserConfig
from ignis.model.stat_randomization_algorithm import StatRandomizationAlgorithm
from ignis.views.ui_fe14_user_config_form import Ui_FE14UserConfigForm


class FE14UserConfigForm(Ui_FE14UserConfigForm):
    updated = Signal(bool)

    def __init__(self):
        super().__init__()

        self.seed_input.setValue(random.randint(-10000, 10000))

        self.birthright_check_box.stateChanged.connect(self._on_update)
        self.conquest_check_box.stateChanged.connect(self._on_update)
        self.revelation_check_box.stateChanged.connect(self._on_update)

    def config(self) -> FE14UserConfig:
        if not self.fields_are_valid():
            raise RuntimeError("Called config when fields were invalid.")
        return FE14UserConfig(
            routes=self._get_routes(),
            stat_randomization_algorithm=self._get_stat_randomization_algorithm(),
            randomize_personal_skills=self.randomize_personal_skills_check_box.isChecked(),
            randomize_equip_skills=self.randomize_equip_skills_check_box.isChecked(),
            include_all_skills_in_skill_pool=self.include_all_skills_check_box.isChecked(),
            randomize_classes=self.randomize_classes_check_box.isChecked(),
            randomize_chest_items=self.randomize_chest_items_check_box.isChecked(),
            unlock_hero_battles=self.unlock_hero_battles_check_box.isChecked(),
            add_anna_to_castle_join=self.add_anna_check_box.isChecked(),
            include_anna_in_character_pool=self.add_anna_check_box.isChecked(),
            include_amiibo_units_in_character_pool=self.amiibo_check_box.isChecked(),
            randomize_children=self.children_check_box.isChecked(),
            randomize_join_order=self.randomize_join_order_check_box.isChecked(),
            same_sex_swaps_only=self.same_sex_only_check_box.isChecked(),
            seed=self.seed_input.value(),
        )

    def fields_are_valid(self):
        return bool(self._get_routes())

    def _on_update(self):
        self.updated.emit(self.fields_are_valid())

    def _get_routes(self) -> List[FE14Route]:
        routes = []
        if self.birthright_check_box.isChecked():
            routes.append(FE14Route.BIRTHRIGHT)
        if self.conquest_check_box.isChecked():
            routes.append(FE14Route.CONQUEST)
        if self.revelation_check_box.isChecked():
            routes.append(FE14Route.REVELATION)
        return routes

    def _get_stat_randomization_algorithm(self) -> StatRandomizationAlgorithm:
        if self.no_stats_radio.isChecked():
            return StatRandomizationAlgorithm.NONE
        elif self.redistribute_stats_radio.isChecked():
            return StatRandomizationAlgorithm.REDISTRIBUTE
        else:
            return StatRandomizationAlgorithm.SHUFFLE
